#!/usr/bin/env python3
"""Safe updater for managed core Skills. No network access; update the source checkout first."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("learn-requirement", "investigate", "make-plan", "execute", "review-skill")
STATE = "install-state.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def safe_file(path: Path) -> bool:
    return not path.is_symlink() and (not path.exists() or path.is_file())


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".workflow-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def load_state(config: Path) -> dict | None:
    path = config / STATE
    if path.is_symlink():
        raise ValueError("Refusing symlinked installation state")
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != 1 or data.get("tool") not in ("cursor", "claude", "both", "copilot", "all"):
        raise ValueError("Unsupported installation-state format")
    if not isinstance(data.get("managed"), dict):
        raise ValueError("Invalid managed Skills map")
    return data


def location(target: Path, tool: str) -> Path:
    return target / (".cursor/skills" if tool == "cursor" else
                     ".github/skills" if tool == "copilot" else ".claude/skills")


def plan(target: Path, state: dict | None, prefer: set[str]) -> list[dict]:
    tool = state["tool"] if state else infer_tool(target)
    root = location(target, tool)
    managed = (state or {}).get("managed", {})
    items = []
    for name in SKILLS:
        upstream = ROOT / "skills" / name / "SKILL.md"
        source = upstream.read_bytes()
        source_hash = digest(source)
        folder = root / name
        path = folder / "SKILL.md"
        if root.is_symlink() or folder.is_symlink() or not safe_file(path):
            status, current_hash = "CONFLICT (symlink/non-file)", None
        elif not path.exists():
            # An existing folder with extra files is not safe to create into.
            status, current_hash = ("CONFLICT (unmanaged directory)", None) if folder.exists() else ("ADD", None)
        else:
            current_hash = digest(path.read_bytes())
            recorded = managed.get(name)
            if current_hash == source_hash:
                status = "CURRENT"
            elif name in prefer:
                status = "REPLACE (explicit upstream choice)"
            elif recorded and current_hash == recorded:
                status = "UPDATE"
            else:
                status = "CONFLICT (locally modified or untracked)"
        items.append(dict(name=name, path=path, upstream=source, upstream_hash=source_hash,
                          current_hash=current_hash, status=status))
    return items


def infer_tool(target: Path) -> str:
    cursor = (target / ".cursor/skills").exists()
    claude = (target / ".claude/skills").exists()
    copilot = (target / ".github/skills").exists()
    if sum((cursor, claude, copilot)) > 1:
        raise ValueError("Both Skill locations exist; installation history is missing. Resolve paths manually.")
    if copilot:
        return "copilot"
    if cursor:
        return "cursor"
    if claude:
        return "both"
    raise ValueError("No installation found. Run scripts/install.py first.")


def update(target: Path, apply: bool = False, use_upstream: set[str] | None = None) -> int:
    prefer = use_upstream or set()
    if prefer - set(SKILLS):
        print(f"ERROR: unknown Skill names: {sorted(prefer - set(SKILLS))}", file=sys.stderr)
        return 2
    target = target.expanduser().resolve()
    config = target / ".agent-workflow"
    if not target.is_dir() or config.is_symlink() or not config.is_dir():
        print("ERROR: target is missing .agent-workflow or has unsafe configuration", file=sys.stderr)
        return 2
    try:
        state = load_state(config)
        items = plan(target, state, prefer)
        new_version = version()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    current_version = state.get("version", "legacy/untracked") if state else "legacy/untracked"
    print(f"Installed: {current_version} | Source checkout: {new_version}")
    for item in items:
        print(f"{item['status']:42} {item['name']}")
    changes = [x for x in items if x["status"] in ("ADD", "UPDATE", "REPLACE (explicit upstream choice)")]
    conflicts = [x for x in items if x["status"].startswith("CONFLICT")]
    if conflicts:
        print("Conflicts kept untouched. Options: keep local; compare and merge manually; "
              "or explicitly choose --use-upstream NAME (backup created).")
    if not apply:
        print(f"Dry run: {len(changes)} applicable changes, {len(conflicts)} conflicts. Use --apply to proceed.")
        return 0

    # The actual changed paths are snapshot before modifications, to support safe rollback.
    if not state:
        state = {"schema": 1, "tool": infer_tool(target), "version": "legacy/untracked", "managed": {}}
    if not changes:
        # Adopt identical legacy files without touching their contents.
        for item in items:
            if item["status"] == "CURRENT":
                state["managed"][item["name"]] = item["upstream_hash"]
        state["version"] = new_version if not conflicts else state["version"]
        write_atomic(config / STATE, (json.dumps(state, indent=2, sort_keys=True) + "\n").encode())
        print("No Skills replaced; current identical Skills may have been adopted.")
        return 0

    root = location(target, state["tool"])
    if root.is_symlink():
        print("ERROR: unsafe Skill directory", file=sys.stderr)
        return 2
    backup_root = config / "backups"
    if backup_root.is_symlink():
        print("ERROR: unsafe backups directory", file=sys.stderr)
        return 2
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = backup_root / run_id
    backup.mkdir(parents=True, exist_ok=False)
    before_state = (config / STATE).read_bytes() if (config / STATE).exists() else None
    entries = []
    try:
        for item in changes:
            name, path = item["name"], item["path"]
            # Recheck before writing in case a user edited a file after preview.
            if path.is_symlink() or path.parent.is_symlink() or not safe_file(path):
                raise RuntimeError(f"Unsafe destination changed: {name}")
            old = path.read_bytes() if path.exists() else None
            observed_hash = digest(old) if old is not None else None
            if observed_hash != item["current_hash"]:
                raise RuntimeError(f"Destination changed during update: {name}")
            if old is not None:
                (backup / (name + ".before")).write_bytes(old)
            entries.append({"name": name, "had_file": old is not None,
                            "before_hash": digest(old) if old is not None else None,
                            "after_hash": item["upstream_hash"]})
            write_atomic(path, item["upstream"])
            state["managed"][name] = item["upstream_hash"]
        for item in items:
            if item["status"] == "CURRENT":
                state["managed"][item["name"]] = item["upstream_hash"]
        if not conflicts:
            state["version"] = new_version
        write_atomic(config / STATE, (json.dumps(state, indent=2, sort_keys=True) + "\n").encode())
        (backup / "state.before").write_bytes(before_state or b"")
        (backup / "rollback.json").write_text(json.dumps({"tool": state["tool"],
                                                          "entries": entries,
                                                          "state_after": digest((config / STATE).read_bytes())},
                                                         indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        # Fail closed, and retain backup for manual recovery; do not claim success.
        print(f"ERROR during update: {exc}; inspect backup at {backup}", file=sys.stderr)
        return 2
    print(f"Updated {len(changes)} Skills. Backup ID: {run_id}")
    if conflicts:
        print(f"Remaining conflicts: {len(conflicts)}; unchanged.")
    return 0


def rollback(target: Path, backup_id: str, apply: bool) -> int:
    if not backup_id or any(c not in "0123456789TZ" for c in backup_id):
        print("ERROR: invalid backup ID", file=sys.stderr)
        return 2
    target = target.expanduser().resolve()
    config = target / ".agent-workflow"
    backup = config / "backups" / backup_id
    if config.is_symlink() or (config / "backups").is_symlink() or backup.is_symlink() or (backup / "rollback.json").is_symlink() or not (backup / "rollback.json").is_file():
        print("ERROR: backup not found or unsafe", file=sys.stderr)
        return 2
    try:
        record = json.loads((backup / "rollback.json").read_text(encoding="utf-8"))
        root = location(target, record["tool"])
        state_path = config / STATE
        if config.is_symlink() or root.is_symlink() or state_path.is_symlink():
            raise ValueError("Symlinked path")
        if not state_path.is_file() or digest(state_path.read_bytes()) != record["state_after"]:
            raise ValueError("Installation state changed since backup; refusing rollback")
        for entry in record["entries"]:
            name = entry["name"]
            if name not in SKILLS:
                raise ValueError("Unknown backed-up Skill")
            path = root / name / "SKILL.md"
            if path.is_symlink() or path.parent.is_symlink() or not path.is_file():
                raise ValueError(f"Missing or unsafe installed Skill: {name}")
            if digest(path.read_bytes()) != entry["after_hash"]:
                raise ValueError(f"Local edits after upgrade: {name}; refusing rollback")
            if entry["had_file"] and digest((backup / (name + ".before")).read_bytes()) != entry["before_hash"]:
                raise ValueError(f"Damaged backup: {name}")
        print(f"{'ROLL BACK' if apply else 'WOULD ROLL BACK'} {len(record['entries'])} Skills from {backup_id}")
        if not apply:
            return 0
        for entry in record["entries"]:
            path = root / entry["name"] / "SKILL.md"
            if entry["had_file"]:
                write_atomic(path, (backup / (entry["name"] + ".before")).read_bytes())
            else:
                path.unlink()
                path.parent.rmdir()  # only removes an empty newly created directory
        old_state = (backup / "state.before").read_bytes()
        if old_state:
            write_atomic(state_path, old_state)
        else:
            state_path.unlink()
        print("Rollback complete. Backup retained for audit.")
        return 0
    except (KeyError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="Existing installed project")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Preview update, no writes")
    mode.add_argument("--apply", action="store_true", help="Apply safe updates")
    mode.add_argument("--rollback", metavar="BACKUP_ID", help="Preview rollback for a backup ID")
    parser.add_argument("--confirm-rollback", action="store_true", help="Apply --rollback after preview")
    parser.add_argument("--use-upstream", action="append", default=[], metavar="SKILL",
                        help="Explicitly replace a conflicting named Skill; creates backup")
    args = parser.parse_args()
    if args.rollback:
        return rollback(args.target, args.rollback, args.confirm_rollback)
    if args.confirm_rollback:
        parser.error("--confirm-rollback requires --rollback")
    return update(args.target, apply=args.apply, use_upstream=set(args.use_upstream))


if __name__ == "__main__":
    raise SystemExit(main())
