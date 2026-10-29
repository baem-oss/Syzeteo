"""US #21: running games remain resumable from persisted SQLite state."""
import tempfile
import unittest
from pathlib import Path

from storage import (connect, create_course, add_learning_unit, add_question,
                     create_round, add_student, randomize_teams, start_game,
                     get_game, list_games, game_cards, game_roster, current_player,
                     reveal_card, resolve_question,
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


    def test_us21_scored_turn_can_continue_after_restart(self):
        first = game_cards(self.conn, self.gid)[0]
        reveal_card(self.conn, self.gid, first["card_no"])
        resolve_question(self.conn, self.gid, first["id"], 1)
        before = get_game(self.conn, self.gid)
        before_cards = [tuple(r) for r in game_cards(self.conn, self.gid)]
        before_roster = [tuple(r) for r in game_roster(self.conn, self.gid)]
        self.assertEqual(before["turn_no"], 2)
        self.assertEqual(before["team1_points"] + before["team2_points"], 1)
        self.reconnect()
        restored = get_game(self.conn, self.gid)
        self.assertEqual(restored["status"], "running")
        for field in ("current_student_id", "current_team", "turn_no",
                      "team1_points", "team2_points", "player_selection_mode"):
            self.assertEqual(restored[field], before[field], field)
        self.assertEqual([tuple(r) for r in game_cards(self.conn, self.gid)], before_cards)
        self.assertEqual([tuple(r) for r in game_roster(self.conn, self.gid)], before_roster)
        next_card = next(c for c in game_cards(self.conn, self.gid) if not c["resolved"])
        reveal_card(self.conn, self.gid, next_card["card_no"])
        self.assertEqual(
            next(c for c in game_cards(self.conn, self.gid)
                 if c["card_no"] == next_card["card_no"])["revealed"], 1)


    def test_us21_two_scored_turns_survive_restart_and_allow_third_score(self):
        """Resume an actually progressed game, not only its initial database row."""
        for _ in range(2):
            card = next(c for c in game_cards(self.conn, self.gid)
                        if c["card_type"] == "question" and not c["resolved"])
            reveal_card(self.conn, self.gid, card["card_no"])
            resolve_question(self.conn, self.gid, card["id"], 1)
        before = get_game(self.conn, self.gid)
        self.assertEqual(before["turn_no"], 3)
        self.assertEqual(before["team1_points"] + before["team2_points"], 2)
        prior_cards = [tuple(c) for c in game_cards(self.conn, self.gid)]
        prior_roster = [tuple(p) for p in game_roster(self.conn, self.gid)]
        self.reconnect()
        restored = get_game(self.conn, self.gid)
        self.assertEqual(restored["status"], "running")
        for key in ("turn_no", "current_student_id", "current_team",
                    "team1_points", "team2_points"):
            self.assertEqual(restored[key], before[key], key)
        self.assertEqual([tuple(c) for c in game_cards(self.conn, self.gid)], prior_cards)
        self.assertEqual([tuple(p) for p in game_roster(self.conn, self.gid)], prior_roster)
        third = next(c for c in game_cards(self.conn, self.gid)
                     if c["card_type"] == "question" and not c["resolved"])
        reveal_card(self.conn, self.gid, third["card_no"])
        resolve_question(self.conn, self.gid, third["id"], 1)
        after = get_game(self.conn, self.gid)
        self.assertEqual(after["turn_no"], 4)
        self.assertEqual(after["team1_points"] + after["team2_points"], 3)


if __name__ == "__main__":
    unittest.main()
