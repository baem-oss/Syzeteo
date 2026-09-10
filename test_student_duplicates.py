import sqlite3
import tempfile
import unittest
from pathlib import Path

from storage import (
    StorageError, add_student, connect, create_course, import_students_csv,
    update_student,
)


class StudentDuplicateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "test.sqlite3")
        create_course(self.conn, "C1", "Course")
        self.course_id = self.conn.execute("SELECT id FROM courses WHERE code='C1'").fetchone()[0]

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_manual_duplicate_raises_localizable_storage_error(self):
        add_student(self.conn, self.course_id, "USER-2")
        with self.assertRaises(StorageError) as ctx:
            add_student(self.conn, self.course_id, "USER-2")
        self.assertEqual(ctx.exception.code, "error.student.name_exists")
        self.assertEqual(ctx.exception.params, {"name": "USER-2"})

    def test_duplicate_name_is_allowed_in_different_course(self):
        add_student(self.conn, self.course_id, "USER-2")
        create_course(self.conn, "C2", "Course 2")
        other = self.conn.execute("SELECT id FROM courses WHERE code='C2'").fetchone()[0]
        add_student(self.conn, other, "USER-2")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM students WHERE display_name='USER-2'").fetchone()[0], 2)

    def test_rename_to_existing_name_raises_same_storage_error(self):
        add_student(self.conn, self.course_id, "USER-1")
        add_student(self.conn, self.course_id, "USER-2")
        sid = self.conn.execute("SELECT id FROM students WHERE course_id=? AND display_name='USER-1'", (self.course_id,)).fetchone()[0]
        with self.assertRaises(StorageError) as ctx:
            update_student(self.conn, sid, "USER-2", None, True)
        self.assertEqual(ctx.exception.code, "error.student.name_exists")
        self.assertEqual(ctx.exception.params, {"name": "USER-2"})
        self.assertEqual(self.conn.execute("SELECT display_name FROM students WHERE id=?", (sid,)).fetchone()[0], "USER-1")

    def test_csv_import_still_skips_duplicate_names(self):
        add_student(self.conn, self.course_id, "USER-2")
        raw = b"name\nUSER-2\nUSER-3\n"
        imported, skipped = import_students_csv(self.conn, self.course_id, raw)
        self.assertEqual((imported, skipped), (1, 1))
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM students WHERE course_id=?", (self.course_id,)).fetchone()[0], 2)


if __name__ == "__main__":
    unittest.main()
