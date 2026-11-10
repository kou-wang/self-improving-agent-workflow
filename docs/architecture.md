# Architecture (V1 design)

## Five manually triggered stages

| Stage | Purpose | Handoff | Stop condition |
|---|---|---|---|
| Learn Requirement | Interpret the user request, without proposing implementation | Intended user-visible outcome, constraints, open questions | Request is unclear; do not guess |
| Investigate | Trace observed behavior to evidence and assess impact | Evidence, root cause or uncertainties, affected scope | Insufficient access/evidence; no data changes |
| Make Plan | Present verifiable outcomes and options, recommend a bounded approach | Approved outcomes, approach, exclusions, validation | Explicit approval absent; no implementation |
| Execute | Implement only the approved plan, respecting project rules | Changes, verification, remaining risks | Missing approval, unsafe operation or conflicting constraints |
| Review Skill | Assess observed gaps and propose instruction updates | Categorized findings, exact proposed edits, test cases | Human has not approved changes; never self-edit |

A stage may be invoked independently when sufficient prior context exists. No orchestration or automatic transition is included in V1.

## Configuration layers

1. **Core Skills**: general process and review criteria, shared across projects.
2. **Project rules**: allowed tools, environments, security and deployment constraints; the project owner owns these.
3. **User preferences**: communication language, ordering, preferred vocabulary, forbidden phrasings; the user owns these.

Skills must read applicable project constraints and preferences when they exist. Templates are not globally binding defaults.

## Review boundaries

Review the accessible conversation and the actual files/outputs; explicitly disclose missing context. Changes to project rules, preferences, or core Skills always require a human-approved separate edit step. Repeated or generalizable findings may justify a core Skill change; one-off project constraints should not leak into core.

## Compatibility strategy

Use one canonical set under `skills/<name>/SKILL.md`. After the Skills exist, a simple installer will copy them to `<project>/.cursor/skills/<name>/` or `<project>/.claude/skills/<name>/`. Do not install both sets in a project unless tested for duplicate discovery and precedence. An alternative common directory or symlink can be evaluated later.
