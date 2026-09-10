import sqlite3
import tempfile
import unittest
from pathlib import Path

from storage import (
    abort_game,
    add_learning_unit,
    add_question,
    add_student,
    connect,
    create_course,
    create_round,
    game_history,
    get_game,
    list_courses,
    randomize_teams,
    start_game,
    StorageError,
    update_course_team_names,
)


class TeamNamesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "test.sqlite3"
        self.conn = connect(self.path)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def _prepare_game(self, team1="Blue", team2="Gold"):
        create_course(self.conn, "DEMO", "Demo", team1, team2)
        cid = self.conn.execute("SELECT id FROM courses WHERE code='DEMO'").fetchone()[0]
        add_learning_unit(self.conn, "LE1", "Demo", 1)
        uid = self.conn.execute("SELECT id FROM learning_units WHERE code='LE1'").fetchone()[0]
        qids = []
        for i in range(8):
            add_question(self.conn, uid, f"Question {i+1}", f"Answer {i+1}")
            qids.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        rid = create_round(self.conn, "Round 1", qids)
        for i in range(8):
            add_student(self.conn, cid, f"Student {i+1}")
        randomize_teams(self.conn, cid)
        students = [r["id"] for r in self.conn.execute("SELECT id FROM students ORDER BY id")]
        gid = start_game(self.conn, rid, cid, students)
        return cid, rid, gid

    def test_custom_team_names_can_be_set_on_course_creation(self):
        create_course(self.conn, "ABC", "Course", "Red Foxes", "Night Owls")
        course = list_courses(self.conn)[0]
        self.assertEqual(course["team1_name"], "Red Foxes")
        self.assertEqual(course["team2_name"], "Night Owls")
        self.assertEqual(self.conn.execute("PRAGMA user_version").fetchone()[0], 3)

    def test_default_team_names_preserve_previous_behavior(self):
        create_course(self.conn, "ABC")
        course = list_courses(self.conn)[0]
        self.assertEqual((course["team1_name"], course["team2_name"]), ("Team 1", "Team 2"))

    def test_team_names_must_be_nonempty_and_distinct(self):
        with self.assertRaises(StorageError) as missing:
            create_course(self.conn, "ABC", "", "", "Gold")
        self.assertEqual(missing.exception.code, "course.error.team_name_required")

        with self.assertRaises(StorageError) as duplicate:
            create_course(self.conn, "ABC", "", "Alpha", " alpha ")
        self.assertEqual(duplicate.exception.code, "course.error.team_names_distinct")

    def test_team_names_can_be_changed_without_changing_internal_team_assignment(self):
        create_course(self.conn, "ABC", "", "Blue", "Gold")
        cid = self.conn.execute("SELECT id FROM courses WHERE code='ABC'").fetchone()[0]
        add_student(self.conn, cid, "Student", team=1)
        sid = self.conn.execute("SELECT id FROM students").fetchone()[0]

        update_course_team_names(self.conn, cid, "North", "South")

        course = self.conn.execute("SELECT * FROM courses WHERE id=?", (cid,)).fetchone()
        student = self.conn.execute("SELECT team FROM students WHERE id=?", (sid,)).fetchone()
        self.assertEqual((course["team1_name"], course["team2_name"]), ("North", "South"))
        self.assertEqual(student["team"], 1)

    def test_running_game_locks_team_names_and_game_keeps_snapshots(self):
        cid, _, gid = self._prepare_game("Blue", "Gold")
        game = get_game(self.conn, gid)
        self.assertEqual((game["team1_name_snapshot"], game["team2_name_snapshot"]), ("Blue", "Gold"))

        with self.assertRaises(StorageError) as locked:
            update_course_team_names(self.conn, cid, "North", "South")
        self.assertEqual(locked.exception.code, "course.error.team_names_running_game")

        abort_game(self.conn, gid)
        update_course_team_names(self.conn, cid, "North", "South")
        course = self.conn.execute("SELECT team1_name,team2_name FROM courses WHERE id=?", (cid,)).fetchone()
        game = get_game(self.conn, gid)
        history = game_history(self.conn, cid)[0]
        self.assertEqual((course["team1_name"], course["team2_name"]), ("North", "South"))
        self.assertEqual((game["team1_name_snapshot"], game["team2_name_snapshot"]), ("Blue", "Gold"))
        self.assertEqual((history["team1_name_snapshot"], history["team2_name_snapshot"]), ("Blue", "Gold"))

    def test_ui_uses_course_and_game_specific_team_names(self):
        source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        self.assertIn('update_course_team_names(conn,team_course["id"],new_team1,new_team2)', source)
        self.assertIn('s1.metric(team_name(1,game),game["team1_points"])', source)
        self.assertIn('s2.metric(team_name(2,game),game["team2_points"])', source)
        self.assertIn('present1=c1.multiselect(tr("game.attendance.team", team=team_name(1,course))', source)
        self.assertNotIn('s1.metric(tr("team.1"),game["team1_points"])', source)
        self.assertNotIn('s2.metric(tr("team.2"),game["team2_points"])', source)

    def test_schema_v2_migrates_in_place_to_v3_without_data_loss(self):
        self.conn.close()
        legacy = sqlite3.connect(self.path)
        legacy.executescript(
            """
            DROP TABLE IF EXISTS game_undo;
            DROP TABLE IF EXISTS game_cards;
            DROP TABLE IF EXISTS game_roster;
            DROP TABLE IF EXISTS games;
            DROP TABLE IF EXISTS round_questions;
            DROP TABLE IF EXISTS rounds;
            DROP TABLE IF EXISTS questions;
            DROP TABLE IF EXISTS learning_units;
            DROP TABLE IF EXISTS students;
            DROP TABLE IF EXISTS courses;
            DROP TABLE IF EXISTS app_settings;

            CREATE TABLE courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL DEFAULT '',
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );
            CREATE TABLE rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                locked INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                locked_at TEXT
            );
            CREATE TABLE games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                round_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'running',
                started_at TEXT NOT NULL,
                finished_at TEXT,
                team1_points INTEGER NOT NULL DEFAULT 0,
                team2_points INTEGER NOT NULL DEFAULT 0,
                team1_assist_used INTEGER NOT NULL DEFAULT 0,
                team2_assist_used INTEGER NOT NULL DEFAULT 0,
                current_student_id INTEGER,
                current_team INTEGER,
                turn_no INTEGER NOT NULL DEFAULT 1,
                player_selection_mode TEXT NOT NULL DEFAULT 'manual',
                UNIQUE(round_id, course_id)
            );
            CREATE TABLE app_settings (setting_key TEXT PRIMARY KEY, setting_value TEXT NOT NULL);
            INSERT INTO courses(id,code,title,active,created_at) VALUES(1,'KEEP','Existing',1,'2026-09-01T00:00:00+00:00');
            INSERT INTO rounds(id,name,locked,created_at) VALUES(1,'Round 1',1,'2026-09-01T00:00:00+00:00');
            INSERT INTO games(id,round_id,course_id,status,started_at,finished_at,team1_points,team2_points)
                VALUES(1,1,1,'finished','2026-09-01T10:00:00+00:00','2026-09-01T11:00:00+00:00',4,3);
            PRAGMA user_version=2;
            """
        )
        legacy.commit()
        legacy.close()

        self.conn = connect(self.path)
        self.assertEqual(self.conn.execute("PRAGMA user_version").fetchone()[0], 3)
        course = self.conn.execute("SELECT code,title,team1_name,team2_name FROM courses WHERE id=1").fetchone()
        game = self.conn.execute("SELECT status,team1_points,team2_points,team1_name_snapshot,team2_name_snapshot FROM games WHERE id=1").fetchone()
        self.assertEqual(tuple(course), ("KEEP", "Existing", "Team 1", "Team 2"))
        self.assertEqual(tuple(game), ("finished", 4, 3, "Team 1", "Team 2"))
        self.assertEqual(self.conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        self.assertEqual(self.conn.execute("PRAGMA foreign_key_check").fetchall(), [])


if __name__ == "__main__":
    unittest.main()
