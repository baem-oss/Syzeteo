#!/usr/bin/env python3
"""Require changed/new acceptance criteria to have changed *assertions* in the PR.

Compared with the pull request's target branch, not the immutable 2026
historical baseline. Reusing an unchanged test name alone is insufficient.
This is syntactic evidence; reviewers must still check semantic relevance.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from acceptance_criteria_check import assertion_signatures, find_test_method

ROOT = Path(__file__).resolve().parent


def assertion_evidence(source, method):
    if source is None:
        return []
    try:
        node = find_test_method(source, method)
    except (ValueError, SyntaxError):
        return []
    return assertion_signatures(node)


def check_incremental(old_criteria, new_criteria, old_file, new_file):
    """Compare criteria and associated assertion ASTs, without Git side effects.

    old_file/new_file take a repository-relative filename and return source or
    None if the file does not exist. Tests can therefore exercise the contract
    without cloning a repository.
    """
    errors = []
    before = {item["id"]: item for item in old_criteria}
    after = {item["id"]: item for item in new_criteria}
    for cid in sorted(before.keys() - after.keys()):
        errors.append(f"{cid}: criterion removed since PR base; reviewed migration required")
    checked = 0
    for cid, item in sorted(after.items()):
        prev = before.get(cid)
        if prev is not None and all(
            item.get(key) == prev.get(key)
            for key in ("story_id", "statement", "status", "manual_review")
        ) and set(item.get("test_references", [])) == set(prev.get("test_references", [])):
            continue
        checked += 1
        supported = False
        for reference in item.get("test_references", []):
            try:
                filename, method = reference.split("::")
            except ValueError:
                continue
            current = assertion_evidence(new_file(filename), method)
            previous = assertion_evidence(old_file(filename), method)
            if current and any(assertion not in previous for assertion in current):
                supported = True
                break
        if not supported:
            errors.append(
                f"{cid}: changed/new criterion requires a new or modified test "
                f"assertion in this PR; an unchanged reference does not count"
            )
    return errors, checked


def read_git_file(base_ref, path, root=ROOT):
    completed = subprocess.run(
        ["git", "show", f"{base_ref}:{path}"], cwd=root,
        text=True, encoding="utf-8", capture_output=True, check=False
    )
    return completed.stdout if completed.returncode == 0 else None


def check_pr(root=ROOT, base_ref="origin/main"):
    # Fail closed if the target ref cannot be resolved. Do not silently compare
    # against an empty repository and mistake all tests for new assertions.
    resolved = subprocess.run(
        ["git", "rev-parse", "--verify", f"{base_ref}^{{commit}}"],
        cwd=root, capture_output=True, text=True, check=False
    )
    if resolved.returncode != 0:
        return [f"PR base ref {base_ref!r} is unavailable; fetch it first"], 0
    name = "docs/Syzeteo-Akzeptanzkriterien.json"
    old_json = read_git_file(base_ref, name, root)
    if old_json is None:
        return [f"PR base has no {name}; explicit migration required"], 0
    old = json.loads(old_json)["criteria"]
    current = json.loads((root / name).read_text(encoding="utf-8"))["criteria"]
    base_sources = {}
    new_sources = {}

    def base_file(filename):
        if filename not in base_sources:
            base_sources[filename] = read_git_file(base_ref, filename, root)
        return base_sources[filename]

    def current_file(filename):
        if filename not in new_sources:
            path = root / filename
            new_sources[filename] = path.read_text(encoding="utf-8") if path.is_file() else None
        return new_sources[filename]

    return check_incremental(old, current, base_file, current_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default="origin/main")
    args = parser.parse_args()
    errors, changed = check_pr(base_ref=args.base_ref)
    print(f"PR criterion evidence: {changed} added/modified criteria checked")
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
