import tempfile
import unittest
from pathlib import Path

from storage import (
    add_late_player,
    add_learning_unit,
    add_question,
    add_student,
    archive_course,
    change_start_player,
    connect,
    create_course,
    create_round,
    delete_learning_unit,
    delete_question,
    dashboard_configuration_issues,
    export_question_pool_json,
    game_cards,
    get_game,
    import_question_pool_json,
    preview_question_pool_import,
    randomize_teams,
    reactivate_course,
    resolve_question,
    reveal_card,
    game_roster,
    round_questions,
    set_next_player,
    start_game,
    StorageError,
    update_learning_unit,
    update_question,
    undo_last_action,
    undo_info,
)


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "test.sqlite3")

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def prepare_round(self, student_count=8):
        create_course(self.conn, "WIBE125")
        cid = self.conn.execute("SELECT id FROM courses").fetchone()[0]
        add_learning_unit(self.conn, "LE1", "Test", 1)
        uid = self.conn.execute("SELECT id FROM learning_units").fetchone()[0]
        qids = []
        for i in range(8):
            add_question(self.conn, uid, f"Frage {i}", f"Antwort {i}")
            qids.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        rid = create_round(self.conn, "Round 1", qids)
        for i in range(student_count):
            add_student(self.conn, cid, f"Person {i+1}")
        randomize_teams(self.conn, cid)
        students = [r["id"] for r in self.conn.execute("SELECT * FROM students").fetchall()]
        return cid, rid, students


    def test_course_errors_use_language_neutral_codes(self):
        with self.assertRaises(StorageError) as missing_code:
            create_course(self.conn, "")
        self.assertEqual(missing_code.exception.code, "course.error.code_required")

        create_course(self.conn, "DEMO")
        with self.assertRaises(StorageError) as duplicate:
            create_course(self.conn, "DEMO")
        self.assertEqual(duplicate.exception.code, "course.error.code_exists")
        self.assertEqual(duplicate.exception.params["code"], "DEMO")

        with self.assertRaises(StorageError) as not_found:
            archive_course(self.conn, 999999)
        self.assertEqual(not_found.exception.code, "course.error.not_found")


    def test_dashboard_configuration_issues_are_language_neutral(self):
        create_course(self.conn, "EMPTY")
        issues = dashboard_configuration_issues(self.conn)
        course_issue = next(i for i in issues if i["title_key"] == "config.issue.course_empty.title")
        self.assertEqual(course_issue["level"], "warning")
        self.assertEqual(course_issue["title_params"]["code"], "EMPTY")
        self.assertEqual(course_issue["impact_key"], "config.issue.course_empty.impact")
        self.assertEqual(course_issue["solution_key"], "config.issue.course_empty.solution")
        self.assertEqual(course_issue["action_page"], "students")
        self.assertEqual(course_issue["action_key"], "config.action.students")

    def test_round_has_eight_questions_and_locks_on_start(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students)
        self.assertEqual(get_game(self.conn, gid)["status"], "running")
        self.assertEqual(len(round_questions(self.conn, rid)), 8)
        self.assertEqual(self.conn.execute("SELECT locked FROM rounds WHERE id=?", (rid,)).fetchone()[0], 1)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM game_cards WHERE game_id=?", (gid,)).fetchone()[0], 9)

    def test_start_requires_four_present_per_team(self):
        cid, rid, students = self.prepare_round(6)
        with self.assertRaises(ValueError):
            start_game(self.conn, rid, cid, students)
        self.assertEqual(self.conn.execute("SELECT locked FROM rounds WHERE id=?", (rid,)).fetchone()[0], 0)

    def test_no_individual_answer_performance_is_stored(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students)
        first = game_cards(self.conn, gid)[0]
        reveal_card(self.conn, gid, first["card_no"])
        resolve_question(self.conn, gid, first["id"], 1)
        card = self.conn.execute("SELECT answered_by_student_id,points_awarded FROM game_cards WHERE id=?", (first["id"],)).fetchone()
        self.assertIsNone(card["answered_by_student_id"])
        self.assertEqual(card["points_awarded"], 1)


    def test_first_player_can_be_selected_manually_before_start(self):
        cid, rid, students = self.prepare_round(8)
        starter_id = int(students[2])
        gid = start_game(self.conn, rid, cid, students, "manual", starter_id)
        game = get_game(self.conn, gid)
        self.assertEqual(int(game["current_student_id"]), starter_id)
        self.assertEqual(game["player_selection_mode"], "random")
        played = self.conn.execute(
            "SELECT has_played FROM game_roster WHERE game_id=? AND student_id=?", (gid, starter_id)
        ).fetchone()
        self.assertEqual(played["has_played"], 1)

    def test_manual_first_player_must_be_present_and_selected(self):
        cid, rid, students = self.prepare_round(8)
        with self.assertRaises(ValueError):
            start_game(self.conn, rid, cid, students, "manual", None)

    def test_start_player_cannot_be_changed_after_game_creation(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students, "random")
        game = get_game(self.conn, gid)
        replacement = next(r for r in game_roster(self.conn, gid) if int(r["student_id"]) != int(game["current_student_id"]))
        with self.assertRaises(ValueError):
            change_start_player(self.conn, gid, replacement["student_id"])

    def test_random_mode_selects_next_player_and_undo_restores_pre_score_state(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students, "random")
        before = get_game(self.conn, gid)
        starter_id = int(before["current_student_id"])
        starter_team = int(before["current_team"])
        first = game_cards(self.conn, gid)[0]
        reveal_card(self.conn, gid, first["card_no"])
        resolve_question(self.conn, gid, first["id"], 1)

        after = get_game(self.conn, gid)
        self.assertEqual(after["player_selection_mode"], "random")
        self.assertEqual(int(after["turn_no"]), 2)
        self.assertNotEqual(int(after["current_student_id"]), starter_id)
        self.assertEqual(int(after["current_team"]), 2 if starter_team == 1 else 1)
        selected = self.conn.execute(
            "SELECT has_played FROM game_roster WHERE game_id=? AND student_id=?",
            (gid, after["current_student_id"]),
        ).fetchone()
        self.assertEqual(selected["has_played"], 1)

        undo_last_action(self.conn, gid)
        restored_game = get_game(self.conn, gid)
        restored_card = self.conn.execute(
            "SELECT revealed,resolved FROM game_cards WHERE id=?", (first["id"],)
        ).fetchone()
        self.assertEqual(int(restored_game["current_student_id"]), starter_id)
        self.assertEqual(int(restored_game["current_team"]), starter_team)
        self.assertEqual(int(restored_game["turn_no"]), 1)
        self.assertEqual((restored_card["revealed"], restored_card["resolved"]), (1, 0))
        self.assertEqual(
            self.conn.execute("SELECT COUNT(*) FROM game_roster WHERE game_id=? AND has_played=1", (gid,)).fetchone()[0],
            1,
        )

    def test_late_player_is_added_to_running_roster_and_undoable(self):
        cid, rid, students = self.prepare_round(10)
        rows = self.conn.execute("SELECT id,team FROM students WHERE course_id=? ORDER BY id", (cid,)).fetchall()
        team1 = [int(r["id"]) for r in rows if r["team"] == 1]
        team2 = [int(r["id"]) for r in rows if r["team"] == 2]
        present = team1[:4] + team2[:4]
        absent = next(sid for sid in team1 + team2 if sid not in present)
        gid = start_game(self.conn, rid, cid, present)

        add_late_player(self.conn, gid, absent)
        added = self.conn.execute(
            "SELECT has_played,team_snapshot FROM game_roster WHERE game_id=? AND student_id=?", (gid, absent)
        ).fetchone()
        self.assertIsNotNone(added)
        self.assertEqual(added["has_played"], 0)
        expected_team = self.conn.execute("SELECT team FROM students WHERE id=?", (absent,)).fetchone()[0]
        self.assertEqual(added["team_snapshot"], expected_team)

        with self.assertRaises(ValueError):
            add_late_player(self.conn, gid, absent)

        undo_last_action(self.conn, gid)
        self.assertIsNone(
            self.conn.execute("SELECT 1 FROM game_roster WHERE game_id=? AND student_id=?", (gid, absent)).fetchone()
        )

    def test_late_player_can_unblock_random_selection(self):
        cid, rid, students = self.prepare_round(10)
        rows = self.conn.execute("SELECT id,team FROM students WHERE course_id=? ORDER BY id", (cid,)).fetchall()
        by_team = {1:[int(r["id"]) for r in rows if r["team"]==1], 2:[int(r["id"]) for r in rows if r["team"]==2]}
        present = by_team[1][:4] + by_team[2][:4]
        gid = start_game(self.conn, rid, cid, present, "random")
        game = get_game(self.conn, gid)
        next_team = 2 if int(game["current_team"]) == 1 else 1

        # Simuliert einen erschöpften Kandidatenpool, z. B. nach bereits absolvierten regulären Einsätzen.
        self.conn.execute(
            "UPDATE game_roster SET has_played=1 WHERE game_id=? AND team_snapshot=?", (gid, next_team)
        )
        self.conn.commit()
        first = game_cards(self.conn, gid)[0]
        reveal_card(self.conn, gid, first["card_no"])
        resolve_question(self.conn, gid, first["id"], 1)
        blocked = get_game(self.conn, gid)
        self.assertEqual(int(blocked["turn_no"]), 1)

        late = next(sid for sid in by_team[next_team] if sid not in present)
        add_late_player(self.conn, gid, late)
        resumed = get_game(self.conn, gid)
        self.assertEqual(int(resumed["turn_no"]), 2)
        self.assertEqual(int(resumed["current_student_id"]), late)
        self.assertEqual(int(resumed["current_team"]), next_team)


    def test_manual_first_player_is_followed_by_automatic_random_player_two(self):
        cid, rid, students = self.prepare_round(8)
        starter_id = int(students[0])
        gid = start_game(self.conn, rid, cid, students, "manual", starter_id)
        before = get_game(self.conn, gid)
        starter_team = int(before["current_team"])
        first = game_cards(self.conn, gid)[0]
        reveal_card(self.conn, gid, first["card_no"])
        resolve_question(self.conn, gid, first["id"], 1)
        after = get_game(self.conn, gid)
        self.assertEqual(int(after["turn_no"]), 2)
        self.assertNotEqual(int(after["current_student_id"]), starter_id)
        self.assertEqual(int(after["current_team"]), 2 if starter_team == 1 else 1)

    def test_manual_next_player_selection_is_rejected_in_random_mode(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students, "random")
        candidate = next(r for r in game_roster(self.conn, gid) if not r["has_played"])
        with self.assertRaises(ValueError):
            set_next_player(self.conn, gid, candidate["student_id"])


    def test_manual_regular_mode_waits_for_instructor_and_accepts_only_next_team(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students, "random", None, "manual")
        before = get_game(self.conn, gid)
        starter_id = int(before["current_student_id"])
        starter_team = int(before["current_team"])
        first = game_cards(self.conn, gid)[0]
        reveal_card(self.conn, gid, first["card_no"])
        resolve_question(self.conn, gid, first["id"], 1)

        waiting = get_game(self.conn, gid)
        self.assertEqual(waiting["player_selection_mode"], "manual")
        self.assertEqual(int(waiting["turn_no"]), 1)
        self.assertEqual(int(waiting["current_student_id"]), starter_id)
        self.assertEqual(int(waiting["current_team"]), starter_team)

        same_team = next(
            r for r in game_roster(self.conn, gid, starter_team)
            if not r["has_played"]
        )
        with self.assertRaises(ValueError):
            set_next_player(self.conn, gid, same_team["student_id"])

        next_team = 2 if starter_team == 1 else 1
        candidate = next(r for r in game_roster(self.conn, gid, next_team) if not r["has_played"])
        set_next_player(self.conn, gid, candidate["student_id"])
        after = get_game(self.conn, gid)
        self.assertEqual(int(after["turn_no"]), 2)
        self.assertEqual(int(after["current_student_id"]), int(candidate["student_id"]))
        self.assertEqual(int(after["current_team"]), next_team)

    def test_manual_regular_mode_player_choice_shares_scoring_undo(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students, "random", None, "manual")
        before = get_game(self.conn, gid)
        starter_id = int(before["current_student_id"])
        starter_team = int(before["current_team"])
        first = game_cards(self.conn, gid)[0]
        reveal_card(self.conn, gid, first["card_no"])
        resolve_question(self.conn, gid, first["id"], 1)
        next_team = 2 if starter_team == 1 else 1
        candidate = next(r for r in game_roster(self.conn, gid, next_team) if not r["has_played"])
        set_next_player(self.conn, gid, candidate["student_id"])

        undo_last_action(self.conn, gid)
        restored = get_game(self.conn, gid)
        restored_card = self.conn.execute(
            "SELECT revealed,resolved FROM game_cards WHERE id=?", (first["id"],)
        ).fetchone()
        self.assertEqual(int(restored["current_student_id"]), starter_id)
        self.assertEqual(int(restored["current_team"]), starter_team)
        self.assertEqual(int(restored["turn_no"]), 1)
        self.assertEqual((restored_card["revealed"], restored_card["resolved"]), (1, 0))

    def test_random_mode_can_complete_all_student_turns_without_repetition(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students, "random")
        for _ in range(8):
            cards = game_cards(self.conn, gid)
            unresolved = [c for c in cards if not c["resolved"]]
            self.assertGreaterEqual(len(unresolved), 2)
            card = unresolved[0]
            reveal_card(self.conn, gid, card["card_no"])
            resolve_question(self.conn, gid, card["id"], 0)
        game = get_game(self.conn, gid)
        self.assertEqual(int(game["turn_no"]), 8)
        used = self.conn.execute(
            "SELECT team_snapshot,COUNT(*) n FROM game_roster WHERE game_id=? AND has_played=1 GROUP BY team_snapshot ORDER BY team_snapshot",
            (gid,),
        ).fetchall()
        self.assertEqual([(r["team_snapshot"], r["n"]) for r in used], [(1, 4), (2, 4)])
        self.assertEqual(
            self.conn.execute("SELECT COUNT(*) FROM game_cards WHERE game_id=? AND resolved=0", (gid,)).fetchone()[0],
            1,
        )

    def test_learning_unit_can_be_reordered_edited_and_only_deleted_without_questions(self):
        add_learning_unit(self.conn, "LE1", "Erste", 2)
        uid1 = self.conn.execute("SELECT id FROM learning_units WHERE code='LE1'").fetchone()[0]
        add_learning_unit(self.conn, "LE2", "Zweite", 1)
        uid2 = self.conn.execute("SELECT id FROM learning_units WHERE code='LE2'").fetchone()[0]
        add_question(self.conn, uid1, "Frage", "Antwort")

        with self.assertRaises(ValueError):
            delete_learning_unit(self.conn, uid1)

        update_question(self.conn, self.conn.execute("SELECT id FROM questions").fetchone()[0], uid2, "Frage", "Antwort", True)
        update_learning_unit(self.conn, uid1, "LE1A", "Erste geändert", 0)
        first = self.conn.execute("SELECT code,title,position FROM learning_units ORDER BY position,code").fetchone()
        self.assertEqual((first["code"], first["title"], first["position"]), ("LE1A", "Erste geändert", 0))
        delete_learning_unit(self.conn, uid1)
        self.assertIsNone(self.conn.execute("SELECT 1 FROM learning_units WHERE id=?", (uid1,)).fetchone())

    def test_question_delete_requires_removal_from_unlocked_round_but_preserves_locked_history(self):
        cid, rid, students = self.prepare_round(8)
        qid = self.conn.execute("SELECT question_id FROM round_questions WHERE round_id=? ORDER BY position LIMIT 1", (rid,)).fetchone()[0]
        with self.assertRaises(ValueError):
            delete_question(self.conn, qid)

        start_game(self.conn, rid, cid, students)
        before = [dict(r) for r in round_questions(self.conn, rid)]
        delete_question(self.conn, qid)
        self.assertIsNone(self.conn.execute("SELECT 1 FROM questions WHERE id=?", (qid,)).fetchone())
        after = [dict(r) for r in round_questions(self.conn, rid)]
        self.assertEqual(len(after), 8)
        self.assertEqual(after[0]["question_text"], before[0]["question_text"])
        self.assertEqual(after[0]["unit_code"], before[0]["unit_code"])

    def test_question_pool_import_only_adds_new_content_and_never_overwrites_existing(self):
        add_learning_unit(self.conn, "LE1", "Bestehender Titel", 7)
        uid = self.conn.execute("SELECT id FROM learning_units WHERE code='LE1'").fetchone()[0]
        add_question(self.conn, uid, "Bestehende Frage", "Bestehende Antwort")

        import tempfile as _tempfile
        other_tmp = _tempfile.TemporaryDirectory()
        try:
            other = connect(Path(other_tmp.name) / "other.sqlite3")
            add_learning_unit(other, "LE1", "Abweichender Titel", 1)
            other_uid1 = other.execute("SELECT id FROM learning_units WHERE code='LE1'").fetchone()[0]
            add_question(other, other_uid1, "Bestehende Frage", "Andere Antwort")
            add_learning_unit(other, "LE2", "Neue LE", 2)
            other_uid2 = other.execute("SELECT id FROM learning_units WHERE code='LE2'").fetchone()[0]
            add_question(other, other_uid2, "Neue Frage", "Neue Antwort")
            raw = export_question_pool_json(other)
            other.close()
        finally:
            other_tmp.cleanup()

        before_units = [tuple(r) for r in self.conn.execute("SELECT * FROM learning_units ORDER BY id").fetchall()]
        before_questions = [tuple(r) for r in self.conn.execute("SELECT * FROM questions ORDER BY id").fetchall()]
        preview = preview_question_pool_import(self.conn, raw)
        self.assertEqual(before_units, [tuple(r) for r in self.conn.execute("SELECT * FROM learning_units ORDER BY id").fetchall()])
        self.assertEqual(before_questions, [tuple(r) for r in self.conn.execute("SELECT * FROM questions ORDER BY id").fetchall()])
        self.assertEqual(preview["new_units"], 1)
        self.assertEqual(preview["new_questions"], 1)
        self.assertEqual(preview["duplicate_questions"], 1)
        result = import_question_pool_json(self.conn, raw)
        self.assertEqual(result["added_units"], 1)
        self.assertEqual(result["added_questions"], 1)
        self.assertEqual(result["skipped_questions"], 1)

        existing = self.conn.execute("SELECT title,position FROM learning_units WHERE code='LE1'").fetchone()
        self.assertEqual((existing["title"], existing["position"]), ("Bestehender Titel", 7))
        question = self.conn.execute("SELECT answer_text FROM questions WHERE question_text='Bestehende Frage'").fetchone()
        self.assertEqual(question["answer_text"], "Bestehende Antwort")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM learning_units WHERE code='LE2'").fetchone()[0], 1)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM questions WHERE question_text='Neue Frage'").fetchone()[0], 1)


    def test_course_archive_preserves_data_hides_course_and_can_be_reactivated(self):
        cid, rid, students = self.prepare_round(8)
        # Ohne laufendes Spiel darf der Kurs archiviert werden.
        before_students = self.conn.execute("SELECT COUNT(*) FROM students WHERE course_id=?", (cid,)).fetchone()[0]
        archive_course(self.conn, cid)
        self.assertEqual(self.conn.execute("SELECT active FROM courses WHERE id=?", (cid,)).fetchone()[0], 0)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM students WHERE course_id=?", (cid,)).fetchone()[0], before_students)
        from storage import list_courses
        self.assertFalse(any(r["id"] == cid for r in list_courses(self.conn)))
        self.assertTrue(any(r["id"] == cid for r in list_courses(self.conn, False)))
        reactivate_course(self.conn, cid)
        self.assertEqual(self.conn.execute("SELECT active FROM courses WHERE id=?", (cid,)).fetchone()[0], 1)

    def test_course_with_running_game_cannot_be_archived(self):
        cid, rid, students = self.prepare_round(8)
        start_game(self.conn, rid, cid, students)
        with self.assertRaises(ValueError):
            archive_course(self.conn, cid)
        self.assertEqual(self.conn.execute("SELECT active FROM courses WHERE id=?", (cid,)).fetchone()[0], 1)


    def test_undo_info_uses_language_neutral_action_descriptor(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students)
        first = game_cards(self.conn, gid)[0]
        reveal_card(self.conn, gid, first["card_no"])
        info = undo_info(self.conn, gid)
        self.assertEqual(info["action_key"], "undo.action.reveal_card")
        self.assertEqual(info["action_params"], {"card_no": first["card_no"]})
        self.assertNotIn("Karte", self.conn.execute("SELECT action_label FROM game_undo WHERE game_id=?", (gid,)).fetchone()[0])

    def test_undo_restores_last_scoring_step(self):
        cid, rid, students = self.prepare_round(8)
        gid = start_game(self.conn, rid, cid, students)
        first = game_cards(self.conn, gid)[0]
        reveal_card(self.conn, gid, first["card_no"])
        resolve_question(self.conn, gid, first["id"], 1)
        self.assertEqual(get_game(self.conn, gid)["team1_points"] + get_game(self.conn, gid)["team2_points"], 1)
        undo_last_action(self.conn, gid)
        restored = self.conn.execute("SELECT revealed,resolved,points_awarded FROM game_cards WHERE id=?", (first["id"],)).fetchone()
        self.assertEqual(restored["revealed"], 1)
        self.assertEqual(restored["resolved"], 0)
        self.assertEqual(restored["points_awarded"], 0)
        game = get_game(self.conn, gid)
        self.assertEqual(game["team1_points"] + game["team2_points"], 0)


if __name__ == "__main__":
    unittest.main()
