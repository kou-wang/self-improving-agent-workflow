<div align="center">

# Self-Improving Agent Workflow

### Five skills. One feedback loop. An agent that adapts to you.

**Stop repeating how you want your coding agent to work.**

[![Latest release](https://img.shields.io/github/v/release/kou-wang/self-improving-agent-workflow?style=for-the-badge)](https://github.com/kou-wang/self-improving-agent-workflow/releases/latest) [![CI](https://img.shields.io/github/actions/workflow/status/kou-wang/self-improving-agent-workflow/installer-smoke.yml?branch=main&style=for-the-badge&label=tests)](https://github.com/kou-wang/self-improving-agent-workflow/actions) [![MIT](https://img.shields.io/github/license/kou-wang/self-improving-agent-workflow?style=for-the-badge)](LICENSE)

**Cursor** · **Claude Code** · **GitHub Copilot**

[Get started](#-quick-start) · [Explore the 5 skills](#-the-five-core-skills) · [How it works](#-how-it-works) · [Detailed guide](docs/overview.md)

</div>

---

## ✨ The idea

**An agent can finish a task and still make you repeat yourself next time.** This project installs five reusable, independent coding-agent skills alongside editable project preferences. After a real interaction, `review-skill` can **propose** improvements to the instructions that shape future responses.

> **Self-improving ≠ self-modifying.** Changes are evidence-based, proposed for human review, and applied only after separate authorization. No background training or automatic cross-project memory.

## 🧭 How it works

```mermaid
flowchart TB
    Request["Your task or feedback"]
    subgraph Skills["Five independent core skills"]
        direction LR
        Learn["01 · learn-requirement"]
        Investigate["02 · investigate"]
        Plan["03 · make-plan"]
        Execute["04 · execute"]
        Review["05 · review-skill"]
    end
    Request -. "invoke any skill directly" .-> Learn
    Request -.-> Investigate
    Request -.-> Plan
    Request -.-> Execute
    Request -.-> Review
    Learn -. "optional handoff" .-> Plan
    Investigate -. "optional handoff" .-> Plan
    Plan -. "after approval" .-> Execute
    Execute -. "feedback" .-> Review
    Review --> Proposal{"Human approves?"}
    Proposal -- "yes: separate authorized edit" --> Adapt["Preferences · Rules · Existing or new Skill"]
    Proposal -- "no" --> Keep["Keep current behavior"]
    Adapt -. "guide future work" .-> Request
    classDef skill fill:#eaf3ff,stroke:#3478c0,color:#14365b
    classDef decision fill:#fff4db,stroke:#b47b1a,color:#4f370e
    class Learn,Investigate,Plan,Execute,Review skill
    class Proposal decision
```

<p align="center"><sub>Optional paths, not a mandatory pipeline. A clear request can go straight to <code>make-plan</code> or <code>execute</code>.</sub></p>

## 🧩 The five core skills

| Skill | When to use it | Output |
| :--- | :--- | :--- |
| **[01 · Learn Requirement](skills/learn-requirement/SKILL.md)** | Understand a feature request or screenshot | Expected user-visible behavior, without implementation |
| **[02 · Investigate](skills/investigate/SKILL.md)** | Trace a bug or unexpected state | Evidence, cause when known, impact, and unknowns — **read-only** |
| **[03 · Make Plan](skills/make-plan/SKILL.md)** | Choose an implementation approach | Recommended plan, trade-offs, verification — **no edits** |
| **[04 · Execute](skills/execute/SKILL.md)** | Carry out a clear, authorized task | Actual changes and validation, within approved boundaries |
| **[05 · Review Skill](skills/review-skill/SKILL.md)** | Stop repeating a correction or preference | Proposed reusable improvement — **no automatic edits** |

## ⚡ Quick start

Install the CLI once (**Python 3.10+**, Git and [pipx](https://pipx.pypa.io/) required):

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
```

Run inside an **existing project directory**:

```bash
# Pick one: cursor | claude | copilot | both | all
agent-workflow install --tool cursor --language en
```

| Agent | Install option |
| :--- | :--- |
| Cursor | `--tool cursor` |
| Claude Code | `--tool claude` |
| GitHub Copilot | `--tool copilot` |
| Cursor + Claude Code | `--tool both` |
| All three | `--tool all` |

Languages: **English `en` · 简体中文 `zh-CN` · 繁體中文 `zh-TW`**. Add `--check` to preview installation. The installer preserves existing files.

## 🔁 Turn feedback into reusable improvements

```text
You:    /investigate — “Saved” appears, but changes disappear on refresh.
Agent:  Explains observed behavior, evidence, and what remains unknown.

You:    /review-skill — I had to ask twice for the business impact.
Agent:  Proposes an edit to user-preferences.md (or a relevant Skill).

You:    Approve the proposed change and authorize applying it.
Result: Your project instructions can guide future responses.
```

**Key features:** independent skills · editable response defaults · project-scoped instructions · safe non-overwriting installs · managed Skill updates · backups and guarded rollback.

## 📚 Go deeper

**[Complete overview →](docs/overview.md)** — design philosophy, project layout, review loop, configuration, upgrade safety, and limitations.

[Quickstart](docs/quickstart.md) · [Cursor](docs/cursor.md) · [Claude Code](docs/claude-code.md) · [Copilot](docs/copilot.md) · [CLI / upgrades](docs/cli.md) · [Roadmap](TODO.md)

---

<sub>**Early access · v0.3.0** — Python CI is passing; real-client behavior is not exhaustively validated. Instructions do not guarantee agent compliance. Do not place secrets or private project information in public issues. [MIT License](LICENSE) · [Report an issue](https://github.com/kou-wang/self-improving-agent-workflow/issues)</sub>
