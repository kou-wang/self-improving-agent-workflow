# Self-Improving Agent Workflow — Detailed Overview

> A technical and practical guide to the five core skills, project rules, review loop, onboarding, upgrades, and early-access limitations.

**[← Back to the homepage](../README.md)** · [Quickstart](quickstart.md) · [CLI](cli.md) · [Initialization](initialization.md)

## 1. Why this project exists

Coding agents are often capable of implementing a task but inconsistent about explanation order, project-specific constraints, or which steps require developer intervention. Repeating instructions in every conversation is inefficient. This project provides a small set of reusable Skills and a project-local place to preserve preferences.

The goal is **fewer unnecessary corrections**, not more automation for its own sake. The workflow also aims to preserve explicit human control over consequential actions.

This is a set of text instructions, local configuration and a CLI; it is not a new model, agent runtime, autonomous daemon or automatic model-training system. Changes do not propagate to unrelated projects automatically.

## 2. Exactly five core skills

| Skill | Input | Output / boundary |
| --- | --- | --- |
| [`learn-requirement`](../skills/learn-requirement/SKILL.md) | A request, message, screenshot or feature description | Clarifies the intended user-visible behavior; no implementation |
| [`investigate`](../skills/investigate/SKILL.md) | A failure, error, unexpected behavior or affected object | Verifiable evidence and causal analysis; read-only |
| [`make-plan`](../skills/make-plan/SKILL.md) | A direct task or relevant earlier findings | Recommended path, trade-offs and validation; no implementation |
| [`execute`](../skills/execute/SKILL.md) | A sufficiently clear authorized request or approved plan | Changes and verification within actual project permissions |
| [`review-skill`](../skills/review-skill/SKILL.md) | Real conversation and task results, including corrections | Proposed reusable changes to preferences, rules or Skills; proposal-only |

**Independent by design.** There is no required call sequence. `/make-plan` does not require `/investigate`; `/execute` does not require `/make-plan` when a direct instruction is sufficiently specific and authorized. A common—but optional—path is requirement/investigation → plan → execute → review.

### When not to invoke a skill

Do not force the user through all five stages for a simple question or a clear small change. Use the smallest relevant Skill; a normal conversation without any Skill is also valid. A review may consider a pattern found in ordinary dialogue, provided there is actual evidence.

## 3. Review is the improvement loop

A typical interaction is **not a series of long, scripted prompts**. The user may paste a bug screenshot or trace log, discuss it briefly, and invoke `/investigate` without restating the context. If the explanation is too technical, they can simply ask, “Explain it more simply and keep the English technical terms.” The conversation continues naturally. After the task, `/review-skill` can inspect that correction and propose saving a response preference so the developer does not need to repeat it. It may also propose improving an existing Skill or creating a justified new project-local Skill.

**Applying approved changes:** once the developer accepts a proposal, use a separate authorized `/execute` to edit the relevant file; use `/make-plan` first only when the change benefits from planning. Review itself never writes preferences or Skills.

The most important distinction is **proposed** versus **applied** improvement:

1. **Observe:** Collect actual examples of avoidable rework, repeated clarification, wording corrections, incorrect handoffs or process gaps.
2. **Classify:** Decide whether the issue belongs in user preferences, project rules, an existing core/project Skill, or a genuinely new project-local Skill. Treat one-off exceptions as one-offs.
3. **Propose:** Name the smallest useful change, its evidence, expected benefit, and how to verify it. Review itself must not edit files.
4. **Approve separately:** The developer decides whether to apply the proposal. File modifications then require an explicitly authorized action, e.g. via `/execute`.
5. **Check:** Confirm a later interaction benefits from the adjustment. If not, revise or revert the rule.

### Where should an improvement live?

| Observation | Appropriate home |
| --- | --- |
| “Lead with business impact, not field names” | `.agent-workflow/user-preferences.md` |
| “Never run write operations against production without explicit approval” | `.agent-workflow/project-rules.md` |
| “Investigation reports should separate observed state from assumptions” | The relevant Skill, if broadly reusable |
| “Our team repeatedly uses a distinct workflow not covered by the five” | New **project-local** Skill, when supported by evidence |
| “This answer is a one-time exception” | Keep in the current task; do not create a permanent rule |

Project configurations and Skills remain editable; a review proposal should not silently modify either. These instructions cannot grant permissions or override organizational policies.

## 4. First-install defaults and project structure

New installations include generalized response preferences derived from a practical software-development workflow: **conclusion first; user-visible behavior and impact before implementation details; concise, structured, evidence-based explanations**.

The templates are generic. They contain no private business data, proprietary code, credentials, or RMA system-specific instructions.

Typical project-local structure (exact Skill location depends on `--tool`):

