# Review Skill: developer-adaptive contract

## Inputs

- Accessible conversation including user's corrections and approvals.
- Skills actually used, inspected from current files rather than memory.
- Observed execution results and tests, where available.
- Applicable project rules and user preferences.

## Primary goal: adapt response quality and reduce repeated developer input

Review must inspect the developer's **actual corrections** to clarity, structure, terminology, order, depth, and business impact, even when no Skill was used before the Review. It should ask: *What had the developer to explain or correct again? Could the Agent have inferred it from accessible context or local preferences? Which repeat interaction would an approved edit avoid?* Do not count purposeful discussion or genuinely new decisions as wasted interaction. Preserve complete explanations rather than optimizing only for short outputs.

The initial preference file contains generalized RMA-derived answer patterns, which the developer can override repeatedly. Update the narrowest existing preference/Skill to avoid contradictory cumulative instructions. User preferences belong to the installed project, not to the shared upstream source.

## Classify each observed issue

- **Response / preference**: language, structure, clarity, explanation depth, business-first ordering, tone, terminology -> user preferences.
- **Process / workflow**: missing check, improper scope, unsafe handoff -> candidate core Skill (only if generalizable).
- **Project policy**: environment, permissions, data model or repository convention -> project rules.
- **One-time exception / no actionable issue**: do not persist.

## New and updated Skills

The purpose of Review is to **reduce repeated developer-agent interaction** by learning from observed corrections and recurring workflows. It can propose either:

- **Update an existing Skill:** when the relevant behavior is already in scope and needs clearer instructions or verification.
- **Create a new project-local Skill:** when a distinct, repeated activity has a reliable trigger, inputs, outputs, and permission boundaries. Recommend an explicit Skill name and full initial `SKILL.md` content. Avoid creating one for a single exception, an ordinary expression preference, or overlapping behavior.

New Skills accumulate as the developer's recurring needs become clear, but increased Skill count is not an optimization target. Keep project-specific Skills local and human-approved; do not automatically publish them to the shared repository. A proposal should identify which future question, handoff, or correction it would avoid. A Skill need not be part of a fixed pipeline; it should remain invocable independently with enough direct input.

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
