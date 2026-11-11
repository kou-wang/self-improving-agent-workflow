# Changelog

All notable user-facing changes will be tracked here when publishing releases.
Version tags follow SemVer (`vMAJOR.MINOR.PATCH`).

## 0.3.0 — in development (not yet published)

- Add first-class GitHub Copilot installation (`--tool copilot`), Copilot project instructions, and a shared three-agent install mode (`--tool all`).
- Extend versioned Skill update/rollback to Copilot and add release archive compatibility checks.
- Document Copilot activation differences and test limitations; maintain existing Cursor/Claude behavior.

## 0.2.1 — published 2026-11-10

- Add MIT License and align package metadata for public reuse.
- Update public onboarding and release documentation to match shipped v0.2.0 functionality.
- Clarify early-access verification limitations and separate CLI vs. Skill upgrades.

## 0.2.0 — published 2026-11-10

- New installations seed an editable, generalized RMA-derived response baseline instead of a blank preference template, plus non-overwriting always-on project rules for Cursor and Claude Code.
- Answer defaults emphasize business consequences, concise structured explanations, and task-appropriate response patterns.
- `make-plan` and `execute` now explicitly support direct standalone invocation; they reuse earlier Skill findings when available but do not require them.
- `review-skill` prioritizes real expression corrections and avoided developer interaction, including ordinary conversations without prior Skill use.
- Documented initialization, personalization, and safe upgrade behavior; added installer default-content regression assertions.
- The release CLI keeps backward compatibility with v0.1.0 archive structure while validating new always-on rule templates in newer releases.
- Local customizations remain protected; existing installations do not have their user preferences silently replaced.

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
- [x] Confirm tests pass for the final release commit.
- [ ] Manually smoke-test the full lifecycle in a fresh Cursor project.
- [ ] Manually smoke-test the full lifecycle in a fresh Claude Code project.
- [ ] Verify conflicting local customizations and rollback in both.
- [ ] License added in v0.2.1 preparation; not part of the original v0.1.0 tag.
- [x] Publish an initial version tag.
