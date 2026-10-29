#!/usr/bin/env python3
"""Incremental acceptance-criteria gate. Existing criteria remain non-blocking."""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOC = ROOT / "docs"
ID = re.compile(r"AC-US([0-9]{2})-([0-9]{2})$")


def check(root=ROOT):
    errors = []
    def read(name):
        return json.loads((root / "docs" / name).read_text(encoding="utf-8"))
    active = read("Syzeteo-Akzeptanzkriterien.json")
    baseline = read("Syzeteo-Akzeptanzkriterien-Baseline.json")
    mapping = read("Syzeteo-Akzeptanztests-Mapping.json")
    stories = {item["id"] for item in mapping["stories"]}
    old = {c["id"]: c for c in baseline["criteria"]}
    seen = set()
    result = {"legacy": 0, "new": 0, "changed": 0}
    for criterion in active["criteria"]:
        cid = criterion.get("id", "")
        match = ID.fullmatch(cid)
        if not match or cid in seen:
            errors.append(f"invalid or duplicated criterion ID: {cid}")
            continue
        seen.add(cid)
        sid = criterion.get("story_id")
        if sid not in stories or sid != int(match.group(1)):
            errors.append(f"{cid}: missing or mismatched story")
        statement = criterion.get("statement", "")
        if not isinstance(statement, str) or not statement.strip():
            errors.append(f"{cid}: empty acceptance criterion")
        refs = criterion.get("test_references", [])
        if not isinstance(refs, list) or len(refs) != len(set(refs)):
            errors.append(f"{cid}: tests must be a duplicate-free list")
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
                if Path(filename).name != filename or not filename.startswith("test_") or not method.startswith("test_"):
                    raise ValueError("invalid test reference")
                tree = ast.parse((root / filename).read_text(encoding="utf-8"))
                if not any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                           and node.name == method for node in ast.walk(tree)):
                    raise ValueError("method not found")
            except (ValueError, OSError, SyntaxError) as exc:
                errors.append(f"{cid}: invalid reference {ref}: {exc}")
        if not refs:
            print(f"GAP {cid}: no automated test mapped")
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
