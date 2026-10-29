"""Verify the public project-reference documentation and its internal links."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
ENTRY_POINTS = [
    ROOT / "README.md",
    ROOT / "README.de.md",
    *sorted(DOCS.glob("*.md")),
    DOCS / "archiv" / "README.md",
]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class RequirementsDocumentationTests(unittest.TestCase):
    def test_all_re_reference_links_resolve(self):
        for path in ENTRY_POINTS:
            with self.subTest(source=str(path.relative_to(ROOT))):
                self.assertTrue(path.is_file())
                for target in LINK.findall(path.read_text(encoding="utf-8")):
                    if target.startswith(("http:", "https:", "mailto:", "#")):
                        continue
                    cleaned = target.split("#", 1)[0].split("?", 1)[0]
                    if cleaned:
                        self.assertTrue((path.parent / cleaned).is_file(),
                                        f"Broken link in {path}: {target}")

    def test_project_reference_is_present_without_teaching_examples(self):
        self.assertTrue((DOCS / "Syzeteo-Projektueberblick-DE.md").is_file())
        self.assertTrue((DOCS / "Syzeteo-L-US-DE.md").is_file())
        self.assertTrue((DOCS / "Syzeteo-Use-Cases-US26-DE.md").is_file())
        self.assertTrue((DOCS / "Syzeteo-Traceability-Matrix-DE.md").is_file())
        for retired in (
            "RE-Fallstudie-DE.md",
            "RE-Methodenbeispiel-DE.md",
            "RE-Beispiel-Spiel-abbrechen.bpmn",
        ):
            self.assertFalse((DOCS / retired).exists(),
                             f"Course-only example should be retired: {retired}")

    def test_obsolete_tdd_working_documents_are_not_cited_as_current(self):
        removed_names = (
            "Syzeteo-Akzeptanztests-TDD-DE.md",
            "Syzeteo-TDD-US10-DE.md",
            "Syzeteo-TDD-US21-DE.md",
            "Syzeteo-TDD-Phase2-US24-DE.md",
            "Syzeteo-Testabdeckung-Review-DE.md",
            "Syzeteo-TDD-Kriterien-Governance-DE.md",
            "Syzeteo-TDD-Phase3-Governance-DE.md",
        )
        for path in ENTRY_POINTS:
            content = path.read_text(encoding="utf-8")
            for name in removed_names:
                self.assertNotIn(name, content,
                                 f"Outdated reference in {path}: {name}")


if __name__ == "__main__":
    unittest.main()
