import unittest
from pathlib import Path


class NavigationStateRegressionTest(unittest.TestCase):
    def test_programmatic_page_navigation_is_deferred_until_before_widget_creation(self):
        source = (Path(__file__).parent / "app.py").read_text(encoding="utf-8")
        radio_pos = source.index('PAGE=st.sidebar.radio(')
        apply_pos = source.index('st.session_state["page_nav"] = _pending_page_nav')
        self.assertLess(apply_pos, radio_pos)
        self.assertNotIn("st.session_state.page_nav=", source)
        self.assertIn('st.session_state["_pending_page_nav"]=PAGE_INSTRUCTOR_SETTINGS', source)


if __name__ == "__main__":
    unittest.main()
