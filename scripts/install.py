#!/usr/bin/env python3
"""Install the five canonical Skills into another project (Python 3 stdlib only).

Dry-run by default. Does not overwrite or delete any existing file.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("learn-requirement", "investigate", "make-plan", "execute", "review-skill")
CONFIG = ("project-rules.md", "user-preferences.md")


def install(tool: str, target: Path, apply: bool) -> int:
    target = target.expanduser().resolve()
    if not target.is_dir():
        print(f"ERROR: project directory does not exist: {target}", file=sys.stderr)
        return 2

    # Cursor can also discover .claude/skills, so 'both' installs only once.
    root = target / (".cursor/skills" if tool == "cursor" else ".claude/skills")
    cfg_root = target / ".agent-workflow"
    jobs = []
    for name in SKILLS:
        src = ROOT / "skills" / name
        dest = root / name
        if not (src / "SKILL.md").is_file():
            print(f"ERROR: missing canonical Skill: {src}", file=sys.stderr)
            return 2
        jobs.append((src, dest, True))
    for name in CONFIG:
        src = ROOT / "templates" / name
        if not src.is_file():
            print(f"ERROR: missing template: {src}", file=sys.stderr)
            return 2
        jobs.append((src, cfg_root / name, False))

    print(f"Target: {target}")
    print(f"Mode: {'apply' if apply else 'dry-run'}; Tool: {tool}")
    blocked = []
    for src, dest, is_dir in jobs:
        if dest.exists() or dest.is_symlink():
            print(f"SKIP existing: {dest.relative_to(target)}")
            blocked.append(dest)
        else:
            print(f"{'INSTALL' if apply else 'WOULD INSTALL'}: {dest.relative_to(target)}")
    if not apply:
        print("\nNo files were changed. Re-run with --apply to install.")
        return 0

    copied = 0
    for src, dest, is_dir in jobs:
        if dest.exists() or dest.is_symlink():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if is_dir:
            # A pre-existing folder is never overwritten.
            shutil.copytree(src, dest)
        else:
            # Exclusive creation avoids overwrite if another process creates it.
            try:
                with dest.open("x", encoding="utf-8") as handle:
                    handle.write(src.read_text(encoding="utf-8"))
            except FileExistsError:
                print(f"SKIP raced existing: {dest.relative_to(target)}")
                continue
        copied += 1
    print(f"\nInstalled {copied} items; skipped {len(blocked)} pre-existing items.")
    print("Read .agent-workflow/project-rules.md and user-preferences.md, then follow docs/quickstart.md.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=("cursor", "claude", "both"), required=True,
                        help="For both, install once to .claude/skills (also discoverable by Cursor)")
    parser.add_argument("--target", required=True, type=Path, help="Existing project directory")
    parser.add_argument("--apply", action="store_true", help="Write new files (otherwise dry-run only)")
    args = parser.parse_args()
    return install(args.tool, args.target, args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
