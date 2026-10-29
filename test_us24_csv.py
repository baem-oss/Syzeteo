"""US #24: CSV export must match the filtered question-log table."""
import unittest
import pandas as pd

from question_protocol import filter_protocol_table, export_protocol_csv


class US24CSVAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.table = pd.DataFrame([
            {"Kurs": "A", "Runde": "R1", "Frage": "Alpha", "Position": 1},
            {"Kurs": "A", "Runde": "R2", "Frage": "Beta, mit Komma", "Position": 2},
            {"Kurs": "B", "Runde": "R1", "Frage": "Zeile 1\nZeile 2", "Position": 3},
        ])

    def test_us24_csv_contains_only_course_and_round_filtered_rows(self):
        view = filter_protocol_table(self.table, "Kurs", "Runde", ["A"], ["R2"])
        csv_bytes = export_protocol_csv(view)
        self.assertTrue(csv_bytes.startswith(b"\xef\xbb\xbf"))
        imported = pd.read_csv(__import__("io").BytesIO(csv_bytes))
        self.assertEqual(imported.to_dict("records"), [
            {"Kurs": "A", "Runde": "R2", "Frage": "Beta, mit Komma", "Position": 2}
        ])

    def test_us24_csv_without_filters_preserves_all_rows_and_text(self):
        view = filter_protocol_table(self.table, "Kurs", "Runde")
        imported = pd.read_csv(__import__("io").BytesIO(export_protocol_csv(view)))
        self.assertEqual(imported.to_dict("records"), self.table.to_dict("records"))

    def test_us24_filtered_empty_result_exports_header_only(self):
        view = filter_protocol_table(self.table, "Kurs", "Runde", ["nicht vorhanden"])
        imported = pd.read_csv(__import__("io").BytesIO(export_protocol_csv(view)))
        self.assertEqual(list(imported.columns), list(self.table.columns))
        self.assertEqual(len(imported), 0)


if __name__ == "__main__":
    unittest.main()
