# Self-Improving Agent Workflow

**Make your coding agent adapt to you—not the other way around.** A human-in-the-loop workflow that learns from concrete developer feedback by proposing updates to existing Skills **or creation of new project-specific Skills**. The goal is to reduce repetitive corrections, explanations, and developer-agent interaction over time. Supports **Cursor** and **Claude Code**.

**Start here: [New user Quickstart](docs/quickstart.md) · [Initialization defaults](docs/initialization.md) · [CLI setup / updates](docs/cli.md)** — install a useful starter Skill set, invoke any Skill independently, and personalize it through approved review.

## Recommended CLI workflow (after the first stable Release)

Install the CLI once:

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
```

In your project:

```bash
agent-workflow install --tool cursor --language zh-CN
agent-workflow update
```

No recurring `git pull` is needed for Skill updates. **There is no stable GitHub Release yet**, so release-based installation/updates currently report a clear error. This is intentionally not a production-ready promise; see [CLI documentation](docs/cli.md).

## Legacy development install (preview first)

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

## Legacy local-checkout upgrades

Update the source checkout, preview the managed Skill changes, then apply:

```bash
git pull --ff-only
python3 scripts/update.py --target /path/to/your-project --check
python3 scripts/update.py --target /path/to/your-project --apply
```

Locally edited official Skills are kept by default; custom Skills and your language/preferences are not touched. Each applied update creates a backup with a rollback ID. See [Upgrade and rollback guide](docs/upgrading.md) for conflict handling, manual merging, and rollback. **Current version: pre-release; no stable release tag yet.**

## Initialization and flexible workflow

New installations include **five ready-to-use independent Skills** and **RMA-derived response defaults** (business impact first, conclusion first, concise structured explanation, task-specific response patterns). These defaults are generalized: no internal RMA business rules, infrastructure, or data are shipped. The developer can refine them repeatedly through `review-skill`. See [Initialization defaults](docs/initialization.md).

A common but **optional** path is:

`Bug / feature feedback → /investigate or /learn-requirement → discussion → /make-plan → /execute`

- **Learn Requirement:** explain the desired user-visible behavior; no code change.
- **Investigate:** trace the actual problem and practical impact; read-only.
- **Make Plan:** use either direct input or relevant conversation findings; recommend one feasible approach and meaningful alternatives.
- **Execute:** act on a **clear direct instruction** or an approved plan, with permissions and safety checks; it does **not** require a prior planning Skill.
- **Review Skill:** learn from real corrections about **response quality** and **avoidable user interaction**; propose preference updates, existing Skill changes, or justified new project-local Skills.

No mandatory stage order or automatic orchestration exists. All Skills can be invoked independently. Project/data/production safety gates still apply. Review proposals require human approval and separately authorized application; updates never silently replace local customizations.

## Layout

- [`skills/`](skills/) — one canonical copy of each Skill
- [`docs/quickstart.md`](docs/quickstart.md) — complete onboarding and smoke test
- [`docs/initialization.md`](docs/initialization.md) — starter Skills, RMA-derived expression defaults, and personalization
- [`scripts/install.py`](scripts/install.py) — dry-run-first, non-overwriting project installer
- [`scripts/update.py`](scripts/update.py) — version-aware upgrade with conflict protection and rollback
- [`agent_workflow/cli.py`](agent_workflow/cli.py) — `agent-workflow` CLI using stable GitHub Releases
- [`docs/cli.md`](docs/cli.md) — first-time CLI install and no-pull updates
- [`templates/`](templates/) — project-local rules and user preferences
- [`docs/architecture.md`](docs/architecture.md) — stage contracts and boundaries
- [`docs/review-design.md`](docs/review-design.md) — review categories and validation
- [`docs/cursor.md`](docs/cursor.md) / [`docs/claude-code.md`](docs/claude-code.md) — tool-specific details
- [`tests/review-scenarios/`](tests/review-scenarios/) — planned regression scenarios

## Principles

Evidence before rules; meaningful approvals before writes; project constraints separate from reusable Skills; no destructive overwrite during installation; verification reports distinguish static checks, behavioral checks and confirmed outcomes.

## Roadmap

See [TODO.md](TODO.md) for upcoming work, including **token efficiency**, **configurable read/write database access**, and **GitHub/GitLab integrations**. These are planned and not yet implemented.

## Project status

Five Skills, an onboarding installer, and a packaged GitHub Releases CLI exist in the repository. The CLI's release-dependent operations cannot run until a stable Release is published. Compatibility smoke tests in real Cursor and Claude Code sessions and regression tests are **not yet completed**. Do not treat this as a certified stable release.

## License

License selection pending. No open-source license granted until a license is explicitly added.

## Security

Do not publish proprietary instructions, private chat transcripts, internal systems, credentials or company data in issues or examples.
