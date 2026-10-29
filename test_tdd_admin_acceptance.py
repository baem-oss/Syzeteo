"""Phase-2 acceptance assertions for US #05–#09: instructor administration.

Tests use isolated in-memory authentication and temporary SQLite application
databases. No productive datasets or credentials are used.
"""
import sqlite3
import tempfile
import unittest
from pathlib import Path

from auth import create_admin, authenticate, change_password, change_username
from storage import (
    StorageError, connect, create_course, archive_course, reactivate_course,
    delete_course, add_student, update_student, list_students,
    add_learning_unit, add_question, create_round, start_game,
    game_cards, import_students_csv,
)


class InstructorAccountAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row

    def tearDown(self):
        self.conn.close()

    def test_us05_login_accepts_valid_credentials_and_rejects_invalid_password(self):
        ok, _ = create_admin(self.conn, "Instructor", "long-password-1234", "long-password-1234")
        self.assertTrue(ok)
        self.assertFalse(authenticate(self.conn, "instructor", "incorrect-password")[0])
        ok, key, display = authenticate(self.conn, "INSTRUCTOR", "long-password-1234")
        self.assertTrue(ok)
        self.assertEqual(key, "auth.ok")
        self.assertEqual(display, "Instructor")
        self.assertIsNotNone(
            self.conn.execute("SELECT last_login_at FROM users").fetchone()[0]
        )

    def test_us06_changing_username_and_password_invalidates_previous_credentials(self):
        self.assertTrue(create_admin(self.conn, "Instructor", "old-password-1234", "old-password-1234")[0])
        ok, _, renamed = change_username(
            self.conn, "Instructor", "old-password-1234", "NewInstructor"
        )
        self.assertTrue(ok)
        self.assertEqual(renamed, "NewInstructor")
        self.assertFalse(authenticate(self.conn, "Instructor", "old-password-1234")[0])
        self.assertTrue(change_password(
            self.conn, "NewInstructor", "old-password-1234",
            "new-password-5678", "new-password-5678"
        )[0])
        self.assertFalse(authenticate(self.conn, "NewInstructor", "old-password-1234")[0])
        self.assertTrue(authenticate(self.conn, "newinstructor", "new-password-5678")[0])

    def test_us06_wrong_old_password_does_not_modify_login_credentials(self):
        self.assertTrue(create_admin(self.conn, "Admin", "old-password-1234", "old-password-1234")[0])
        ok, key = change_password(
            self.conn, "Admin", "wrong-password", "new-password-5678", "new-password-5678"
        )
        self.assertFalse(ok)
        self.assertEqual(key, "auth.error.old_password_wrong")
        self.assertTrue(authenticate(self.conn, "Admin", "old-password-1234")[0])
        self.assertFalse(authenticate(self.conn, "Admin", "new-password-5678")[0])


class CourseAndStudentAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "acceptance.sqlite3")
        create_course(self.conn, "A", "Course A")
        create_course(self.conn, "B", "Course B")
        self.a = self.conn.execute("SELECT id FROM courses WHERE code='A'").fetchone()[0]
        self.b = self.conn.execute("SELECT id FROM courses WHERE code='B'").fetchone()[0]

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_us07_deleting_course_removes_games_students_and_history_but_keeps_global_pool(self):
        add_learning_unit(self.conn, "LE1", "Global unit", 1)
        uid = self.conn.execute("SELECT id FROM learning_units WHERE code='LE1'").fetchone()[0]
        questions = []
        for n in range(8):
            add_question(self.conn, uid, f"Question {n}", f"Answer {n}")
            questions.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        rid = create_round(self.conn, "Shared round", questions)
        for n in range(8):
            add_student(self.conn, self.a, f"Student {n}", team=1 if n < 4 else 2)
        add_student(self.conn, self.b, "Student in other course", team=1)
        present = [r["id"] for r in list_students(self.conn, self.a)]
        game_id = start_game(self.conn, rid, self.a, present)
        self.assertEqual(len(game_cards(self.conn, game_id)), 9)
        delete_course(self.conn, self.a)
        self.assertEqual(self.conn.execute(
            "SELECT COUNT(*) FROM courses WHERE id=?", (self.a,)
        ).fetchone()[0], 0)
        for table, column in (("students", "course_id"), ("games", "course_id")):
            self.assertEqual(self.conn.execute(
                f"SELECT COUNT(*) FROM {table} WHERE {column}=?", (self.a,)
            ).fetchone()[0], 0)
        self.assertEqual(self.conn.execute(
            "SELECT COUNT(*) FROM game_cards WHERE game_id=?", (game_id,)
        ).fetchone()[0], 0)
        self.assertEqual(self.conn.execute(
            "SELECT COUNT(*) FROM game_roster WHERE game_id=?", (game_id,)
        ).fetchone()[0], 0)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0], 8)
        self.assertEqual(self.conn.execute(
            "SELECT COUNT(*) FROM round_questions WHERE round_id=?", (rid,)
        ).fetchone()[0], 8)
        self.assertEqual(self.conn.execute(
            "SELECT COUNT(*) FROM students WHERE course_id=?", (self.b,)
        ).fetchone()[0], 1)

    def test_us07_archiving_and_reactivating_preserves_course_students(self):
        add_student(self.conn, self.a, "Student A")
        archive_course(self.conn, self.a)
        self.assertEqual(
            self.conn.execute("SELECT active FROM courses WHERE id=?", (self.a,)).fetchone()[0],
            0
        )
        self.assertEqual(len(list_students(self.conn, self.a)), 1)
        reactivate_course(self.conn, self.a)
        self.assertEqual(
            self.conn.execute("SELECT active FROM courses WHERE id=?", (self.a,)).fetchone()[0],
            1
        )
        self.assertEqual(len(list_students(self.conn, self.a)), 1)

    def test_us08_update_student_and_active_status_only_affects_selected_course_member(self):
        add_student(self.conn, self.a, "First", team=1)
        add_student(self.conn, self.a, "Second", team=2)
        add_student(self.conn, self.b, "Other", team=1)
        selected = next(s for s in list_students(self.conn, self.a)
                        if s["display_name"] == "First")
        update_student(self.conn, selected["id"], "First Updated", 2, False)
        first = next(s for s in list_students(self.conn, self.a)
                     if s["id"] == selected["id"])
        self.assertEqual(
            (first["display_name"], first["team"], first["active"]),
            ("First Updated", 2, 0)
        )
        self.assertEqual([s["display_name"] for s in list_students(
            self.conn, self.a, active_only=True)], ["Second"])
        self.assertEqual(
            [(s["display_name"], s["team"], s["active"]) for s in list_students(self.conn, self.b)],
            [("Other", 1, 1)]
        )

    def test_us09_csv_import_accepts_bom_and_semicolon_names_and_skips_duplicates(self):
        add_student(self.conn, self.a, "Ada Lovelace")
        raw = ("Vorname;Nachname\nAda;Lovelace\nGrace;Hopper\n").encode("utf-8-sig")
        imported, skipped = import_students_csv(self.conn, self.a, raw)
        self.assertEqual((imported, skipped), (1, 1))
        students = {s["display_name"]: s for s in list_students(self.conn, self.a)}
        self.assertEqual(set(students), {"Ada Lovelace", "Grace Hopper"})
        self.assertEqual((students["Grace Hopper"]["first_name"],
                          students["Grace Hopper"]["last_name"]), ("Grace", "Hopper"))
        self.assertEqual(list_students(self.conn, self.b), [])

    def test_us09_csv_import_rejects_missing_name_columns(self):
        with self.assertRaises(StorageError) as ctx:
            import_students_csv(self.conn, self.a, b"matriculation;course\n123;A\n")
        self.assertEqual(ctx.exception.code, "error.student.csv_columns")
        self.assertEqual(list_students(self.conn, self.a), [])


if __name__ == "__main__":
    unittest.main()
