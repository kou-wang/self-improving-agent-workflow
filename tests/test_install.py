"""Regression tests for the onboarding installer. Run: python3 -m unittest discover -s tests -v"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts" / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()

    def test_dry_run_does_not_write(self):
        self.assertEqual(installer.install("cursor", self.project, False), 0)
        self.assertFalse((self.project / ".cursor").exists())
        self.assertFalse((self.project / ".agent-workflow").exists())

    def test_cursor_install_and_idempotence(self):
        self.assertEqual(installer.install("cursor", self.project, True), 0)
        skills = self.project / ".cursor" / "skills"
        for name in installer.SKILLS:
            self.assertTrue((skills / name / "SKILL.md").is_file())
        prefs = self.project / ".agent-workflow" / "user-preferences.md"
        prefs.write_text("personal rule\n", encoding="utf-8")
        skill = skills / "execute" / "SKILL.md"
        skill.write_text("local customization\n", encoding="utf-8")
        self.assertEqual(installer.install("cursor", self.project, True), 0)
        self.assertEqual(prefs.read_text(encoding="utf-8"), "personal rule\n")
        self.assertEqual(skill.read_text(encoding="utf-8"), "local customization\n")

    def test_both_installs_one_copy(self):
        self.assertEqual(installer.install("both", self.project, True), 0)
        self.assertTrue((self.project / ".claude/skills/review-skill/SKILL.md").is_file())
        self.assertFalse((self.project / ".cursor").exists())

    def test_language_options_and_preservation(self):
        for code in ("en", "zh-CN", "zh-TW"):
            with self.subTest(code=code):
                with tempfile.TemporaryDirectory() as temp:
                    target = Path(temp)
                    self.assertEqual(installer.install("cursor", target, True, code), 0)
                    language = target / ".agent-workflow" / "language.md"
                    self.assertEqual(language.read_text(encoding="utf-8"),
                                     f"# Agent response language\nLanguage: {code}\n")
                    self.assertEqual(installer.install("cursor", target, True, "en"), 0)
                    self.assertEqual(language.read_text(encoding="utf-8"),
                                     f"# Agent response language\nLanguage: {code}\n")

    def test_missing_target_fails_without_creation(self):
        target = self.project / "missing"
        self.assertEqual(installer.install("claude", target, True), 2)
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
