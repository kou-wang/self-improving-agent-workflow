# v0.3.0 — GitHub Copilot support

**Status:** Prepared for release; publish only after the PR is merged and CI passes.

## New: GitHub Copilot

- `agent-workflow install --tool copilot --language en` installs the five existing Skills to `.github/skills/<name>/SKILL.md`.
- New `.github/copilot-instructions.md` points Copilot to local project rules, response language, and user preferences.
- `--tool all` installs for Cursor, Claude Code, and GitHub Copilot with a single Skills copy under `.claude/skills/` and all relevant project instructions.
- `--tool both` remains Cursor + Claude Code to preserve existing behavior.
- Managed Copilot Skill updates and guarded rollback use the existing non-overwriting updater and backup mechanism.

## Compatibility and safety

- Official releases before v0.3.0 continue to install for Cursor and Claude Code with the newer CLI; Copilot options require a v0.3.0 or newer release.
- The downloaded v0.3.0+ source archive must contain the new Copilot instruction template. Missing files fail safely.
- Existing preferences, local Skills, and project instructions are never silently replaced by an install.
- Multi-tool installations should select `--tool all` on a new project. Separate later installations into the same project may not share update tracking.

## Getting started

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
# Run inside an existing project directory, after v0.3.0 is published:
agent-workflow install --tool copilot --language en
```

See [Copilot setup](copilot.md) for supported surfaces and Skill activation.

## Verification and limits

- Python automated tests cover installer modes, release compatibility and archive safety, preservation of local files, Copilot upgrades, and rollback.
- **Real GitHub Copilot client behavior has not yet been fully smoke-tested.** Skills are typically selected contextually, and slash command availability varies among Copilot interfaces.
- This is still an early-access workflow, not an authorization mechanism, production-certified agent, or autonomous Skill-writing system.
