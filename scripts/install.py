#!/usr/bin/env python3
"""Install the five canonical Skills into another project (Python 3 stdlib only).

Dry-run by default. Does not overwrite or delete any existing file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("learn-requirement", "investigate", "make-plan", "execute", "review-skill")
CONFIG = ("project-rules.md", "user-preferences.md")
STATE = "install-state.json"


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
LANGUAGES = ("en", "zh-CN", "zh-TW")


def install(tool: str, target: Path, apply: bool, language: str = "en") -> int:
    if language not in LANGUAGES:
        print(f"ERROR: unsupported language: {language}", file=sys.stderr)
        return 2
    target = target.expanduser().resolve()
    if not target.is_dir():
        print(f"ERROR: project directory does not exist: {target}", file=sys.stderr)
        return 2

    # Cursor and Copilot both recognize .claude/skills. Share one copy for
    # 'both' (Cursor + Claude) and 'all' (Cursor + Claude + Copilot).
    skill_dir = {"cursor": ".cursor/skills", "claude": ".claude/skills",
                 "both": ".claude/skills", "copilot": ".github/skills",
                 "all": ".claude/skills"}
    if tool not in skill_dir:
        print(f"ERROR: unsupported tool: {tool}", file=sys.stderr)
        return 2
    root = target / skill_dir[tool]
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

    # Always-on project rules make preferences effective even without a Skill.
    # Do not touch existing rules: project owners may have customized them.
    rule_jobs = []
    if tool in ("cursor", "both", "all"):
        rule_jobs.append(("cursor-rule.mdc", ".cursor/rules/agent-workflow.mdc"))
    if tool in ("claude", "both", "all"):
        rule_jobs.append(("claude-rule.md", ".claude/rules/agent-workflow.md"))
    if tool in ("copilot", "all"):
        rule_jobs.append(("copilot-instructions.md", ".github/copilot-instructions.md"))
    # v0.1.0 release archives predate always-on rules. They remain installable
    # with an upgraded CLI; mixed/incomplete template sets fail closed.
    rule_available = [(ROOT / "templates" / name).is_file()
                      for name in ("cursor-rule.mdc", "claude-rule.md")]
    if any(rule_available) and not all(rule_available):
        print("ERROR: incomplete response rule templates", file=sys.stderr)
        return 2
    if tool in ("copilot", "all") and not (ROOT / "templates/copilot-instructions.md").is_file():
        print("ERROR: this source release does not support GitHub Copilot (requires v0.3.0+)",
              file=sys.stderr)
        return 2
    if all(rule_available):
        for template_name, relative_dest in rule_jobs:
            src = ROOT / "templates" / template_name
            jobs.append((src, target / relative_dest, False))
    elif rule_jobs:
        print("NOTE: this legacy release has no always-on response rule templates.")

    # Language is independent of the user preferences file and is never overwritten.
    jobs.append((None, cfg_root / "language.md", False))

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
                    handle.write((f"# Agent response language\nLanguage: {language}\n" if src is None else src.read_text(encoding="utf-8")))
            except FileExistsError:
                print(f"SKIP raced existing: {dest.relative_to(target)}")
                continue
        copied += 1
    # Track only files installed or byte-identical to source.
    state_path = cfg_root / STATE
    if state_path.is_symlink():
        print("WARNING: symlinked install-state.json; not writing it", file=sys.stderr)
    elif not state_path.exists():
        managed = {}
        for name in SKILLS:
            source = ROOT / "skills" / name / "SKILL.md"
            installed = root / name / "SKILL.md"
            if installed.is_file() and not installed.is_symlink() and hash_file(installed) == hash_file(source):
                managed[name] = hash_file(source)
        record = {"schema": 1, "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
                  "tool": tool, "managed": managed}
        try:
            with state_path.open("x", encoding="utf-8") as handle:
                json.dump(record, handle, indent=2, sort_keys=True)
                handle.write("\n")
            print("Created installation state for safe future upgrades.")
        except FileExistsError:
            print("SKIP existing installation state.")
    print(f"\nInstalled {copied} items; skipped {len(blocked)} pre-existing items.")
    print("Read .agent-workflow/project-rules.md and user-preferences.md, then follow docs/quickstart.md.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=("cursor", "claude", "both", "copilot", "all"), required=True,
                        help="For both/all, share one .claude/skills copy across compatible agents")
    parser.add_argument("--target", required=True, type=Path, help="Existing project directory")
    parser.add_argument("--apply", action="store_true", help="Write new files (otherwise dry-run only)")
    parser.add_argument("--language", choices=LANGUAGES, default="en", help="Response language on first install (default: en)")
    args = parser.parse_args()
    return install(args.tool, args.target, args.apply, args.language)


if __name__ == "__main__":
    raise SystemExit(main())
