import unittest
from pathlib import Path


class RoundSelectionUiTest(unittest.TestCase):
    def test_round_multiselects_do_not_use_streamlit_max_selections_overlay(self):
        app = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        self.assertIn('st.multiselect(tr("rounds.select_eight"),list(new_round_qopts))', app)
        self.assertIn('st.multiselect(tr("rounds.change_questions"),list(edit_qopts),default=selected_labels)', app)
        self.assertNotIn('tr("rounds.select_eight"),list(new_round_qopts),max_selections=8', app)
        self.assertNotIn('tr("rounds.change_questions"),list(edit_qopts),default=selected_labels,max_selections=8', app)

    def test_exact_eight_remains_a_domain_rule(self):
        storage = (Path(__file__).resolve().parent / "storage.py").read_text(encoding="utf-8")
        self.assertGreaterEqual(storage.count('raise StorageError("error.round.exact_eight")'), 3)


if __name__ == "__main__":
    unittest.main()
