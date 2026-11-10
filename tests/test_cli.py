"""Offline tests: GitHub Releases are mocked; no network or live projects."""
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_workflow import cli


def archive(version="1.2.3", missing=None, bad_version=False):
    data = {}
    data["VERSION"] = (("9.9.9" if bad_version else version) + "\n").encode()
    for name in cli.SKILLS:
        data[f"skills/{name}/SKILL.md"] = (
            f"---\nname: {name}\ndescription: Portable test skill\n---\n# Test\n"
        ).encode()
    for name in cli.install_engine.CONFIG:
        data[f"templates/{name}"] = f"# {name}\n".encode()
    if version != "0.1.0":
        data["templates/cursor-rule.mdc"] = (
            "---\nalwaysApply: true\n---\n# Initial response rule\n"
        ).encode()
        data["templates/claude-rule.md"] = b"# Initial response rule\n"
    if missing:
        del data[missing]
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as handle:
        for name, content in data.items():
            info = tarfile.TarInfo("publisher-release/" + name)
            info.size = len(content)
            handle.addfile(info, io.BytesIO(content))
    return buffer.getvalue()


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()

    def mock_release(self, payload=None, tag="v1.2.3"):
        tarball = archive() if payload is None else payload
        release = json.dumps({
            "tag_name": tag, "prerelease": False, "draft": False,
            "tarball_url": f"https://api.github.com/repos/{cli.REPO}/tarball/{tag}"
        }).encode()
        def fake_read(url, limit):
            return release if url == cli.API else tarball
        return mock.patch.object(cli, "_read_url", side_effect=fake_read)

    def test_no_release_fails_safely(self):
        from urllib.error import HTTPError
        err = HTTPError(cli.API, 404, "Not Found", {}, None)
        with mock.patch.object(cli, "_read_url", side_effect=err):
            self.assertEqual(cli.main(["install", "--tool", "cursor", "--target", str(self.project)]), 2)
        self.assertFalse((self.project / ".cursor").exists())

    def test_install_then_update_without_git_pull(self):
        with self.mock_release():
            self.assertEqual(cli.main(["install", "--tool", "cursor", "--language", "zh-TW",
                                       "--target", str(self.project)]), 0)
            self.assertEqual(cli.main(["update", "--target", str(self.project), "--check"]), 0)
            self.assertEqual(cli.main(["update", "--target", str(self.project)]), 0)
        state = json.loads((self.project / ".agent-workflow/install-state.json").read_text())
        self.assertEqual(state["version"], "1.2.3")
        self.assertIn("zh-TW", (self.project / ".agent-workflow/language.md").read_text())
        self.assertTrue((self.project / ".cursor/rules/agent-workflow.mdc").is_file())

    def test_install_preview_is_read_only(self):
        with self.mock_release():
            self.assertEqual(cli.main(["install", "--tool", "both", "--target", str(self.project),
                                       "--check"]), 0)
        self.assertFalse((self.project / ".claude").exists())

    def test_invalid_tag_and_mismatch_are_rejected(self):
        with self.mock_release(tag="v1.2.3-rc1"):
            self.assertEqual(cli.main(["install", "--tool", "cursor", "--target", str(self.project)]), 2)
        with self.mock_release(payload=archive(bad_version=True)):
            self.assertEqual(cli.main(["install", "--tool", "cursor", "--target", str(self.project)]), 2)
        self.assertFalse((self.project / ".cursor").exists())

    def test_legacy_release_remains_installable(self):
        with self.mock_release(payload=archive(version="0.1.0"), tag="v0.1.0"):
            self.assertEqual(cli.main(["install", "--tool", "cursor", "--target",
                                       str(self.project)]), 0)
        self.assertTrue((self.project / ".cursor/skills/execute/SKILL.md").is_file())
        self.assertFalse((self.project / ".cursor/rules").exists())

    def test_missing_new_rule_rejected(self):
        with self.mock_release(payload=archive(missing="templates/claude-rule.md")):
            self.assertEqual(cli.main(["install", "--tool", "claude", "--target",
                                       str(self.project)]), 2)
        self.assertFalse((self.project / ".claude").exists())

    def test_incomplete_release_rejected(self):
        with self.mock_release(payload=archive(missing="skills/review-skill/SKILL.md")):
            self.assertEqual(cli.main(["install", "--tool", "claude", "--target", str(self.project)]), 2)
        self.assertFalse((self.project / ".claude").exists())

    def test_custom_skill_and_local_changes_are_kept(self):
        with self.mock_release():
            self.assertEqual(cli.main(["install", "--tool", "cursor", "--target", str(self.project)]), 0)
        skills = self.project / ".cursor/skills"
        custom = skills / "mine/SKILL.md"
        custom.parent.mkdir()
        custom.write_text("personal skill", encoding="utf-8")
        conflict = skills / "execute/SKILL.md"
        conflict.write_text("customized core", encoding="utf-8")
        with self.mock_release():
            self.assertEqual(cli.main(["update", "--target", str(self.project)]), 0)
        self.assertEqual(conflict.read_text(), "customized core")
        self.assertEqual(custom.read_text(), "personal skill")

    def test_download_redirect_is_restricted(self):
        with self.assertRaises(ValueError):
            cli._read_url("https://example.com/malicious.tar.gz", 1234)

    def test_packaged_console_entrypoint(self):
        import agent_workflow.cli
        self.assertTrue(callable(agent_workflow.cli.main))


if __name__ == "__main__":
    unittest.main()
