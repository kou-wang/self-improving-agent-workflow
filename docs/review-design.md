# Review Skill: developer-adaptive contract

## Inputs

- Accessible conversation including user's corrections and approvals.
- Skills actually used, inspected from current files rather than memory.
- Observed execution results and tests, where available.
- Applicable project rules and user preferences.

## Classify each observed issue

- **Response / preference**: language, tone, terminology, structure -> user preferences.
- **Process / workflow**: missing check, improper scope, unsafe handoff -> candidate core Skill (only if generalizable).
- **Project policy**: environment, permissions, data model or repository convention -> project rules.
- **One-time exception / no actionable issue**: do not persist.

## New and updated Skills

The purpose of Review is to **reduce repeated developer-agent interaction** by learning from observed corrections and recurring workflows. It can propose either:

- **Update an existing Skill:** when the relevant behavior is already in scope and needs clearer instructions or verification.
- **Create a new project-local Skill:** when a distinct, repeated activity has a reliable trigger, inputs, outputs, and permission boundaries. Recommend an explicit Skill name and full initial `SKILL.md` content. Avoid creating one for a single exception, an ordinary expression preference, or overlapping behavior.

New Skills accumulate as the developer's recurring needs become clear, but increased Skill count is not an optimization target. Keep project-specific Skills local and human-approved; do not automatically publish them to the shared repository. A proposal should identify which future question, handoff, or correction it would avoid.

## Review output (proposals only)

For every finding include: evidence (what happened), gap, category, target existing file **or new Skill path**, exact proposed addition/change **or complete new Skill draft**, repeated developer interaction avoided, risks or overgeneralization, a reproduction/regression scenario, and proposed verification method. Mark uncertain findings as uncertain; recommend no edit when current instructions already cover the behavior.

## Approval and verification

1. Present proposed edits; do **not** write files.
2. Human accepts or rejects each proposed change.
3. A separate execution step applies only accepted edits.
4. Check for structural validity and conflict with other rules.
5. Run the original case and at least one counterexample where practical; distinguish static instruction checks from behavioral tests.
6. Record validation results and unresolved limitations. Never claim guaranteed prevention of future model mistakes.

## Privacy

Use anonymized examples. No copying of personal conversations, company-specific screenshots, internal hostnames or confidential identifiers into the public repository.
