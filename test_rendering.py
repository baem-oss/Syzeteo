import unittest

from rendering import escape_markdown_literal, plain_text_html, round_question_html


class RenderingTest(unittest.TestCase):
    def test_numbered_lines_are_escaped_for_markdown_capable_card_labels(self):
        source = (
            "6. LE10 – Gegeben ist folgender Ausschnitt\n"
            "7. Der Mitarbeiter prüft die Kundenstammdaten.\n"
            "8. Das System prüft den Auftrag."
        )
        rendered = escape_markdown_literal(source)
        self.assertIn("6\\. LE10", rendered)
        self.assertIn("7\\. Der Mitarbeiter", rendered)
        self.assertIn("8\\. Das System", rendered)
        self.assertNotIn("\n7. Der Mitarbeiter", rendered)

    def test_markdown_syntax_in_question_content_is_neutralized(self):
        source = "# Titel\n- Punkt\n*Betonung*\n> Zitat"
        rendered = escape_markdown_literal(source)
        self.assertEqual(rendered, "\\# Titel\n\\- Punkt\n\\*Betonung\\*\n\\> Zitat")

    def test_plain_multiline_html_escapes_markup_and_preserves_literal_content(self):
        source = "7. Zeile\n<script>alert('x')</script>"
        rendered = plain_text_html(source)
        self.assertIn("white-space: pre-wrap", rendered)
        self.assertIn("7. Zeile\n", rendered)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_opened_question_renderer_bypasses_streamlit_markdown(self):
        from pathlib import Path
        app_source = Path(__file__).with_name("app.py").read_text(encoding="utf-8")
        self.assertIn("st.html(plain_text_html(text))", app_source)
        self.assertNotIn("st.markdown(plain_text_html(text)", app_source)

    def test_round_overview_keeps_outer_position_and_inner_numbered_lines_literal(self):
        source = (
            "Gegeben ist: UC #011 Kundendaten bestätigen\n"
            "2. Der Kunde gibt seine Kundennummer ein.\n"
            "3. Das System zeigt die Kundendaten an."
        )
        rendered = round_question_html(1, "LE10", source)
        self.assertIn("1. <strong>LE10</strong> – Gegeben ist:", rendered)
        self.assertIn("\n2. Der Kunde gibt", rendered)
        self.assertIn("\n3. Das System zeigt", rendered)
        self.assertNotIn("<ol", rendered)
        self.assertNotIn("<li", rendered)

    def test_round_overview_does_not_use_markdown_capable_write_for_question_text(self):
        from pathlib import Path
        app_source = Path(__file__).with_name("app.py").read_text(encoding="utf-8")
        self.assertIn('st.html(round_question_html(item["position"], item["unit_code"], item["question_text"]))', app_source)
        self.assertNotIn('st.write(f"{item[\'position\']}. **{item[\'unit_code\']}** – {item[\'question_text\']}")', app_source)


if __name__ == "__main__":
    unittest.main()
