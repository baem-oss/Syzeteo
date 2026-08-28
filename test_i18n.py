import ast
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import i18n
from storage import connect, get_app_setting, set_app_setting


class I18nTest(unittest.TestCase):
    def setUp(self):
        i18n.load_catalog.cache_clear()

    def test_i18n_t01_catalogs_are_valid_utf8_json(self):
        root = Path(__file__).resolve().parent / "locales"
        for path in root.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertIsInstance(data, dict)
            self.assertTrue(all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()))

    def test_i18n_t02_t03_official_catalogs_have_same_keys(self):
        en = i18n.load_catalog("en")
        de = i18n.load_catalog("de")
        self.assertEqual(set(en), set(de))
        self.assertEqual(i18n.validate_catalogs(), [])

    def test_i18n_t04_placeholders_must_match(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "en.json").write_text('{"language.name":"English","x":"Course {code}"}', encoding="utf-8")
            (root / "de.json").write_text('{"language.name":"Deutsch","x":"Kurs {course}"}', encoding="utf-8")
            with patch.object(i18n, "LOCALES_DIR", root):
                i18n.load_catalog.cache_clear()
                errors = i18n.validate_catalogs()
            self.assertTrue(any("placeholder mismatch" in item for item in errors))

    def test_i18n_t05_missing_language_key_falls_back_to_english(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "en.json").write_text('{"language.name":"English","x":"English text"}', encoding="utf-8")
            (root / "fr.json").write_text('{"language.name":"Français"}', encoding="utf-8")
            with patch.object(i18n, "LOCALES_DIR", root):
                i18n.load_catalog.cache_clear()
                self.assertEqual(i18n.t("x", locale="fr"), "English text")

    def test_i18n_unknown_locale_falls_back_to_english(self):
        self.assertEqual(i18n.t("nav.dashboard", locale="xx"), "Dashboard")

    def test_i18n_unknown_key_is_visible_and_strict_mode_fails(self):
        self.assertEqual(i18n.t("missing.key", locale="en"), "missing.key")
        with self.assertRaises(i18n.I18nError):
            i18n.t("missing.key", locale="en", strict=True)

    def test_i18n_navigation_uses_stable_ids(self):
        source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        for legacy_control in (
            'PAGE=="Übersicht"', 'PAGE=="Kurse"', 'PAGE=="Studierende & Teams"',
            'PAGE=="Lerneinheiten"', 'PAGE=="Fragenpool"', 'PAGE=="Import / Export"',
            'PAGE=="Runden"', 'PAGE=="Spiel"', 'PAGE=="Fragenprotokoll"',
            'PAGE=="Instructor Settings"', 'PAGE=="Account"',
        ):
            self.assertNotIn(legacy_control, source)
        for stable_id in (
            'PAGE_DASHBOARD = "dashboard"', 'PAGE_COURSES = "courses"',
            'PAGE_STUDENTS = "students"', 'PAGE_GAME = "game"',
            'PAGE_INSTRUCTOR_SETTINGS = "instructor_settings"',
        ):
            self.assertIn(stable_id, source)

    def test_i18n_configuration_issue_actions_use_page_ids(self):
        source = (Path(__file__).resolve().parent / "storage.py").read_text(encoding="utf-8")
        for page_id in ('"students"', '"learning_units"', '"question_pool"', '"rounds"', '"game"'):
            self.assertIn(page_id, source)

    def test_i18n_language_selection_is_only_login_and_instructor_settings(self):
        source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        self.assertIn('locale_selector("login")', source)
        self.assertIn('locale_selector("instructor_settings", persist=True)', source)
        self.assertNotIn('locale_selector("sidebar")', source)
        self.assertNotIn('locale_selector("account")', source)

    def test_i18n_persistent_locale_setting_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            conn = connect(Path(td) / "test.sqlite3")
            self.assertIsNone(get_app_setting(conn, "ui_locale"))
            set_app_setting(conn, "ui_locale", "de")
            self.assertEqual(get_app_setting(conn, "ui_locale"), "de")
            conn.close()

    def test_i18n_dashboard_first_page_has_no_known_german_ui_literals(self):
        source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        block = source.split("if PAGE==PAGE_DASHBOARD:", 1)[1].split("elif PAGE==PAGE_COURSES:", 1)[0]
        for literal in (
            "Noch keine Kurse angelegt.", "Gespielte Runden", "Aktuelle Führung",
            "Laufendes Spiel fortsetzen", "Spielhistorie", "Noch keine Spiele vorhanden.",
            "Rundenergebnisse als Tabelle", "Alle Kurse im Überblick",
        ):
            self.assertNotIn(literal, block)
        self.assertIn('tr("dashboard.no_courses")', block)
        self.assertIn('tr("dashboard.game_history")', block)

    def test_i18n_courses_page_has_no_known_german_ui_literals(self):
        source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        block = source.split("elif PAGE==PAGE_COURSES:", 1)[1].split("elif PAGE==PAGE_STUDENTS:", 1)[0]
        for literal in (
            'st.title("Kurse")', '"Kurskürzel"', '"Kurs anlegen"', '"Aktive Kurse"',
            '"Kurs archivieren"', '"Archivierte Kurse anzeigen', '"Kurs reaktivieren"',
            '"Kurs löschen"', '"Zu löschender Kurs"', '"Kurs endgültig löschen"',
            '"Keine archivierten Kurse vorhanden."',
        ):
            self.assertNotIn(literal, block)
        for key in (
            'courses.title', 'courses.create', 'courses.archive.button',
            'courses.reactivate.button', 'courses.delete.button',
        ):
            self.assertIn(f'tr("{key}"', block)

    def test_i18n_course_storage_errors_have_translations(self):
        for locale in ("en", "de"):
            for key in (
                "course.error.code_required", "course.error.code_exists",
                "course.error.not_found", "course.error.running_game",
            ):
                self.assertNotEqual(i18n.t(key, locale=locale, code="DEMO"), key)

    def test_i18n_all_remaining_pages_have_no_known_german_ui_literals(self):
        source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        ui_source = source.replace("/* Anwesenheitscheck: bis zu ca. 15 Namen ohne internes Scrollen sichtbar. */", "")
        forbidden = (
            'st.title("Studierende & Teams")', '"Zuerst einen Kurs anlegen."',
            'st.title("Lerneinheiten")', '"Globaler Fragenpool"',
            'st.title("Runden")', 'st.title("Spiel")', '"Anwesenheitscheck"',
            '"Startspieler"', '"Zufällige Spielerwahl"', '"Manuelle Spielerwahl"',
            '"Musterantwort"', 'st.title("Fragenprotokoll")',
            '"Kursübergreifende Abdeckung"', '"Zentrale Übersicht und Steuerung',
            '"Systemstatus"', '"Angemeldet als **', '"Bisheriges Passwort"',
        )
        for literal in forbidden:
            self.assertNotIn(literal, ui_source)

    def test_i18n_configuration_issue_catalog_keys_are_translated(self):
        keys = (
            "config.issue.db.title", "config.issue.course_empty.title",
            "config.issue.unassigned.title", "config.issue.no_unit.title",
            "config.issue.unit_no_questions.title", "config.issue.round_incomplete.title",
            "config.issue.no_playable_round.title", "config.issue.running.title",
            "config.action.students", "config.action.game",
        )
        for locale in ("en", "de"):
            for key in keys:
                self.assertNotEqual(i18n.t(key, locale=locale, code="DEMO", count=1, name="Round 1", round_name="Round 1", course_code="DEMO", status="ok"), key)

    def test_i18n_storage_domain_errors_are_translated(self):
        keys = (
            "error.student.name_required", "error.learning_unit.required",
            "error.question.text_required", "error.import.invalid_json",
            "error.round.exact_eight", "error.game.need_four",
            "error.card.unavailable", "error.assist.used", "error.game.next_unavailable",
        )
        for locale in ("en", "de"):
            for key in keys:
                self.assertNotEqual(i18n.t(key, locale=locale), key)


    def test_i18n_all_literal_translation_keys_exist_in_english_catalog(self):
        catalog = i18n.load_catalog("en")
        source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        keys = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "tr" and node.args:
                arg = node.args[0]
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    keys.add(arg.value)
        missing = sorted(key for key in keys if key not in catalog)
        self.assertEqual(missing, [])

    def test_i18n_all_literal_storage_error_keys_exist_in_catalog(self):
        catalog = i18n.load_catalog("en")
        source = (Path(__file__).resolve().parent / "storage.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        keys = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "StorageError" and node.args:
                arg = node.args[0]
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    keys.add(arg.value)
        missing = sorted(key for key in keys if key not in catalog)
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
