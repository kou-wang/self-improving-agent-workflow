# Self-Improving Agent Workflow

**Make your coding agent adapt to you—not the other way around.** A human-in-the-loop workflow that learns from concrete developer feedback by proposing updates to existing Skills **or creation of new project-specific Skills**. The goal is to reduce repetitive corrections, explanations, and developer-agent interaction over time. Supports **Cursor** and **Claude Code**.

**Start here: [New user Quickstart](docs/quickstart.md)** — clone, install, configure, use all five stages, and review proposed improvements.

## Install (preview first)

```bash
git clone https://github.com/kou-wang/self-improving-agent-workflow.git
cd self-improving-agent-workflow
python3 scripts/install.py --tool cursor --target /path/to/your-project --language zh-CN
python3 scripts/install.py --tool cursor --target /path/to/your-project --language zh-CN --apply
```

Use `--tool claude` for Claude Code, or `--tool both` to share one install in a project that uses both tools. The installer **never overwrites** existing Skills or local configuration. It requires only Python 3 and an existing project directory. See the [Quickstart](docs/quickstart.md) for the end-to-end process.

## Language: one flag, three options

Choose `--language en` (English), `--language zh-CN` (简体中文), or `--language zh-TW` (繁體中文) during installation. English is the default. To change later:

```bash
python3 scripts/set_language.py --target /path/to/your-project --language zh-TW
python3 scripts/set_language.py --target /path/to/your-project --language zh-TW --apply
```

Only `.agent-workflow/language.md` is changed; personal preferences and existing Skills are preserved. Restart the agent session if necessary. Exact identifiers and requested terminology are not translated.

## Workflow

`Learn Requirement → Investigate → Make Plan → Execute → Review Skill`

1. **Learn Requirement** — establish what success looks like, without implementation proposals.
2. **Investigate** — trace actual evidence, root cause, and affected scope, without writes.
3. **Make Plan** — present bounded, verifiable outcomes; stop for approval.
4. **Execute** — implement only approved outcomes, verify results; no commit/push by default.
5. **Review Skill** — examine real friction and failures, propose an update to an existing Skill or a **new project-local Skill** when a distinct repeated workflow warrants one. The developer approves before any file change.

Stages have **no automatic orchestration**. `investigate` may be selected automatically; the other four require explicit invocation. Review proposals require human approval and separately authorized application. The agent becomes better tailored through approved, persisted project Skills—not automatic unattended learning.

## Layout

- [`skills/`](skills/) — one canonical copy of each Skill
- [`docs/quickstart.md`](docs/quickstart.md) — complete onboarding and smoke test
- [`scripts/install.py`](scripts/install.py) — dry-run-first, non-overwriting project installer
- [`templates/`](templates/) — project-local rules and user preferences
- [`docs/architecture.md`](docs/architecture.md) — stage contracts and boundaries
- [`docs/review-design.md`](docs/review-design.md) — review categories and validation
- [`docs/cursor.md`](docs/cursor.md) / [`docs/claude-code.md`](docs/claude-code.md) — tool-specific details
- [`tests/review-scenarios/`](tests/review-scenarios/) — planned regression scenarios

## Principles

Evidence before rules; meaningful approvals before writes; project constraints separate from reusable Skills; no destructive overwrite during installation; verification reports distinguish static checks, behavioral checks and confirmed outcomes.

## Project status

Five Skills and an onboarding installer exist in the repository. Compatibility smoke tests in real Cursor and Claude Code sessions and regression tests are **not yet completed**. Do not treat this as a certified stable release.

## License

License selection pending. No open-source license granted until a license is explicitly added.

## Security

Do not publish proprietary instructions, private chat transcripts, internal systems, credentials or company data in issues or examples.
