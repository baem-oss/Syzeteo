import tempfile
import unittest
from pathlib import Path

from storage import (
    StorageError,
    abort_game,
    add_learning_unit,
    add_question,
    add_student,
    connect,
    course_scoreboard,
    create_course,
    create_round,
    dashboard_round_status,
    delete_aborted_game,
    game_cards,
    get_game,
    list_games,
    randomize_teams,
    start_game,
)


class AbortDeleteGameTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "test.sqlite3")

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def prepare_game(self):
        create_course(self.conn, "WIBE225")
        cid = self.conn.execute("SELECT id FROM courses WHERE code='WIBE225'").fetchone()[0]
        add_learning_unit(self.conn, "LE1", "Test", 1)
        uid = self.conn.execute("SELECT id FROM learning_units WHERE code='LE1'").fetchone()[0]
        qids = []
        for i in range(8):
            add_question(self.conn, uid, f"Question {i+1}", f"Answer {i+1}")
            qids.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        rid = create_round(self.conn, "Round 1", qids)
        for i in range(8):
            add_student(self.conn, cid, f"Student {i+1}")
        randomize_teams(self.conn, cid)
        students = [r["id"] for r in self.conn.execute("SELECT id FROM students ORDER BY id").fetchall()]
        gid = start_game(self.conn, rid, cid, students)
        return cid, rid, gid, students

    def test_running_game_can_be_aborted_and_is_not_running_afterwards(self):
        cid, rid, gid, _ = self.prepare_game()
        abort_game(self.conn, gid)
        self.assertEqual(get_game(self.conn, gid)["status"], "aborted")
        self.assertEqual(list_games(self.conn, "running"), [])
        self.assertEqual([g["id"] for g in list_games(self.conn, "aborted")], [gid])
        coverage = next(r for r in dashboard_round_status(self.conn) if int(r["id"]) == int(rid))
        self.assertEqual(coverage["coverage"]["WIBE225"], "aborted")

    def test_aborted_game_is_excluded_from_results(self):
        cid, _, gid, _ = self.prepare_game()
        self.conn.execute("UPDATE games SET team1_points=3,team2_points=2 WHERE id=?", (gid,))
        self.conn.commit()
        abort_game(self.conn, gid)
        score = next(r for r in course_scoreboard(self.conn) if int(r["id"]) == int(cid))
        self.assertEqual((score["team1_points"], score["team2_points"]), (0, 0))
        self.assertEqual(int(score["games_played"] or 0), 0)

    def test_only_running_games_can_be_aborted(self):
        _, _, gid, _ = self.prepare_game()
        self.conn.execute("UPDATE games SET status='finished' WHERE id=?", (gid,))
        self.conn.commit()
        with self.assertRaises(StorageError) as ctx:
            abort_game(self.conn, gid)
        self.assertEqual(ctx.exception.code, "error.game.abort_running_only")

    def test_only_aborted_games_can_be_deleted(self):
        _, _, gid, _ = self.prepare_game()
        with self.assertRaises(StorageError) as ctx:
            delete_aborted_game(self.conn, gid)
        self.assertEqual(ctx.exception.code, "error.game.delete_aborted_only")
        self.assertIsNotNone(get_game(self.conn, gid))

    def test_delete_aborted_game_cascades_and_round_can_be_started_again(self):
        cid, rid, gid, students = self.prepare_game()
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM game_roster WHERE game_id=?", (gid,)).fetchone()[0], 8)
        self.assertEqual(len(game_cards(self.conn, gid)), 9)
        abort_game(self.conn, gid)
        delete_aborted_game(self.conn, gid)
        self.assertIsNone(get_game(self.conn, gid))
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM game_roster WHERE game_id=?", (gid,)).fetchone()[0], 0)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM game_cards WHERE game_id=?", (gid,)).fetchone()[0], 0)
        coverage = next(r for r in dashboard_round_status(self.conn) if int(r["id"]) == int(rid))
        self.assertEqual(coverage["coverage"]["WIBE225"], "open")
        replacement = start_game(self.conn, rid, cid, students)
        self.assertNotEqual(replacement, gid)
        self.assertEqual(get_game(self.conn, replacement)["status"], "running")


if __name__ == "__main__":
    unittest.main()
