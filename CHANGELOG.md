# Changelog

All notable user-facing changes will be tracked here when publishing releases.
Version tags should follow SemVer (`vMAJOR.MINOR.PATCH`) once the release process has been validated.

## Unreleased — 0.1.0-dev

- Five separate Skills: learn-requirement, investigate, make-plan, execute, review-skill.
- Review proposes improvements to an existing Skill or a new project-local Skill, with explicit developer approval.
- Project-local language selection: English, Simplified Chinese, Traditional Chinese.
- Dry-run-first installer for Cursor and Claude Code, with non-overwrite behavior.
- Initial managed installation state (version + SHA-256 hashes).
- Safe local-checkout updater: check/apply, keep-local default, opt-in use-upstream, backups and guarded rollback.
- Documentation for onboarding, manual workflow, and upgrades.
- Automated Python regression test definitions.

### Before the first stable release

- [ ] Confirm automated installer and updater tests pass in CI.
- [ ] Manually smoke-test the full lifecycle in a fresh Cursor project.
- [ ] Manually smoke-test the full lifecycle in a fresh Claude Code project.
- [ ] Verify conflicting local customizations and rollback in both.
- [ ] Choose and add an explicit license.
- [ ] Publish an initial version tag after validation.
