from pathlib import Path

APP = Path("app.py")
source = APP.read_text(encoding="utf-8")

source = source.replace('APP_VERSION = "1.1.0-dev1"', 'APP_VERSION = "1.1.0"', 1)

needle = '''st.sidebar.title(tr("app.title"))
st.sidebar.caption(tr("app.tagline"))
PAGE=st.sidebar.radio(
'''
replacement = '''st.sidebar.title(tr("app.title"))
st.sidebar.caption(tr("app.tagline"))

# Programmatic navigation must be applied before the widget with key
# "page_nav" is instantiated in the current Streamlit run.
_pending_page_nav = st.session_state.pop("_pending_page_nav", None)
if _pending_page_nav in PAGE_IDS:
    st.session_state["page_nav"] = _pending_page_nav

PAGE=st.sidebar.radio(
'''
if needle in source:
    source = source.replace(needle, replacement, 1)
elif 'st.session_state["page_nav"] = _pending_page_nav' not in source:
    raise RuntimeError("navigation insertion point not found")

old_nav = '''def navigate(page, game_id=None, clear_finished=False):
    st.session_state.page_nav=page
'''
new_nav = '''def navigate(page, game_id=None, clear_finished=False):
    st.session_state["_pending_page_nav"]=page
'''
if old_nav in source:
    source = source.replace(old_nav, new_nav, 1)
elif 'st.session_state["_pending_page_nav"]=page' not in source:
    raise RuntimeError("navigate() patch point not found")

source = source.replace(
    '                    st.session_state.page_nav=PAGE_INSTRUCTOR_SETTINGS\n',
    '                    st.session_state["_pending_page_nav"]=PAGE_INSTRUCTOR_SETTINGS\n',
    1,
)

if 'APP_VERSION = "1.1.0"' not in source:
    raise RuntimeError("release version not set")
if "st.session_state.page_nav=" in source:
    raise RuntimeError("direct page_nav mutation remains")
if source.index('st.session_state["page_nav"] = _pending_page_nav') > source.index('PAGE=st.sidebar.radio('):
    raise RuntimeError("pending navigation is applied too late")

APP.write_text(source, encoding="utf-8")

Path("test_navigation.py").write_text('''import unittest
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
''', encoding="utf-8")
