"""Contract tests for PR-relative acceptance-criterion assertion evidence."""
import tempfile
import unittest
from pathlib import Path

from tdd_pr_evidence_check import check_incremental, check_pr


class PRAssertionEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.old = [{
            "id": "AC-US01-01", "story_id": 1,
            "statement": "Old rule", "status": "specified_partial",
            "manual_review": False, "test_references": ["test_x.py::test_rule"]
        }]
        self.new = [dict(self.old[0])]
        self.before = {"test_x.py": "def test_rule():\n    assert result == 1\n"}
        self.after = dict(self.before)

    def check(self):
        return check_incremental(
            self.old, self.new,
            self.before.get, self.after.get
        )

    def test_unchanged_criteria_require_no_new_assertions(self):
        self.assertEqual(self.check(), ([], 0))

    def test_changed_rule_with_unchanged_test_is_blocked(self):
        self.new[0]["statement"] = "A new behavior"
        errors, count = self.check()
        self.assertEqual(count, 1)
        self.assertIn("requires a new or modified test assertion", errors[0])

    def test_changed_rule_with_modified_assertion_is_accepted(self):
        self.new[0]["statement"] = "New behavior"
        self.after["test_x.py"] = "def test_rule():\n    assert result == 2\n"
        self.assertEqual(self.check(), ([], 1))

    def test_new_criterion_cannot_reuse_unmodified_existing_test(self):
        self.new.append({
            "id": "AC-US01-02", "story_id": 1,
            "statement": "New", "status": "specified_partial",
            "manual_review": False, "test_references": ["test_x.py::test_rule"]
        })
        errors, count = self.check()
        self.assertEqual(count, 1)
        self.assertIn("AC-US01-02", errors[0])

    def test_new_test_method_with_assertion_is_accepted(self):
        self.new.append({
            "id": "AC-US01-02", "story_id": 1,
            "statement": "New", "status": "specified_partial",
            "manual_review": False, "test_references": ["test_new.py::test_new_behavior"]
        })
        self.after["test_new.py"] = (
            "def test_new_behavior():\n    assert measured == expected\n"
        )
        self.assertEqual(self.check(), ([], 1))

    def test_test_setup_change_without_assertion_change_is_blocked(self):
        self.new[0]["statement"] = "Different requirement"
        self.after["test_x.py"] = (
            "def test_rule():\n    result = calculate()\n    assert result == 1\n"
        )
        self.assertTrue(self.check()[0])

    def test_new_test_method_with_only_pass_is_blocked(self):
        self.new.append({
            "id": "AC-US01-02", "story_id": 1,
            "statement": "New", "status": "specified_partial",
            "manual_review": False, "test_references": ["test_new.py::test_new_behavior"]
        })
        self.after["test_new.py"] = "def test_new_behavior(): pass\n"
        self.assertTrue(self.check()[0])

    def test_criterion_removed_from_pr_base_is_blocked(self):
        self.new = []
        errors, _ = self.check()
        self.assertIn("criterion removed", errors[0])

    def test_test_reference_only_change_needs_modified_assertion(self):
        self.new[0]["test_references"] = ["test_x.py::test_other"]
        self.after["test_x.py"] += "\ndef test_other():\n    assert actual == expected\n"
        self.assertEqual(self.check(), ([], 1))

    def test_test_reference_only_change_cannot_reuse_old_assertion(self):
        self.before["test_x.py"] += "\ndef test_other():\n    assert actual == expected\n"
        self.after = dict(self.before)
        self.new[0]["test_references"] = ["test_x.py::test_other"]
        self.assertTrue(self.check()[0])

    def test_missing_pr_base_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            errors, changed = check_pr(Path(temp), "missing-branch")
        self.assertEqual(changed, 0)
        self.assertIn("unavailable", errors[0])


if __name__ == "__main__":
    unittest.main()