```text
project/
  .agent-workflow/
    project-rules.md         # permissions and project-specific boundaries
    user-preferences.md      # developer-owned response preferences
    language.md              # en, zh-CN, zh-TW
    install-state.json       # version and managed core Skill hashes
  .cursor/skills/            # when --tool cursor
  .claude/skills/            # when --tool claude, both or all
  .github/skills/            # when --tool copilot
  .cursor/rules/agent-workflow.mdc      # when Cursor enabled
  .claude/rules/agent-workflow.md       # when Claude enabled
  .github/copilot-instructions.md      # when Copilot enabled
```

For `--tool all`, a **single** `.claude/skills/` set is shared, with each agent’s own project instruction file. The installer will not silently create a second unmanaged set of Skills when an existing tracked installation points to another location. See [Copilot setup](copilot.md).

**Existing local files are not overwritten.** This means a newly released template will not replace personal preferences or established project rules. Review and merge desired starter changes manually.

## 5. Setup and daily use

Prerequisites: Python 3.10+, Git, pipx and an existing project directory. Install the CLI through GitHub:

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
```

In the project, choose the intended agent and language:

```bash
agent-workflow install --tool cursor --language en --check
agent-workflow install --tool cursor --language en
```

Other tool modes are `claude`, `copilot`, `both` (Cursor + Claude Code), and `all` (all three). Language codes are `en`, `zh-CN`, and `zh-TW`.

If the agent does not discover the Skills immediately, reopen/restart its project or agent session, ensure the relevant Skills directory exists, and consult your client-specific setup guide. Exact activation shortcuts and automatically selected Skills differ by client; especially for Copilot, do not assume slash commands always exist.

### Realistic example

```text
User: /investigate — Clicking Save shows success, but refreshing discards changes.
Agent: Verifies the observable flow and identifies what is known vs. unknown.
User: /make-plan — Recommend a fix and show how to validate it. Do not implement.
Agent: Proposes a supported, bounded plan.
User: /execute — Implement the approved plan.
Agent: Reports actual edits, tests, outcomes, and remaining uncertainty.
User: /review-skill — I had to ask twice for the user-visible impact.
Agent: Proposes a targeted, reusable preference or Skill adjustment; does not edit.
```

## 6. Updates, preservation, and rollback

The CLI program and managed Skill content are **different update surfaces**:

```bash
# Update installed CLI code (e.g. when new tool options become available)
pipx upgrade self-improving-agent-workflow

# Preview and update official core Skills from the latest stable GitHub Release
agent-workflow update --check
agent-workflow update

# Use the backup ID shown in the update output
agent-workflow rollback BACKUP_ID
agent-workflow rollback BACKUP_ID --apply
```

The installer does not overwrite existing Skills or config. The updater uses tracked hashes to protect locally edited official Skills and leaves project-specific custom Skills alone. An applied update records backups. Rollback refuses to overwrite changes made after the update.

The updater is not fully transactional across multiple files; an interrupted update may require manual recovery from backup. GitHub Release archives are inspected and restricted, but downloads are not cryptographically signed or attested. See [CLI](cli.md) and [Upgrading](upgrading.md) for the full model.

## 7. Platform support

| Agent | Skill location / instruction | Notes |
| --- | --- | --- |
| Cursor | `.cursor/skills/`; `.cursor/rules/agent-workflow.mdc` | A single project rule points to preferences and boundaries |
| Claude Code | `.claude/skills/`; `.claude/rules/agent-workflow.md` | Project-scoped response defaults; runtime behavior depends on client support |
| GitHub Copilot | `.github/skills/`; `.github/copilot-instructions.md` | Available from v0.3.0, early-access real-client validation |

The five canonical Skill files are shared conceptually; installation layout and agent invocation affordances differ. Client support and instruction compliance can change with agent versions. See [Cursor](cursor.md), [Claude Code](claude-code.md), and [Copilot](copilot.md).

## 8. Safety, testing, and limitations

- **Authority:** No Skill grants database, production, deployment, external-repository or other write permissions. Explicit authorization and applicable project policies still apply.
- **Stage boundaries:** `learn-requirement`, `investigate`, `make-plan` and `review-skill` are non-implementing; `execute` is for authorized work.
- **Testing:** Python installer, CLI, mocked GitHub Release, update and rollback tests run in CI. A CLI upgrade and fresh Cursor installation were exercised manually. Full behavior across all supported agent client versions is not comprehensively validated.
- **Learning:** “Self-improving” means humans may approve adjustments to local instruction files. It does **not** imply autonomous learning, continuous execution, or cross-project synchronization.
- **Privacy:** Do not expose credentials, source code, proprietary prompts or private chat transcripts in public examples or GitHub Issues.

## 9. Contributing and next steps

When reporting an issue, include the release version, selected tool mode, host application/version, command, expected behavior and observed behavior, with sensitive data removed. Browse the [roadmap](../TODO.md) for future work; suggestions are not promises of shipped functionality.

The project is licensed under [MIT](../LICENSE). [Open an issue](https://github.com/kou-wang/self-improving-agent-workflow/issues).
