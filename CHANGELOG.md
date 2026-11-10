# Changelog

All notable user-facing changes will be tracked here when publishing releases.
Version tags should follow SemVer (`vMAJOR.MINOR.PATCH`) once the release process has been validated.

## Unreleased — RMA-derived initialization and independent Skills

- New installations seed an editable, generalized RMA-derived response baseline instead of a blank preference template, plus non-overwriting always-on project rules for Cursor and Claude Code.
- Answer defaults emphasize business consequences, concise structured explanations, and task-appropriate response patterns.
- `make-plan` and `execute` now explicitly support direct standalone invocation; they reuse earlier Skill findings when available but do not require them.
- `review-skill` prioritizes real expression corrections and avoided developer interaction, including ordinary conversations without prior Skill use.
- Documented initialization, personalization, and safe upgrade behavior; added installer default-content regression assertions.

## 0.1.0 — published 2026-11-10

- Five separate Skills: learn-requirement, investigate, make-plan, execute, review-skill.
- Review proposes improvements to an existing Skill or a new project-local Skill, with explicit developer approval.
- Project-local language selection: English, Simplified Chinese, Traditional Chinese.
- Dry-run-first installer for Cursor and Claude Code, with non-overwrite behavior.
- Initial managed installation state (version + SHA-256 hashes).
- Safe local-checkout updater: check/apply, keep-local default, opt-in use-upstream, backups and guarded rollback.
- Documentation for onboarding, manual workflow, and upgrades.
- Packaged `agent-workflow` CLI for installation and upgrades using stable GitHub Releases (no recurring git pull).
- Mocked offline CLI tests, including missing releases, unsafe release contents, and custom Skill preservation.
- Automated Python regression test definitions.

### Validation originally tracked for this release (not all complete)

- [x] Confirm installer, updater and CLI automated tests pass in the previously inspected GitHub Actions run (#39).
- [ ] Confirm tests still pass for the final release commit.
- [ ] Manually smoke-test the full lifecycle in a fresh Cursor project.
- [ ] Manually smoke-test the full lifecycle in a fresh Claude Code project.
- [ ] Verify conflicting local customizations and rollback in both.
- [ ] Choose and add an explicit license.
- [ ] Publish an initial version tag after validation.
