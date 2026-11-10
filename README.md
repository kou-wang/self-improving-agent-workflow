# Self-Improving Agent Workflow

A human-controlled, review-driven workflow for AI coding agents.

**Status: foundation scaffold (not yet a working Skill package).** The five Skills and review evaluation logic will be migrated in subsequent steps. Currently targeting **Cursor** and **Claude Code** only.

## Concept

`Learn Requirement → Investigate → Make Plan → Execute → Review Skill`

Every stage is invoked intentionally, not automatically chained. The review stage identifies issues grounded in the actual conversation and work outcome, proposes targeted improvements, and requires human approval before changing any instruction.

## Design principles

- **Evidence before changes:** Do not extrapolate an incident into a universal rule.
- **Approval gates:** Planning stops before implementation; review proposes changes without applying them.
- **Separation of concerns:** Shared Skills, project constraints, and personal response preferences live separately.
- **No implicit side effects:** No push, commit, deployment, or data mutation without project-specific authorization.
- **Verify revisions:** A proposed fix needs at least one concrete regression scenario and an explicit verification result.
- **Honest boundaries:** Chat history may be incomplete. No automatic learning or improvement is promised without a supported implementation.

## Repository layout

```text
skills/                     # Canonical Skill definitions (coming next)
templates/user-preferences.md
                           # Project-local response preferences template
templates/project-rules.md # Project constraints template
docs/architecture.md       # Stages, boundaries, and handoffs
docs/review-design.md      # Review issue taxonomy and approval process
docs/cursor.md             # Cursor installation design
docs/claude-code.md        # Claude Code installation design
tests/review-scenarios/    # Regression cases (coming next)
scripts/                   # Optional installer (not yet implemented)
```

## Roadmap

1. ✅ Inventory existing Cursor Skills and design a public foundation.
2. ☐ Extract five generic Skills without proprietary content.
3. ☐ Add review proposal format, approval, and verification cases.
4. ☐ Validate installation and manual invocation in Cursor.
5. ☐ Validate installation and manual invocation in Claude Code.
6. ☐ Add CI checks and publish a tested release.

## Security and provenance

This repository must not contain the source project's `.cursor` directory, internal infrastructure details, code, credentials, or private conversation excerpts. The public package is rewritten from generalized behavior, not copied wholesale from the source project.

## License

License pending author selection. Do not redistribute as an open-source licensed project until a license is chosen and added.
