# GitHub Copilot support (v0.3.0+)

The five Agent Workflow Skills can be installed for GitHub Copilot, including Copilot agent mode in VS Code and supported Copilot agent surfaces. Exact Skill activation and visibility depend on your Copilot client and version. GitHub documents the project directory `.github/skills/<name>/SKILL.md` and the repository-wide instructions file `.github/copilot-instructions.md`.

Official references: [GitHub — Add agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) and [GitHub — Repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/configure-custom-instructions/add-repository-instructions-in-your-ide).

## Install

The following requires the **v0.3.0 or newer CLI and GitHub Release**. If only v0.2.1 is published, these options cannot be installed from the official release yet.

Install the CLI once, then in an existing project directory:

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
agent-workflow install --tool copilot --language en
```

For an already-installed CLI, run `pipx upgrade self-improving-agent-workflow` first.

Use `--check` to preview installation, or `--language zh-CN` / `--language zh-TW` for other response languages.

### File layout

```text
your-project/
  .github/
    skills/
      learn-requirement/SKILL.md
      investigate/SKILL.md
      make-plan/SKILL.md
      execute/SKILL.md
      review-skill/SKILL.md
    copilot-instructions.md
  .agent-workflow/
    project-rules.md
    user-preferences.md
    language.md
    install-state.json
```

The instructions file references your project-local preferences, project rules and language. It does not override organization policies, GitHub permissions or explicit approvals.

### Using Copilot together with Cursor and Claude Code

For **a new project**, `agent-workflow install --tool all` installs the Skills once in `.claude/skills/`, which all three compatible agents can discover, and installs project instructions for Cursor, Claude Code, and Copilot.

The existing `--tool both` continues to mean **Cursor + Claude Code** (it does not include Copilot). If an existing tracked installation uses a different Skills directory, the installer refuses to create a second unmanaged copy. Choose `--tool all` on a new project, or migrate the existing installation intentionally before changing tool modes. The installer also preserves any existing `.github/copilot-instructions.md`; merge preferences manually if you already use that file.

## Use the Skills

Ask Copilot's agent to use a named Skill, for example:

```text
Use the investigate skill to examine why "Saved" appears but the change disappears after refresh.
Distinguish evidence from hypotheses. Do not modify files.
```

Copilot generally **selects Skills based on context**; Skill availability and whether a `/skill-name` shortcut appears vary by client. Do not assume that every Copilot interface exposes the same slash commands as Cursor.

After a task, ask for `review-skill` to **propose**, not automatically apply, improvements to your reusable preferences or Skills.

## Upgrade

```bash
pipx upgrade self-improving-agent-workflow
agent-workflow update --check
agent-workflow update
```

Upgrades preserve existing project preferences and untracked custom Skills; changed official Skills require an explicit upstream choice before replacement. Update uses backups for rollback. Re-running `install` adds missing files only, without overwriting existing instructions.

## Validation status

- Python unit tests cover Copilot installation, dry run, non-overwrite behavior, official release archives, managed Skill updates and rollback.
- **Live Copilot agent behavior has not yet been verified** on each supported Copilot surface. Treat this as early-access support until real-client validation is completed.
- Copilot code review and cloud agent have different capabilities and may not follow every workflow in the same way as VS Code agent mode.
