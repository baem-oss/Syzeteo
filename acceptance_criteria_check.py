#!/usr/bin/env python3
"""Acceptance-criterion integrity gate: IDs, coverage links and executable assertions.

The frozen 2026 baseline remains a historical comparison, not a current
semantic sign-off. This gate checks structure; PR-specific changed-code evidence
is checked separately by tdd_pr_evidence_check.py.
"""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ID = re.compile(r"AC-US([0-9]{2})-([0-9]{2})$")


def assertion_signatures(method):
    """Return AST signatures of direct assertions in a unittest-style method."""
    signatures = []
    for node in ast.walk(method):
        if isinstance(node, ast.Assert):
            signatures.append(ast.dump(node, include_attributes=False))
        elif isinstance(node, ast.Call):
            func = node.func
            if (isinstance(func, ast.Attribute) and func.attr.startswith("assert")
                    and isinstance(func.value, ast.Name) and func.value.id == "self"):
                signatures.append(ast.dump(node, include_attributes=False))
    return signatures


def find_test_method(source, name):
    tree = ast.parse(source)
    found = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    ]
    if len(found) != 1:
        raise ValueError(f"expected exactly one test method {name}, found {len(found)}")
    return found[0]


def check(root=ROOT):
    errors = []

    def read(name):
        return json.loads((root / "docs" / name).read_text(encoding="utf-8"))

    active = read("Syzeteo-Akzeptanzkriterien.json")
    baseline = read("Syzeteo-Akzeptanzkriterien-Baseline.json")
    mapping = read("Syzeteo-Akzeptanztests-Mapping.json")
    old = {c["id"]: c for c in baseline["criteria"]}
    stories = {}
    for item in mapping["stories"]:
        sid = item.get("id")
        if sid in stories:
            errors.append(f"duplicate story mapping: {sid}")
        stories[sid] = item

    seen = set()
    by_story = {}
    result = {"legacy": 0, "new": 0, "changed": 0}
    source_cache = {}
    for criterion in active["criteria"]:
        cid = criterion.get("id", "")
        match = ID.fullmatch(cid) if isinstance(cid, str) else None
        if not match or cid in seen:
            errors.append(f"invalid or duplicated criterion ID: {cid}")
            continue
        seen.add(cid)
        sid = criterion.get("story_id")
        if sid not in stories or sid != int(match.group(1)):
            errors.append(f"{cid}: missing or mismatched story")
        by_story.setdefault(sid, []).append(criterion)
        statement = criterion.get("statement", "")
        if not isinstance(statement, str) or not statement.strip():
            errors.append(f"{cid}: empty acceptance criterion")
        if not isinstance(criterion.get("manual_review"), bool):
            errors.append(f"{cid}: manual_review must be boolean")
        refs = criterion.get("test_references", [])
        if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
            errors.append(f"{cid}: tests must be a string list")
            continue
        if len(refs) != len(set(refs)):
            errors.append(f"{cid}: duplicate test references")
            continue
        previous = old.get(cid)
        changed = previous is None or any(
            criterion.get(key) != previous.get(key)
            for key in ("story_id", "statement", "status", "manual_review")
        )
        if changed:
            result["new" if previous is None else "changed"] += 1
            if not set(refs) - set(previous.get("test_references", []) if previous else []):
                errors.append(f"{cid}: new/changed criterion requires a new test reference")
        else:
            result["legacy"] += 1
        for ref in refs:
            try:
                filename, method = ref.split("::")
                if (Path(filename).name != filename
                        or not filename.startswith("test_") or not filename.endswith(".py")
                        or not method.startswith("test_")):
                    raise ValueError("invalid test reference")
                if filename not in source_cache:
                    source_cache[filename] = (root / filename).read_text(encoding="utf-8")
                node = find_test_method(source_cache[filename], method)
                if not assertion_signatures(node):
                    raise ValueError("test method contains no direct assertions")
            except (ValueError, OSError, SyntaxError) as exc:
                errors.append(f"{cid}: invalid reference {ref}: {exc}")
        if not refs:
            print(f"GAP {cid}: no automated test mapped")

    for sid, item in stories.items():
        criteria = by_story.get(sid, [])
        ids = {c["id"] for c in criteria}
        declared = item.get("criteria")
        if (not isinstance(declared, list) or len(declared) != len(set(declared))
                or set(declared) != ids):
            errors.append(f"US #{sid:02d}: criteria mapping differs from acceptance catalog")
        expected_primary = f"AC-US{sid:02d}-01"
        if item.get("criterion") != expected_primary or expected_primary not in ids:
            errors.append(f"US #{sid:02d}: invalid primary criterion mapping")
        mapped = item.get("test_references")
        if not isinstance(mapped, list) or len(mapped) != len(set(mapped)):
            errors.append(f"US #{sid:02d}: invalid or duplicate story test mappings")
        else:
            referenced = {ref for c in criteria for ref in c.get("test_references", [])}
            if set(mapped) != referenced:
                errors.append(f"US #{sid:02d}: criterion/story test references disagree")

    for story_id in stories.keys() - by_story.keys():
        errors.append(f"US #{story_id:02d}: no acceptance criterion defined")
    for cid in old.keys() - seen:
        errors.append(f"{cid}: baseline criterion removed")
    print(f"Acceptance criteria: {len(seen)} total; {result['legacy']} unchanged; "
          f"{result['new']} new; {result['changed']} changed")
    return errors


def main():
    errors = check()
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
