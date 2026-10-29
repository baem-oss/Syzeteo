"""Contract tests for stable acceptance criteria, mapping and assertion integrity."""
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
            "def test_old(): assert 3 == 3\n"
            "def test_new(): assert 2 == 2\n"
            "def test_no_assert(): pass\n", encoding="utf-8"
        )
        self.original = {
            "id": "AC-US01-01", "story_id": 1,
            "statement": "Given A, when B, then C",
            "status": "legacy_provisional", "manual_review": False,
            "test_references": ["test_example.py::test_old"]
        }
        self.active = [json.loads(json.dumps(self.original))]
        self.mapping_override = None
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        refs = list(dict.fromkeys(ref for c in self.active for ref in c["test_references"]))
        mapping = {
            "id": 1, "criterion": "AC-US01-01",
            "criteria": [c["id"] for c in self.active],
            "test_references": refs
        }
        files = {
            "Syzeteo-Akzeptanzkriterien.json": {"criteria": self.active},
            "Syzeteo-Akzeptanzkriterien-Baseline.json": {"criteria": [self.original]},
            "Syzeteo-Akzeptanztests-Mapping.json": {
                "stories": [self.mapping_override if self.mapping_override else mapping]
            }
        }
        for name, payload in files.items():
            (self.root / "docs" / name).write_text(
                json.dumps(payload), encoding="utf-8"
            )

    def test_unchanged_legacy_is_allowed(self):
        self.assertEqual(check(self.root), [])

    def test_changed_statement_without_new_evidence_is_blocked(self):
        self.active[0]["statement"] = "Changed"
        self.save()
        self.assertTrue(any("new test reference" in x for x in check(self.root)))

    def test_changed_statement_with_new_evidence_is_allowed(self):
        self.active[0]["statement"] = "Changed"
        self.active[0]["test_references"].append("test_example.py::test_new")
        self.save()
        self.assertEqual(check(self.root), [])

    def test_new_criterion_without_evidence_is_blocked(self):
        self.active.append({
            "id": "AC-US01-02", "story_id": 1, "statement": "New criterion",
            "status": "specified_partial", "manual_review": False,
            "test_references": []
        })
        self.save()
        self.assertTrue(any("new test reference" in x for x in check(self.root)))

    def test_new_criterion_with_existing_test_is_accepted_as_new_mapping(self):
        # The separate PR gate will require changes to the actual test's assertions.
        self.active.append({
            "id": "AC-US01-02", "story_id": 1, "statement": "New criterion",
            "status": "specified_partial", "manual_review": False,
            "test_references": ["test_example.py::test_new"]
        })
        self.save()
        self.assertEqual(check(self.root), [])

    def test_duplicate_criterion_id_is_rejected(self):
        self.active.append(json.loads(json.dumps(self.original)))
        self.save()
        self.assertTrue(check(self.root))

    def test_removed_criterion_is_rejected(self):
        self.active = []
        self.save()
        self.assertTrue(check(self.root))

    def test_nonexistent_test_is_rejected(self):
        self.active[0]["test_references"] = ["test_example.py::test_missing"]
        self.save()
        self.assertTrue(any("invalid reference" in x for x in check(self.root)))

    def test_wrong_story_id_is_rejected(self):
        self.active[0]["story_id"] = 2
        self.save()
        self.assertTrue(any("mismatched story" in x for x in check(self.root)))

    def test_method_without_assertions_is_blocked(self):
        self.active[0]["test_references"] = ["test_example.py::test_no_assert"]
        self.save()
        self.assertTrue(any("contains no direct assertions" in x for x in check(self.root)))

    def test_missing_criterion_story_link_is_blocked(self):
        self.mapping_override = {
            "id": 1, "criterion": "AC-US01-01", "criteria": [],
            "test_references": ["test_example.py::test_old"]
        }
        self.save()
        self.assertTrue(any("criteria mapping differs" in x for x in check(self.root)))

    def test_unmapped_criterion_test_is_blocked(self):
        self.mapping_override = {
            "id": 1, "criterion": "AC-US01-01", "criteria": ["AC-US01-01"],
            "test_references": []
        }
        self.save()
        self.assertTrue(any("test references disagree" in x for x in check(self.root)))

    def test_orphaned_story_test_reference_is_blocked(self):
        self.mapping_override = {
            "id": 1, "criterion": "AC-US01-01", "criteria": ["AC-US01-01"],
            "test_references": [
                "test_example.py::test_old", "test_example.py::test_new"
            ]
        }
        self.save()
        self.assertTrue(any("test references disagree" in x for x in check(self.root)))

    def test_duplicate_story_mapping_is_blocked(self):
        self.save()
        path = self.root / "docs" / "Syzeteo-Akzeptanztests-Mapping.json"
        data = json.loads(path.read_text())
        data["stories"].append(data["stories"][0])
        path.write_text(json.dumps(data))
        self.assertTrue(any("duplicate story mapping" in x for x in check(self.root)))


if __name__ == "__main__":
    unittest.main()
