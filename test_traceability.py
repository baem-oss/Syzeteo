"""Tests for incremental requirements-to-tests gate."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class TraceabilityGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="syzeteo-tdd-")
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()
        shutil.copyfile(ROOT / "traceability_check.py", self.root / "traceability_check.py")
        (self.root / "test_example.py").write_text(
            "def test_existing(): pass\ndef test_new(): pass\n", encoding="utf-8"
        )
        self.baseline = {
            "stories": [{"id": 1, "title": "Old", "description": "Als User möchte ich Old.",
                         "test_references": ["test_example.py::test_existing"]}]
        }
        self.mapping = {
            "stories": [{"id": 1, "criterion": "AC-US01-01",
                         "test_references": ["test_example.py::test_existing"]}]
        }
        self.write()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, story="Old", detail="Als User möchte ich Old."):
        (self.root / "docs" / "Syzeteo-L-US-DE.md").write_text(
            f"# Stories\n\n- [x] **US #01 – {story}**  \n  {detail}\n", encoding="utf-8"
        )
        for name, obj in (("Syzeteo-TDD-Baseline.json", self.baseline),
                          ("Syzeteo-Akzeptanztests-Mapping.json", self.mapping)):
            (self.root / "docs" / name).write_text(json.dumps(obj), encoding="utf-8")

    def run_gate(self):
        return subprocess.run(
            [sys.executable, str(self.root / "traceability_check.py")],
            cwd=self.root, text=True, capture_output=True, check=False
        )

    def test_legacy_mapping_is_allowed(self):
        self.assertEqual(self.run_gate().returncode, 0)

    def test_changed_story_without_new_test_is_blocked(self):
        self.write(story="Changed")
        self.assertNotEqual(self.run_gate().returncode, 0)

    def test_changed_story_with_new_test_is_allowed(self):
        self.mapping["stories"][0]["test_references"].append("test_example.py::test_new")
        self.write(story="Changed")
        self.assertEqual(self.run_gate().returncode, 0)

    def test_unknown_test_method_is_blocked(self):
        self.mapping["stories"][0]["test_references"] = ["test_example.py::test_missing"]
        self.write()
        self.assertNotEqual(self.run_gate().returncode, 0)

    def test_new_story_without_mapping_is_blocked(self):
        story_path = self.root / "docs" / "Syzeteo-L-US-DE.md"
        story_path.write_text(story_path.read_text(encoding="utf-8") +
                              "\n- [x] **US #02 – New**\n  Als User möchte ich New.\n",
                              encoding="utf-8")
        self.assertNotEqual(self.run_gate().returncode, 0)


if __name__ == "__main__":
    unittest.main()
