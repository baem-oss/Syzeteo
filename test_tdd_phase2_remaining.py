"""Domain assertions for the remaining Phase-2 legacy acceptance criteria.

A test here verifies a concrete outcome (rather than just method existence).
Browser rendering remains separately subject to the manual acceptance record.
"""
import json
import tempfile
import unittest
from pathlib import Path

from storage import (
    StorageError, connect, create_course, add_student, list_students,
    add_learning_unit, update_learning_unit, list_learning_units,
    add_question, update_question, list_questions,
    export_question_pool_json, import_question_pool_json,
    create_round, round_questions, start_game, get_game, game_cards,
    game_roster, change_start_player, reveal_card, resolve_question,
    add_late_player, undo_last_action, dashboard_configuration_issues,
    dashboard_round_status, course_scoreboard, game_history,
    abort_game, delete_aborted_game, update_course_team_names,
    question_analysis_rows, tic_tac_toe_line, CARD_TYPE_CHALLENGE,
)


class RemainingPhase2AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "phase2.db")
        create_course(self.conn, "A")
        create_course(self.conn, "B")
        self.course = {
            row["code"]: row["id"]
            for row in self.conn.execute("SELECT id, code FROM courses")
        }
        add_learning_unit(self.conn, "LE1", "Learning unit", 1)
        self.unit = self.conn.execute(
            "SELECT id FROM learning_units WHERE code='LE1'"
        ).fetchone()[0]
        self.questions = []
        for n in range(8):
            add_question(self.conn, self.unit, f"Question {n}", f"Answer {n}")
            self.questions.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        self.round = create_round(self.conn, "Round P2", self.questions)
        for n in range(10):
            add_student(self.conn, self.course["A"], f"Student {n}",
                        team=1 if n < 5 else 2)
        self.students = list_students(self.conn, self.course["A"])
        self.present = [r["id"] for r in self.students if r["team"] == 1][:4] + [
            r["id"] for r in self.students if r["team"] == 2][:4]

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def game(self, **kwargs):
        return start_game(self.conn, self.round, self.course["A"], self.present, **kwargs)

    def first_question(self, gid):
        return next(c for c in game_cards(self.conn, gid) if c["card_type"] == "question")

    def test_us01_manual_starter_selection_replaces_random_choice_before_first_card(self):
        chosen = self.present[-1]
        gid = self.game(first_player_mode="manual", first_player_id=chosen)
        game = get_game(self.conn, gid)
        self.assertEqual(game["current_student_id"], chosen)
        team = next(s["team"] for s in self.students if s["id"] == chosen)
        self.assertEqual(game["current_team"], team)
        self.assertEqual(sum(r["has_played"] for r in game_roster(self.conn, gid)), 1)
        with self.assertRaises(StorageError):
            change_start_player(self.conn, gid, self.present[0])

    def test_us02_selection_mode_is_frozen_in_running_game(self):
        gid = self.game(player_selection_mode="manual")
        self.assertEqual(get_game(self.conn, gid)["player_selection_mode"], "manual")
        card = self.first_question(gid)
        reveal_card(self.conn, gid, card["card_no"])
        resolve_question(self.conn, gid, card["id"], 1)
        self.assertEqual(get_game(self.conn, gid)["player_selection_mode"], "manual")
        self.assertEqual(get_game(self.conn, gid)["turn_no"], 1)

    def test_us03_late_arrival_is_added_only_to_running_roster(self):
        absent = next(s for s in self.students if s["id"] not in self.present)
        gid = self.game()
        self.assertNotIn(absent["id"], [r["student_id"] for r in game_roster(self.conn, gid)])
        add_late_player(self.conn, gid, absent["id"])
        self.assertIn(absent["id"], [r["student_id"] for r in game_roster(self.conn, gid)])
        with self.assertRaises(StorageError):
            add_late_player(self.conn, gid, absent["id"])

    def test_us04_instructor_settings_reports_empty_course_with_action(self):
        issues = dashboard_configuration_issues(self.conn)
        matching = [x for x in issues if x.get("action_page") == "students"
                    and x.get("title_params", {}).get("code") == "B"]
        self.assertTrue(matching)
        self.assertTrue(all(x["level"] == "warning" for x in matching))
        self.assertTrue(all(x["title_key"].startswith("config.issue.") for x in matching))

    def test_us11_only_present_students_enter_initial_game_roster(self):
        gid = self.game()
        roster = game_roster(self.conn, gid)
        self.assertEqual(len(roster), 8)
        self.assertEqual({r["student_id"] for r in roster}, set(self.present))
        self.assertEqual({r["team_snapshot"] for r in roster}, {1, 2})

    def test_us12_learning_unit_can_be_renamed_and_reordered(self):
        update_learning_unit(self.conn, self.unit, "LE2", "Renamed", 4)
        unit = next(u for u in list_learning_units(self.conn)
                    if u["id"] == self.unit)
        self.assertEqual((unit["code"], unit["title"], unit["position"]),
                         ("LE2", "Renamed", 4))

    def test_us13_question_edit_and_archive_preserve_global_pool_entry(self):
        qid = self.questions[0]
        update_question(self.conn, qid, self.unit, "Revised", "New answer", False)
        stored = next(q for q in list_questions(self.conn) if q["id"] == qid)
        self.assertEqual((stored["question_text"], stored["answer_text"], stored["active"]),
                         ("Revised", "New answer", 0))
        self.assertNotIn(qid, [q["id"] for q in list_questions(self.conn, active_only=True)])

    def test_us14_question_pool_export_import_preserves_unit_and_question(self):
        payload = json.loads(export_question_pool_json(self.conn).decode("utf-8"))
        self.assertEqual(len(payload["questions"]), 8)
        self.assertEqual(payload["learning_units"][0]["code"], "LE1")
        fresh = connect(Path(self.tmp.name) / "import.db")
        try:
            import_question_pool_json(fresh, json.dumps(payload).encode("utf-8"))
            self.assertEqual(len(list_learning_units(fresh)), 1)
            self.assertEqual(len(list_questions(fresh)), 8)
            self.assertEqual(list_questions(fresh)[0]["answer_text"], "Answer 0")
        finally:
            fresh.close()

    def test_us15_round_has_exactly_eight_distinct_questions_in_order(self):
        questions = round_questions(self.conn, self.round)
        self.assertEqual(len(questions), 8)
        self.assertEqual([q["position"] for q in questions], list(range(1, 9)))
        self.assertEqual([q["question_id"] for q in questions], self.questions)
        with self.assertRaises(StorageError):
            create_round(self.conn, "Invalid", self.questions[:7])

    def test_us16_start_creates_nine_cards_and_disallows_second_start_for_same_course(self):
        gid = self.game()
        cards = game_cards(self.conn, gid)
        self.assertEqual(len(cards), 9)
        self.assertEqual(sum(c["card_type"] == CARD_TYPE_CHALLENGE for c in cards), 1)
        with self.assertRaises(StorageError):
            self.game()
        self.assertEqual(get_game(self.conn, gid)["status"], "running")

    def test_us17_scoring_question_updates_only_current_team_points(self):
        gid = self.game()
        before = get_game(self.conn, gid)
        card = self.first_question(gid)
        reveal_card(self.conn, gid, card["card_no"])
        resolve_question(self.conn, gid, card["id"], 1)
        after = get_game(self.conn, gid)
        scoring = "team1_points" if before["current_team"] == 1 else "team2_points"
        other = "team2_points" if scoring == "team1_points" else "team1_points"
        self.assertEqual(after[scoring] - before[scoring], 1)
        self.assertEqual(after[other], before[other])
        self.assertEqual(next(c for c in game_cards(self.conn, gid)
                              if c["id"] == card["id"])["resolved"], 1)

    def test_us18_team_assist_is_consumed_once_and_does_not_store_person_performance(self):
        gid = self.game()
        active = get_game(self.conn, gid)["current_team"]
        teammate = next(r for r in game_roster(self.conn, gid)
                        if r["team_snapshot"] == active)
        card = self.first_question(gid)
        reveal_card(self.conn, gid, card["card_no"])
        resolve_question(self.conn, gid, card["id"], 1, team_assist_used=True,
                         answered_by_student_id=teammate["student_id"])
        used = "team1_assist_used" if active == 1 else "team2_assist_used"
        self.assertEqual(get_game(self.conn, gid)[used], 1)
        stored = next(c for c in game_cards(self.conn, gid) if c["id"] == card["id"])
        self.assertEqual(stored["team_assist_used"], 1)
        self.assertIsNone(stored["answered_by_student_id"])

    def test_us19_challenge_card_can_award_two_points_to_active_team(self):
        gid = self.game()
        card = next(c for c in game_cards(self.conn, gid)
                    if c["card_type"] == CARD_TYPE_CHALLENGE)
        before = get_game(self.conn, gid)
        reveal_card(self.conn, gid, card["card_no"])
        resolve_question(self.conn, gid, card["id"], 2)
        after = get_game(self.conn, gid)
        point_key = "team1_points" if before["current_team"] == 1 else "team2_points"
        self.assertEqual(after[point_key] - before[point_key], 2)

    def test_us20_undo_restores_points_and_unresolved_card(self):
        gid = self.game()
        card = self.first_question(gid)
        reveal_card(self.conn, gid, card["card_no"])
        before = get_game(self.conn, gid)
        resolve_question(self.conn, gid, card["id"], 1)
        undo_last_action(self.conn, gid)
        after = get_game(self.conn, gid)
        self.assertEqual((after["team1_points"], after["team2_points"]),
                         (before["team1_points"], before["team2_points"]))
        restored = next(c for c in game_cards(self.conn, gid) if c["card_no"] == card["card_no"])
        self.assertEqual((restored["revealed"], restored["resolved"]), (1, 0))

    def test_us22_question_text_escapes_html_in_projection_rendering(self):
        from rendering import plain_text_html
        rendered = plain_text_html("Question <script>alert(1)</script>\n2. Next")
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("2. Next", rendered)

    def test_us23_finished_results_are_included_but_running_games_not_scored(self):
        gid = self.game()
        self.conn.execute("UPDATE games SET status='finished', team1_points=3, team2_points=2 WHERE id=?",
                          (gid,))
        self.conn.commit()
        scores = {r["code"]: r for r in course_scoreboard(self.conn)}
        self.assertEqual(scores["A"]["team1_points"], 3)
        self.assertEqual(scores["A"]["games_played"], 1)
        self.assertEqual(scores["B"]["games_played"], 0)
        self.assertEqual(game_history(self.conn, self.course["A"])[0]["id"], gid)

    def test_us25_round_coverage_distinguishes_running_played_and_open_courses(self):
        gid = self.game()
        status = next(r for r in dashboard_round_status(self.conn)
                      if r["id"] == self.round)
        self.assertEqual(status["coverage"]["A"], "running")
        self.assertEqual(status["coverage"]["B"], "open")
        self.conn.execute("UPDATE games SET status='finished' WHERE id=?", (gid,))
        self.conn.commit()
        status = next(r for r in dashboard_round_status(self.conn)
                      if r["id"] == self.round)
        self.assertEqual(status["coverage"]["A"], "played")
        self.assertEqual(status["coverage"]["B"], "open")

    def test_us26_aborted_game_deletion_removes_cards_and_releases_round(self):
        gid = self.game()
        abort_game(self.conn, gid)
        self.assertEqual(get_game(self.conn, gid)["status"], "aborted")
        delete_aborted_game(self.conn, gid)
        self.assertIsNone(get_game(self.conn, gid))
        self.assertEqual(game_cards(self.conn, gid), [])
        successor = self.game()
        self.assertNotEqual(successor, gid)

    def test_us27_team_name_changes_preserve_running_game_snapshots(self):
        update_course_team_names(self.conn, self.course["A"], "Blue", "Red")
        gid = self.game()
        game = get_game(self.conn, gid)
        self.assertEqual((game["team1_name_snapshot"], game["team2_name_snapshot"]),
                         ("Blue", "Red"))
        with self.assertRaises(StorageError):
            update_course_team_names(self.conn, self.course["A"], "One", "Two")
        self.assertEqual((get_game(self.conn, gid)["team1_name_snapshot"],
                          get_game(self.conn, gid)["team2_name_snapshot"]), ("Blue", "Red"))

    def test_us28_analysis_excludes_unfinished_games_and_student_identity(self):
        gid = self.game()
        card = self.first_question(gid)
        reveal_card(self.conn, gid, card["card_no"])
        resolve_question(self.conn, gid, card["id"], 1)
        self.assertEqual(question_analysis_rows(self.conn), [])
        self.conn.execute("UPDATE games SET status='finished' WHERE id=?", (gid,))
        self.conn.commit()
        fields = {r[1] for r in self.conn.execute("PRAGMA table_info(game_cards)")}
        self.assertIn("answered_by_student_id", fields)
        self.assertNotIn("answered_by_student_id", {
            field for row in question_analysis_rows(self.conn)
            for field in row.keys()
        })

    def test_us29_tic_tac_toe_recognizes_scored_team_row_without_changing_points(self):
        cards = [{"points_team": 1 if i < 3 else None,
                  "resolved_at": f"2026-10-29T12:00:0{i}"} for i in range(9)]
        winner = tic_tac_toe_line(cards)
        self.assertIsNotNone(winner)
        self.assertEqual((winner[0], tuple(winner[1]), winner[2]),
                         (1, (0, 1, 2), "row"))
        self.assertEqual(sum(c["points_team"] == 1 for c in cards), 3)


if __name__ == "__main__":
    unittest.main()
