"""US #10 – direct acceptance tests for manual/random team assignment."""
import tempfile
import unittest
from pathlib import Path
from storage import (connect, create_course, add_student, list_students,
                     update_student, randomize_teams, StorageError,
                     add_learning_unit, add_question, create_round, start_game,
                     game_roster, get_game)


class US10TeamAssignmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "test.sqlite3")
        create_course(self.conn, "A")
        create_course(self.conn, "B")
        self.a = self.conn.execute("SELECT id FROM courses WHERE code='A'").fetchone()[0]
        self.b = self.conn.execute("SELECT id FROM courses WHERE code='B'").fetchone()[0]

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_us10_manual_assignment_changes_only_selected_student(self):
        add_student(self.conn, self.a, "Alpha")
        add_student(self.conn, self.a, "Beta")
        students = list_students(self.conn, self.a)
        chosen = next(s for s in students if s["display_name"] == "Alpha")
        update_student(self.conn, chosen["id"], "Alpha", 2, True)
        actual = {s["display_name"]: s["team"] for s in list_students(self.conn, self.a)}
        self.assertEqual(actual, {"Alpha": 2, "Beta": None})

    def test_us10_random_assignment_balances_odd_number(self):
        for i in range(7):
            add_student(self.conn, self.a, f"Student {i}")
        randomize_teams(self.conn, self.a)
        rows = list_students(self.conn, self.a)
        self.assertEqual({r["team"] for r in rows}, {1, 2})
        self.assertEqual(sorted([sum(r["team"] == t for r in rows) for t in (1, 2)]),
                         [3, 4])

    def test_us10_random_assignment_ignores_inactive_and_other_courses(self):
        for i in range(4):
            add_student(self.conn, self.a, f"Student {i}")
        add_student(self.conn, self.a, "Inactive")
        add_student(self.conn, self.b, "Other", team=2)
        inactive = next(s for s in list_students(self.conn, self.a)
                        if s["display_name"] == "Inactive")
        update_student(self.conn, inactive["id"], "Inactive", None, False)
        randomize_teams(self.conn, self.a)
        active = [s for s in list_students(self.conn, self.a) if s["active"]]
        self.assertEqual(sorted(sum(s["team"] == t for s in active) for t in (1, 2)), [2, 2])
        self.assertIsNone(next(s for s in list_students(self.conn, self.a)
                               if s["display_name"] == "Inactive")["team"])
        self.assertEqual(list_students(self.conn, self.b)[0]["team"], 2)

    def test_us10_random_assignment_rejects_less_than_two_active(self):
        add_student(self.conn, self.a, "Only")
        with self.assertRaises(StorageError) as ctx:
            randomize_teams(self.conn, self.a)
        self.assertEqual(ctx.exception.code, "error.student.need_two")
        self.assertIsNone(list_students(self.conn, self.a)[0]["team"])

    def test_us10_manual_assignment_rejects_invalid_team_without_mutation(self):
        add_student(self.conn, self.a, "Alpha", team=1)
        student = list_students(self.conn, self.a)[0]
        with self.assertRaises(StorageError) as ctx:
            update_student(self.conn, student["id"], "Alpha", 3, True)
        self.assertEqual(ctx.exception.code, "error.student.invalid_team")
        self.assertEqual(list_students(self.conn, self.a)[0]["team"], 1)


    def test_us10_reassignment_does_not_change_running_game_team_snapshots(self):
        """NFANF #02: changing course master data must not rewrite a running game."""
        add_learning_unit(self.conn, "LE1", "Unit", 1)
        unit = self.conn.execute(
            "SELECT id FROM learning_units WHERE code='LE1'"
        ).fetchone()[0]
        questions = []
        for i in range(8):
            add_question(self.conn, unit, f"Question {i}", f"Answer {i}")
            questions.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        rid = create_round(self.conn, "Snapshot round", questions)
        for i in range(8):
            add_student(self.conn, self.a, f"Player {i}", team=1 if i < 4 else 2)
        students = list_students(self.conn, self.a)
        ids = [s["id"] for s in students]
        gid = start_game(self.conn, rid, self.a, ids)
        before = {row["student_id"]: (row["display_name_snapshot"], row["team_snapshot"])
                  for row in game_roster(self.conn, gid)}
        current_before = (get_game(self.conn, gid)["current_student_id"],
                          get_game(self.conn, gid)["current_team"])
        changed = next(s for s in students if s["team"] == 1)
        update_student(self.conn, changed["id"], changed["display_name"], 2, True)
        self.assertEqual(
            self.conn.execute("SELECT team FROM students WHERE id=?",
                              (changed["id"],)).fetchone()[0], 2
        )
        after = {row["student_id"]: (row["display_name_snapshot"], row["team_snapshot"])
                 for row in game_roster(self.conn, gid)}
        self.assertEqual(after, before)
        self.assertEqual(
            (get_game(self.conn, gid)["current_student_id"],
             get_game(self.conn, gid)["current_team"]), current_before
        )


if __name__ == "__main__":
    unittest.main()
