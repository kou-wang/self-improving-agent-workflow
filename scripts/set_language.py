#!/usr/bin/env python3
"""Select an installed project's response language without touching other preferences."""
import argparse
from pathlib import Path

LANGUAGES = {"en": "English", "zh-CN": "简体中文", "zh-TW": "繁體中文"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="Existing project root")
    parser.add_argument("--language", required=True, choices=LANGUAGES)
    parser.add_argument("--apply", action="store_true", help="Apply after preview")
    args = parser.parse_args()
    root = args.target.expanduser().resolve()
    if not root.is_dir() or not (root / ".agent-workflow").is_dir():
        parser.error("Target project must exist and have .agent-workflow/ installed")
    path = root / ".agent-workflow" / "language.md"
    if path.is_symlink():
        parser.error("Refusing to replace a symlink")
    if path.exists() and not path.is_file():
        parser.error("Expected a regular language.md file")
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if not existing.startswith("# Agent response language\nLanguage: "):
            parser.error("Unrecognized language.md format; refusing to overwrite custom content")
    print(f"{'SET' if args.apply else 'WOULD SET'} {path}: {args.language} ({LANGUAGES[args.language]})")
    if args.apply:
        path.write_text(f"# Agent response language\nLanguage: {args.language}\n", encoding="utf-8")
        print("Restart the agent session or explicitly ask it to re-read the updated language file.")

if __name__ == "__main__":
    main()
