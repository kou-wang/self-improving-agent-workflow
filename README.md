# Self-Improving Agent Workflow

**Make your coding agent adapt to you—not the other way around.**

A lightweight, human-approved set of **five independent Skills** for [Cursor](https://cursor.com/) and [Claude Code](https://claude.com/product/claude-code). Clarify requirements, investigate bugs, plan and execute changes, then use real feedback to **propose better instructions for next time**.

**[Quickstart](docs/quickstart.md) · [How personalization works](docs/initialization.md) · [CLI & upgrades](docs/cli.md) · [Latest release](https://github.com/kou-wang/self-improving-agent-workflow/releases/latest)**

> **Early access (v0.2.1).** The Python installer and CLI have automated tests, and a CLI upgrade plus fresh Cursor project installation have been exercised. Full behavior across Cursor/Claude Code versions and complete end-to-end rollback scenarios are **not yet verified**.

## Why use it?

Coding agents can solve tasks yet still require repeated explanations of *what matters*, *how to explain it*, and *which workflows to follow*. This project starts with usable, editable response defaults—**conclusion first, user-visible behavior and impact before code details, concise but complete**—and provides a review process for turning **specific corrections** into reusable improvements.

- **Start anywhere.** Use one Skill without running the others first.
- **Keep control.** Review suggests changes; modifying Skills or preferences requires your approval and a separate authorized action.
- **Keep your setup.** Installation does not overwrite existing files. Upgrades protect locally edited Skills and support backups/rollback.
- **Project-scoped defaults.** Cursor and Claude Code receive an always-on project rule pointing to local preferences and project rules, even outside Skill calls.

This is a **human-in-the-loop instruction workflow**, not an autonomous agent, background learner, or model-training system. It does not learn across unrelated projects unless you explicitly carry changes over.

## Install in your project

**Prerequisites:** Python 3.10+, Git, [pipx](https://pipx.pypa.io/), and an existing project directory. This CLI is installed from GitHub, **not PyPI**.

Install the CLI once:

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
```

Then open a terminal **inside your own project**:

```bash
agent-workflow install --tool cursor --language en
```

Use `--tool claude` for Claude Code or `--tool both` for both. Languages: `en`, `zh-CN`, `zh-TW`. To preview first, add `--check` to the installation command.

Open or restart the project in your coding agent. Your installation now contains five Skills, editable settings under `.agent-workflow/`, and the relevant project rule. See the [step-by-step guide](docs/quickstart.md) if Skills do not appear.

## The five Skills

| Skill | Use it when… | What it does |
| --- | --- | --- |
| [`/learn-requirement`](skills/learn-requirement/SKILL.md) | A request or screenshot is ambiguous | Describes the intended user-visible result without jumping to implementation |
| [`/investigate`](skills/investigate/SKILL.md) | A bug, error, or unexpected state needs explanation | Traces available evidence and separates confirmed causes from unknowns; read-only |
| [`/make-plan`](skills/make-plan/SKILL.md) | You need an implementation approach | Proposes scope, trade-offs, verification, and a recommended plan; does not change files |
| [`/execute`](skills/execute/SKILL.md) | You have a clear action to take | Carries out an authorized request or approved plan within project safety rules |
| [`/review-skill`](skills/review-skill/SKILL.md) | The agent repeatedly misses your preferred behavior | Reviews actual interactions and proposes targeted Skill, rule, or preference improvements; does not apply them |

**No mandatory pipeline:** call `/make-plan` directly for a known feature or `/execute` directly for a sufficiently specific, authorized change. The progression below is only an example.

## Example: from feedback to a better workflow

**1. Investigate a report**

```text
/investigate
The app shows "Saved", but the change disappears after refresh.
What happened, what is affected, and what is still unknown?
```

The Skill should distinguish the visible success message from evidence of persistence, rather than assume a database cause.

**2. Decide what to change**

```text
/make-plan
Recommend a fix with verification steps. Do not implement yet.
```

**3. Apply only when authorized**

```text
/execute
Implement the approved plan and report what was verified.
```

**4. Improve future responses**

```text
/review-skill
I had to ask twice for the user-visible impact.
Propose a reusable change so future explanations lead with that impact.
```

Review **proposes** an edit to a Skill, a project rule, or `.agent-workflow/user-preferences.md`. You decide whether to apply it. You can invoke `/review-skill` after ordinary chats too; no preceding Skill is required.

## What gets installed?

```text
your-project/
├── .cursor/skills/          # or .claude/skills/ (one copy for --tool both)
│   ├── learn-requirement/
│   ├── investigate/
│   ├── make-plan/
│   ├── execute/
│   └── review-skill/
├── .cursor/rules/agent-workflow.mdc  # Cursor, when selected
│   # OR .claude/rules/agent-workflow.md for Claude Code
└── .agent-workflow/
    ├── project-rules.md       # your project constraints and permissions
    ├── user-preferences.md    # editable starter response style
    ├── language.md            # selected response language
    └── install-state.json     # version and managed Skill hashes
```

The initial style is generalized from a real development workflow; it includes **no proprietary RMA system details**. Customize the files for your project. Existing preferences and rules are not silently replaced by new defaults.

## Updates and rollback

```bash
# Update the CLI implementation (separate from updating Skills)
pipx upgrade self-improving-agent-workflow

# Check, then update installed core Skills from the latest stable GitHub Release
agent-workflow update --check
agent-workflow update

# Preview rollback using the backup ID printed by an update
agent-workflow rollback BACKUP_ID
agent-workflow rollback BACKUP_ID --apply
```

To add missing project rule files to an older installation, rerun `agent-workflow install --tool cursor --language en`; it skips existing files. Changes to the CLI itself require the separate `pipx upgrade` command. See [upgrade details](docs/upgrading.md) and [CLI limitations](docs/cli.md).

## Scope, safety, and limitations

- `/learn-requirement`, `/investigate`, and `/make-plan` do not implement changes. `/review-skill` only proposes improvements.
- `/execute` does not grant database, deployment, production, or repository permissions; project rules and explicit authorization still govern those operations.
- Instructions do **not** guarantee model compliance. Always verify consequential code/data changes yourself.
- The updater preserves local edits by default, but is **not fully transactional** across files. It relies on GitHub-hosted releases, without signed-release attestations.
- Please keep credentials, internal code, and private conversation content out of public issues.

## Documentation and community

[Cursor guide](docs/cursor.md) · [Claude Code guide](docs/claude-code.md) · [Architecture](docs/architecture.md) · [Review design](docs/review-design.md) · [Roadmap](TODO.md) · [Changelog](CHANGELOG.md)

Feedback and reproducible bug reports are welcome via [GitHub Issues](https://github.com/kou-wang/self-improving-agent-workflow/issues). Include the CLI version, coding agent, command, expected behavior, and observed result—**without secrets or proprietary data**.

**License:** [MIT](LICENSE).
