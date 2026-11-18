import tempfile
import unittest
from pathlib import Path

from storage import (
    StorageError, add_learning_unit, add_question, add_student, connect,
    create_course, create_round, export_played_round_txt, randomize_teams,
    start_game,
)


class ExportPlayedRoundTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tempdir.name) / "existing.sqlite3")
        create_course(self.conn, "WIBE-TEST")
        self.course_id = self.conn.execute("SELECT id FROM courses WHERE code='WIBE-TEST'").fetchone()[0]
        add_learning_unit(self.conn, "LE-TEST", "Learning unit", 1)
        unit_id = self.conn.execute("SELECT id FROM learning_units WHERE code='LE-TEST'").fetchone()[0]
        question_ids = []
        for i in range(8):
            add_question(self.conn, unit_id, f"Frage {i + 1}: äöü?", f"Geheime Lösung {i + 1}")
            question_ids.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        self.round_id = create_round(self.conn, "Prüfungsrunde Ä", question_ids)
        for i in range(8):
            add_student(self.conn, self.course_id, f"Student {i + 1}")
        randomize_teams(self.conn, self.course_id)
        roster = [r["id"] for r in self.conn.execute("SELECT id FROM students ORDER BY id")]
        self.game_id = start_game(self.conn, self.round_id, self.course_id, roster)

    def tearDown(self):
        self.conn.close()
        self.tempdir.cleanup()

    def test_no_export_before_game_finished(self):
        with self.assertRaises(StorageError) as ctx:
            export_played_round_txt(self.conn, self.round_id)
        self.assertEqual(ctx.exception.code, "error.round.export_unavailable")

    def test_finished_export_is_utf8_ordered_private_and_read_only(self):
        self.conn.execute("UPDATE games SET status='finished' WHERE id=?", (self.game_id,))
        self.conn.commit()
        before = self.conn.total_changes
        first = export_played_round_txt(self.conn, self.round_id)
        self.assertEqual(first, export_played_round_txt(self.conn, self.round_id))
        self.assertEqual(self.conn.total_changes, before)
        result = first.decode("utf-8")
        self.assertTrue(result.startswith("Runde: Prüfungsrunde Ä\n\n"))
        self.assertEqual(result.count("Frage "), 8)
        self.assertLess(result.index("1. Frage 1"), result.index("8. Frage 8"))
        for forbidden in ("Geheime Lösung", "Challenge", "BäM", "Student", "Punkte"):
            self.assertNotIn(forbidden, result)

    def test_export_uses_immutable_snapshot(self):
        self.conn.execute("UPDATE games SET status='finished' WHERE id=?", (self.game_id,))
        self.conn.execute("UPDATE questions SET question_text='Nachträglich geändert'")
        self.conn.commit()
        result = export_played_round_txt(self.conn, self.round_id).decode("utf-8")
        self.assertIn("Frage 1: äöü?", result)
        self.assertNotIn("Nachträglich geändert", result)


if __name__ == "__main__":
    unittest.main()
