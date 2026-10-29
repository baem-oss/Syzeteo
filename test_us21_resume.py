"""US #21: running games remain resumable from persisted SQLite state."""
import tempfile
import unittest
from pathlib import Path

from storage import (connect, create_course, add_learning_unit, add_question,
                     create_round, add_student, randomize_teams, start_game,
                     get_game, list_games, game_cards, game_roster, current_player,
                     abort_game)


class US21ResumeAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "resume.sqlite3"
        self.conn = connect(self.db)
        create_course(self.conn, "C21")
        self.course = self.conn.execute("SELECT id FROM courses WHERE code='C21'").fetchone()[0]
        add_learning_unit(self.conn, "LE21", "Learning", 1)
        unit = self.conn.execute("SELECT id FROM learning_units WHERE code='LE21'").fetchone()[0]
        questions = []
        for number in range(8):
            add_question(self.conn, unit, f"Question {number}", f"Answer {number}")
            questions.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        self.round = create_round(self.conn, "US21-Round", questions)
        for number in range(8):
            add_student(self.conn, self.course, f"Player {number}")
        randomize_teams(self.conn, self.course)
        students = [r["id"] for r in self.conn.execute(
            "SELECT id FROM students WHERE course_id=? ORDER BY id", (self.course,))]
        self.gid = start_game(self.conn, self.round, self.course, students)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def reconnect(self):
        self.conn.close()
        self.conn = connect(self.db)

    def test_us21_running_game_can_be_found_after_restart(self):
        self.reconnect()
        running = list_games(self.conn, "running")
        self.assertEqual([r["id"] for r in running], [self.gid])
        self.assertEqual(get_game(self.conn, self.gid)["status"], "running")

    def test_us21_game_state_cards_and_roster_survive_restart(self):
        before = get_game(self.conn, self.gid)
        before_roster = [tuple(r) for r in game_roster(self.conn, self.gid)]
        before_cards = [tuple(r) for r in game_cards(self.conn, self.gid)]
        self.assertEqual(len(before_cards), 9)
        self.reconnect()
        after = get_game(self.conn, self.gid)
        for column in ("current_student_id", "current_team", "turn_no",
                       "team1_points", "team2_points", "player_selection_mode",
                       "team1_name_snapshot", "team2_name_snapshot"):
            self.assertEqual(after[column], before[column], column)
        self.assertEqual([tuple(r) for r in game_cards(self.conn, self.gid)], before_cards)
        self.assertEqual([tuple(r) for r in game_roster(self.conn, self.gid)], before_roster)
        self.assertEqual(current_player(self.conn, after)["student_id"], after["current_student_id"])

    def test_us21_aborted_game_cannot_be_resumed_as_running(self):
        abort_game(self.conn, self.gid)
        self.reconnect()
        self.assertEqual(list_games(self.conn, "running"), [])
        self.assertEqual(get_game(self.conn, self.gid)["status"], "aborted")


if __name__ == "__main__":
    unittest.main()
