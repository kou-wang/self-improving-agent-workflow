# Initialization: useful defaults, then developer-owned improvement

A first install should work **before** the developer has trained any personalized Skills. The starter package is informed by a real RMA Cursor workflow; its **communication style** is generalized to other projects, but its private business rules, identifiers, servers, permissions, and commands are **not** included.

## What a new installation provides

- Five **independent** core Skills: `learn-requirement`, `investigate`, `make-plan`, `execute`, `review-skill`.
- `.agent-workflow/user-preferences.md`: populated RMA-derived response defaults, fully editable.
- `.agent-workflow/project-rules.md`: a **blank project-policy template** to avoid assuming any environment, database, permission, or business rule.
- `.agent-workflow/language.md`: chosen output language. Project terms and code identifiers remain exact.
- `.agent-workflow/install-state.json`: managed core Skill hashes to protect local modifications during updates.

## Default communication baseline

The response should help the developer **understand business behavior and make decisions**, not recite code. Defaults are **conclusion first**, **business impact first**, **short structured self-contained explanations**, evidence-backed cause and effect, and implementation detail only when it matters or is requested.

Use different shapes for different tasks:

| Task | Starter response shape |
|---|---|
| Simple question | Direct answer, usually 1–3 points |
| Requirement | Desired behavior → Current situation → Problem |
| Bug investigation | Expected vs actual → Cause → Impact → Fix direction → Urgency |
| Code review | Before/after behavior → Meaningful issues (scenario, consequence, fix) → Decisions if needed → Merge recommendation |
| Plan/design | Recommended approach → Why → Trade-offs; alternatives only if meaningful |
| Execution | Achieved/not achieved outcomes → Actual changes → Verification |
| Change summary | Before → After → Business impact |
| Skill review | Suggested change → Evidence → Repeated developer interaction avoided → Validation |

Omit headings when they do not improve clarity. Never report a hypothetical risk as a confirmed defect. Do not make the developer infer user impact from a function, file, or field name. The defaults are **editable preferences, not forced output schemas**.

## Natural usage (no required pipeline)

Common development flow:

`PM/Bug text or screenshot → /investigate or /learn-requirement → questions and adjustments → /make-plan → /execute`

But each Skill works alone:

- `/make-plan` can start from a new direct request without a prior investigation.
- `/execute` can act on a sufficiently specific, authorized direct request, without a prior plan.
- `/review-skill` can analyze response corrections from ordinary agent conversations without a previous Skill call.

A stage never authorizes an unrelated file change, database write, deployment, commit, or push. Project permissions and explicit user authorization still apply.

## Improve through normal work

1. Start with the initializer's usable defaults.
2. Work normally; when the developer corrects an explanation, ordering, terminology, missing check, or repeated handoff, keep that actual conversation as evidence.
3. `/review-skill` decides whether a **User Preference**, **existing Skill**, **Project Rule**, or a **new project-local Skill** is the narrowest justified change. A one-time exception may require **no change**.
4. The developer approves a specific proposal; a separately authorized edit applies it.
5. Verify a fresh conversation or realistic scenario. Repeat reviews as developer habits evolve.

Optimization target: **fewer avoidable developer inputs/corrections**, better explanations, and correct actions—not mandatory response brevity or an ever-growing Skill count.

## What upgrades do not overwrite

The installer skips existing local paths. The official updater uses stored hashes: locally edited core Skills produce a **conflict** and are kept by default. It does **not** replace user preferences, project rules, language settings, or custom Skills. A developer may explicitly choose an upstream version of an individual core Skill after review, with a backup.

**Existing users:** A package update deliberately does **not** inject the new starter defaults into their customized `user-preferences.md`. Read the [template](../templates/user-preferences.md) and selectively merge only the defaults you want. No silent preference migration.
