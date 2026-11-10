# Architecture (V1 design)

## Five independently invocable Skills

| Stage | Purpose | Handoff | Stop condition |
|---|---|---|---|
| Learn Requirement | Interpret the user request, without proposing implementation | Intended user-visible outcome, constraints, open questions | Request is unclear; do not guess |
| Investigate | Trace observed behavior to evidence and assess impact | Evidence, root cause or uncertainties, affected scope | Insufficient access/evidence; no data changes |
| Make Plan | Plan from a new request **or** previous findings; recommend a bounded approach | Proposed outcomes, alternatives, exclusions, validation | Stops without implementing; material ambiguity identified |
| Execute | Act on direct explicit instructions **or** an approved plan, respecting project rules | Changes, verification, remaining risks | Insufficient authorization, unsafe operation, or conflicting constraints |
| Review Skill | Assess observed gaps and propose instruction updates | Categorized findings, exact proposed edits, test cases | Human has not approved changes; never self-edit |

Every Skill can be invoked on its own, including from the user's current request alone; prior Skill calls are never prerequisites. Conversation context is reused when available. No orchestration or automatic transition is included in V1.

## Configuration layers

1. **Core Skills**: general process and review criteria, shared across projects.
2. **Project rules**: allowed tools, environments, security and deployment constraints; the project owner owns these.
3. **User preferences**: starts with generalized RMA-derived response defaults, then evolves through the user's approved corrections; the user owns these. The selected language stays in a separate local file.

The installer copies **ready-to-use defaults** at first install. Skills read applicable project constraints and preferences. A short **always-on project rule** also points every Cursor/Claude chat at those settings, even when no Skill is invoked. Defaults apply only inside that project; the installer and updater must not overwrite preferences or other local customizations.

## Review boundaries

Review the accessible conversation and the actual files/outputs; explicitly disclose missing context. Changes to project rules, preferences, or core Skills always require a human-approved separate edit step. Repeated or generalizable findings may justify a core Skill change; one-off project constraints should not leak into core.

## Compatibility strategy

Use one canonical set under `skills/<name>/SKILL.md`. After the Skills exist, a simple installer will copy them to `<project>/.cursor/skills/<name>/` or `<project>/.claude/skills/<name>/`. Do not install both sets in a project unless tested for duplicate discovery and precedence. An alternative common directory or symlink can be evaluated later.
