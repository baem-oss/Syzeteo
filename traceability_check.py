#!/usr/bin/env python3
"""Validate incremental TDD traceability. Legacy gaps are reported, not blocked."""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOC = ROOT / "docs"
PATTERN = re.compile(r"^- \\[x\\] \\*\\*US #(\\d+) – ([^\\n*]+)\\*\\*([\\s\\S]*?)(?=\\n- \\[x\\] \\*\\*US #|\\s*$)", re.M)

def load(name):
    return json.loads((DOC / name).read_text(encoding="utf-8"))

def main():
    manifest = load("Syzeteo-Akzeptanztests-Mapping.json")
    baseline = load("Syzeteo-TDD-Baseline.json")
    content = (DOC / "Syzeteo-L-US-DE.md").read_text(encoding="utf-8")
    found = {int(m.group(1)): (m.group(2).strip(), " ".join(m.group(3).split())) for m in PATTERN.finditer(content)}
    old = {r["id"]: r for r in baseline["stories"]}
    current = {r["id"]: r for r in manifest["stories"]}
    errors = []
    for sid in sorted(found):
        if sid not in current:
            errors.append(f"US #{sid:02d}: no acceptance mapping entry")
            continue
        item = current[sid]
        refs = item.get("test_references", [])
        new_or_changed = sid not in old or found[sid] != (old[sid]["title"], old[sid]["description"])
        if new_or_changed:
            previous = set(old[sid]["test_references"]) if sid in old else set()
            if not set(refs) - previous:
                errors.append(f"US #{sid:02d}: new/changed story requires at least one NEW test reference (baseline must not be silently changed)")
        if not refs:
            print(f"GAP: US #{sid:02d} has no mapped automated tests")
        for ref in refs:
            try:
                filename, method = ref.split("::", 1)
                tree = ast.parse((ROOT / filename).read_text(encoding="utf-8"))
                names = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
                if not filename.startswith("test_") or not method.startswith("test_") or method not in names:
                    raise ValueError("test method not found")
            except (ValueError, OSError, SyntaxError) as exc:
                errors.append(f"US #{sid:02d}: invalid test reference {ref}: {exc}")
    for sid in sorted(set(current) - set(found)):
        errors.append(f"US #{sid:02d}: mapping without corresponding user story")
    for sid in sorted(set(old) - set(found)):
        errors.append(f"US #{sid:02d}: established story removed; explicit review required")
    print(f"Traceability: {len(found)} stories; {sum(bool(current.get(i, {}).get('test_references')) for i in found)} mapped; {sum(not bool(current.get(i, {}).get('test_references')) for i in found)} without automation")
    for err in errors:
        print("ERROR:", err, file=sys.stderr)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
