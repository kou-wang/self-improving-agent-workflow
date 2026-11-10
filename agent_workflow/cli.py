"""User-facing agent-workflow CLI.

Gets only published, non-prerelease GitHub releases and installs vetted Skill text.
The downloaded archive is treated as data; Python code from it is never executed.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from scripts import install as install_engine
from scripts import update as update_engine

REPO = "kou-wang/self-improving-agent-workflow"
API = f"https://api.github.com/repos/{REPO}/releases/latest"
TAG = re.compile(r"^v([0-9]+)\.([0-9]+)\.([0-9]+)$")
SKILLS = install_engine.SKILLS
MAX_DOWNLOAD = 8 * 1024 * 1024
MAX_TEXT = 512 * 1024
MAX_TOTAL = 4 * 1024 * 1024
ALLOWED_HOSTS = {"api.github.com", "github.com", "codeload.github.com"}


def _read_url(url: str, max_size: int) -> bytes:
    # Restrict redirects and destinations to GitHub's documented infrastructure.
    class RestrictedRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            candidate = urllib.parse.urlsplit(newurl)
            if candidate.scheme != "https" or candidate.hostname not in ALLOWED_HOSTS:
                raise ValueError("Untrusted release redirect")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Untrusted GitHub URL")
    opener = urllib.request.build_opener(RestrictedRedirect())
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "self-improving-agent-workflow-cli",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with opener.open(request, timeout=20) as response:
        data = response.read(max_size + 1)
    if len(data) > max_size:
        raise ValueError("Release response too large")
    return data


def _release_metadata() -> tuple[str, str]:
    try:
        release = json.loads(_read_url(API, 256 * 1024))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise ValueError("No published stable GitHub Release yet. Nothing was changed.") from error
        raise
    tag = release.get("tag_name", "")
    match = TAG.fullmatch(tag)
    if release.get("draft") or release.get("prerelease") or not match:
        raise ValueError("Latest Release is not a stable semantic version")
    archive = release.get("tarball_url", "")
    if not isinstance(archive, str) or not archive.startswith(
        f"https://api.github.com/repos/{REPO}/tarball/"
    ):
        raise ValueError("Unexpected release archive URL")
    return tag, archive


def _release_tree(tag: str, archive_url: str, root: Path) -> None:
    # Never extract the downloaded tarball to disk. Only read explicitly expected
    # regular text files and put their bytes under a temporary isolated directory.
    source = _read_url(archive_url, MAX_DOWNLOAD)
    needed = {"VERSION"}
    needed.update(f"skills/{name}/SKILL.md" for name in SKILLS)
    needed.update(f"templates/{name}" for name in install_engine.CONFIG)
    found = {}
    total = 0
    with tarfile.open(fileobj=io.BytesIO(source), mode="r:gz") as archive:
        for member in archive:
            relative = member.name.split("/", 1)
            if len(relative) != 2 or relative[1] not in needed:
                continue
            path = relative[1]
            if path in found or not member.isfile() or member.size > MAX_TEXT:
                raise ValueError(f"Invalid or duplicate release file: {path}")
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError(f"Could not read release file: {path}")
            data = stream.read(MAX_TEXT + 1)
            if len(data) != member.size:
                raise ValueError(f"Invalid release file length: {path}")
            data.decode("utf-8")
            total += len(data)
            if total > MAX_TOTAL:
                raise ValueError("Release files exceeded safe size limit")
            found[path] = data
    if set(found) != needed:
        raise ValueError(f"Incomplete release archive: {sorted(needed - set(found))}")
    expected = tag.removeprefix("v")
    if found["VERSION"].decode("utf-8").strip() != expected:
        raise ValueError("Release VERSION does not match published Git tag")
    for path, data in found.items():
        dest = root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)


def _version_tuple(value: str):
    match = re.fullmatch(r"v?([0-9]+)\.([0-9]+)\.([0-9]+)(?:[-+].*)?", value)
    return tuple(map(int, match.groups()[:3])) if match else None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="agent-workflow",
        description="Install and safely update Cursor / Claude Code Skills from stable GitHub Releases.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    install = sub.add_parser("install", help="Install the latest stable workflow in a project")
    install.add_argument("--tool", required=True, choices=("cursor", "claude", "both"))
    install.add_argument("--target", type=Path, default=Path.cwd())
    install.add_argument("--language", choices=install_engine.LANGUAGES, default="en")
    install.add_argument("--check", action="store_true", help="Dry run; default is to install")

    update = sub.add_parser("update", help="Fetch latest stable Release and safely update the project")
    update.add_argument("--target", type=Path, default=Path.cwd())
    update.add_argument("--check", action="store_true", help="Preview without writes")
    update.add_argument("--use-upstream", action="append", default=[], metavar="SKILL",
                        help="Explicitly replace a locally modified official Skill, with backup")

    rollback = sub.add_parser("rollback", help="Restore a prior safe-update backup")
    rollback.add_argument("backup_id")
    rollback.add_argument("--target", type=Path, default=Path.cwd())
    rollback.add_argument("--apply", action="store_true", help="Actually restore; default is preview")

    args = parser.parse_args(argv)
    if args.command == "rollback":
        return update_engine.rollback(args.target, args.backup_id, args.apply)

    try:
        tag, archive_url = _release_metadata()
        with tempfile.TemporaryDirectory(prefix="agent-workflow-release-") as temp:
            root = Path(temp)
            _release_tree(tag, archive_url, root)
            if args.command == "install":
                old = install_engine.ROOT
                try:
                    install_engine.ROOT = root
                    print(f"Official release: {tag}")
                    return install_engine.install(args.tool, args.target, not args.check, args.language)
                finally:
                    install_engine.ROOT = old

            # Do not downgrade a project installed from a newer official version.
            try:
                state = update_engine.load_state(args.target.expanduser().resolve() / ".agent-workflow")
            except (ValueError, OSError, json.JSONDecodeError) as error:
                print(f"ERROR: {error}", file=sys.stderr)
                return 2
            current = _version_tuple(state.get("version", "")) if state else None
            incoming = _version_tuple(tag)
            if current and incoming and incoming < current:
                print(f"ERROR: installed version is newer than {tag}; refusing downgrade", file=sys.stderr)
                return 2
            old = update_engine.ROOT
            try:
                update_engine.ROOT = root
                print(f"Official release: {tag}")
                return update_engine.update(
                    args.target, apply=not args.check,
                    use_upstream=set(args.use_upstream),
                )
            finally:
                update_engine.ROOT = old
    except (ValueError, OSError, urllib.error.URLError, tarfile.TarError,
            UnicodeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
