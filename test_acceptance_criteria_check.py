"""Contract tests for incremental acceptance-criterion traceability."""
import json
import tempfile
import unittest
from pathlib import Path
from acceptance_criteria_check import check


class AcceptanceCriteriaGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()
        (self.root / "test_example.py").write_text(
            "def test_old(): pass\ndef test_new(): assert 1 == 1\n", encoding="utf-8")
        self.original = {"id": "AC-US01-01", "story_id": 1,
                         "statement": "Given A, when B, then C",
                         "status": "legacy_provisional", "manual_review": False,
                         "test_references": ["test_example.py::test_old"]}
        self.active = [json.loads(json.dumps(self.original))]
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        files = {
            "Syzeteo-Akzeptanzkriterien.json": {"criteria": self.active},
            "Syzeteo-Akzeptanzkriterien-Baseline.json": {"criteria": [self.original]},
            "Syzeteo-Akzeptanztests-Mapping.json": {"stories": [{"id": 1}]}
        }
        for name, payload in files.items():
            (self.root / "docs" / name).write_text(json.dumps(payload), encoding="utf-8")

    def test_unchanged_legacy_is_allowed(self):
        self.assertEqual(check(self.root), [])

    def test_changed_statement_without_new_evidence_is_blocked(self):
        self.active[0]["statement"] = "Changed"
        self.save()
        self.assertTrue(check(self.root))

    def test_changed_statement_with_new_evidence_is_allowed(self):
        self.active[0]["statement"] = "Changed"
        self.active[0]["test_references"].append("test_example.py::test_new")
        self.save()
        self.assertEqual(check(self.root), [])

    def test_new_criterion_without_evidence_is_blocked(self):
        self.active.append({"id": "AC-US01-02", "story_id": 1,
                            "statement": "New criterion", "test_references": []})
        self.save()
        self.assertTrue(check(self.root))

    def test_new_criterion_with_existing_test_is_accepted_as_new_mapping(self):
        self.active.append({"id": "AC-US01-02", "story_id": 1,
                            "statement": "New criterion",
                            "test_references": ["test_example.py::test_new"]})
        self.save()
        self.assertEqual(check(self.root), [])

    def test_duplicate_criterion_id_is_rejected(self):
        self.active.append(dict(self.original))
        self.save()
        self.assertTrue(check(self.root))

    def test_removed_criterion_is_rejected(self):
        self.active = []
        self.save()
        self.assertTrue(check(self.root))

    def test_nonexistent_test_is_rejected(self):
        self.active[0]["test_references"] = ["test_example.py::test_missing"]
        self.save()
        self.assertTrue(check(self.root))

    def test_wrong_story_id_is_rejected(self):
        self.active[0]["story_id"] = 2
        self.save()
        self.assertTrue(check(self.root))


if __name__ == "__main__":
    unittest.main()
