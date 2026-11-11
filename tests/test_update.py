"""Tests for managed core Skill upgrades and safe rollback."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


installer = load("workflow_installer", "install.py")
updater = load("workflow_updater", "update.py")


class UpgradeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.target = root / "project"
        self.target.mkdir()
        self.source = root / "source"
        shutil.copytree(ROOT / "skills", self.source / "skills")
        (self.source / "VERSION").write_text("0.2.0-test\n", encoding="utf-8")
        self.original_root = updater.ROOT
        updater.ROOT = self.source
        self.addCleanup(lambda: setattr(updater, "ROOT", self.original_root))
        self.assertEqual(installer.install("cursor", self.target, True, "zh-CN"), 0)
        self.skill = self.target / ".cursor/skills/execute/SKILL.md"
        self.source_skill = self.source / "skills/execute/SKILL.md"
        self.prefs = self.target / ".agent-workflow/user-preferences.md"
        self.language = self.target / ".agent-workflow/language.md"

    def test_copilot_update_and_rollback_preserves_preferences(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            self.assertEqual(installer.install("copilot", target, True, "zh-TW"), 0)
            local = target / ".github/skills/execute/SKILL.md"
            old = local.read_bytes()
            self.source_skill.write_bytes(old + b"\\n# Copilot update\\n")
            self.assertEqual(updater.update(target, apply=False), 0)
            self.assertEqual(local.read_bytes(), old)
            self.assertEqual(updater.update(target, apply=True), 0)
            self.assertIn(b"Copilot update", local.read_bytes())
            backup = next((target / ".agent-workflow/backups").iterdir())
            self.assertEqual(updater.rollback(target, backup.name, True), 0)
            self.assertEqual(local.read_bytes(), old)
            self.assertIn("zh-TW", (target / ".agent-workflow/language.md").read_text())

    def test_check_is_read_only_and_updates_with_backup(self):
        old = self.skill.read_bytes()
        self.source_skill.write_bytes(old + b"\n# Upstream update\n")
        self.assertEqual(updater.update(self.target, apply=False), 0)
        self.assertEqual(self.skill.read_bytes(), old)
        self.assertEqual(updater.update(self.target, apply=True), 0)
        self.assertIn(b"Upstream update", self.skill.read_bytes())
        backups = list((self.target / ".agent-workflow/backups").iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual(updater.rollback(self.target, backups[0].name, False), 0)
        self.assertIn(b"Upstream update", self.skill.read_bytes())
        self.assertEqual(updater.rollback(self.target, backups[0].name, True), 0)
        self.assertEqual(self.skill.read_bytes(), old)

    def test_local_conflict_is_not_overwritten(self):
        self.skill.write_text("my local customization\n", encoding="utf-8")
        self.source_skill.write_text("new upstream\n", encoding="utf-8")
        self.assertEqual(updater.update(self.target, apply=True), 0)
        self.assertEqual(self.skill.read_text(encoding="utf-8"), "my local customization\n")
        self.assertEqual(updater.update(self.target, apply=True, use_upstream={"execute"}), 0)
        self.assertEqual(self.skill.read_text(encoding="utf-8"), "new upstream\n")

    def test_preferences_language_and_custom_skills_survive(self):
        self.prefs.write_text("my preferences", encoding="utf-8")
        custom = self.target / ".cursor/skills/my-custom/SKILL.md"
        custom.parent.mkdir()
        custom.write_text("custom contents", encoding="utf-8")
        self.source_skill.write_text("new upstream", encoding="utf-8")
        self.assertEqual(updater.update(self.target, apply=True), 0)
        self.assertEqual(self.prefs.read_text(), "my preferences")
        self.assertIn("zh-CN", self.language.read_text())
        self.assertEqual(custom.read_text(), "custom contents")

    def test_rollback_rejects_edits_after_upgrade(self):
        self.source_skill.write_text("new upstream", encoding="utf-8")
        self.assertEqual(updater.update(self.target, apply=True), 0)
        backup = next((self.target / ".agent-workflow/backups").iterdir())
        self.skill.write_text("changed after upgrade", encoding="utf-8")
        self.assertEqual(updater.rollback(self.target, backup.name, True), 2)
        self.assertEqual(self.skill.read_text(), "changed after upgrade")

    def test_untracked_modified_legacy_install_is_not_overwritten(self):
        (self.target / ".agent-workflow/install-state.json").unlink()
        self.skill.write_text("legacy custom", encoding="utf-8")
        self.source_skill.write_text("new upstream", encoding="utf-8")
        self.assertEqual(updater.update(self.target, apply=True), 0)
        self.assertEqual(self.skill.read_text(), "legacy custom")


if __name__ == "__main__":
    unittest.main()
