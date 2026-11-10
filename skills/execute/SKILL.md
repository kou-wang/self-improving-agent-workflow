---
name: execute
description: >-
  Implement only the outcomes and approach explicitly approved in the conversation.
  Use when the user explicitly asks to execute an agreed plan or make the
  previously approved changes; do not treat a proposed plan as authorization.
disable-model-invocation: true
---

# Execute

Carry out the **approved outcomes**, within the agreed scope and the project's permissions. Implement the selected approach, verify observable results, and report exactly what did and did not happen. Do not reopen the plan, quietly add adjacent work, or claim success based on an attempted action.

**Local configuration:** Before following this Skill, read `.agent-workflow/project-rules.md` and `.agent-workflow/user-preferences.md` in the active project if present. Project rules never grant permission beyond actual tool or user authorization.

## Inputs and authority

1. Read the latest relevant plan **and subsequent decisions or corrections** in the accessible conversation. The later explicit decision takes precedence over an earlier recommendation. If the history or plan is unavailable, do not invent approval.
2. Identify separately: **approved outcomes**, the **approved approach**, **explicit exclusions**, and **success checks**. A recommendation is not approval. If several approaches remain open and the user has not selected one, stop and request a decision.
3. Read applicable project rules, permissions, and user response preferences. Project-specific rules determine allowed tools, repositories, branches, environments, data writes, approvals, and delivery conventions. This Skill grants no permissions.
4. Before any potentially destructive, irreversible, production, external-system, or data-changing action, confirm that the specific action and target are authorized under the applicable rules. General permission to implement code does not authorize database writes, deployments, pushes, or releases.

## Execute in order

1. **Preflight.** Inspect only the files, state, dependencies, and relevant environment needed for the approved work. Identify existing user changes and avoid overwriting or discarding them. Establish a baseline when useful.
2. **Confirm the change boundary.** Map each approved outcome to a concrete edit or action and an observable check. Do not add a new feature, migration, refactor, cleanup, side effect, or unrelated file change without approval.
3. **Handle working context safely.** If an existing issue, branch, or change request is explicitly designated, work in that context when permitted. Do not silently switch or create branches. Preserve unrelated uncommitted work. A branch switch must not carry uncommitted changes into the wrong branch; if safe restoration is not possible, stay put and explain.
4. **Implement the approved changes.** Prefer the smallest coherent change that satisfies all approved outcomes. Respect the project's data, security, privacy, and external-service rules. Stop before any operation whose target or authorization is unresolved.
5. **Verify.** Run relevant checks and tests that are safe and available. Inspect observable results and check each approved outcome independently. Distinguish a static check, local test, integration test, and confirmed deployed behavior. Do not claim a check ran when it did not.
6. **Assess the actual result.** Report partial completion honestly. If a required step fails, do not silently substitute a different approach, broaden the scope, or turn the failure into an unapproved follow-up action.

## Commit, push, deployment, and data changes

- **Default for code changes:** leave them **uncommitted and unpushed**. Do not open or merge a pull/merge request or deploy without separate explicit authorization or an already applicable project instruction that specifically permits that operation.
- **Database or external state mutations:** execute only specifically approved operations against the explicitly authorized target. Check scope and safety controls first; report what actually ran, the affected scope when known, and any failures. Never invent a successful mutation from a command that merely started.
- **Irreversible or sensitive actions:** if authorization, target, side effects, or rollback expectations are unclear, stop at that boundary and describe what needs a decision.
- **Existing changes:** never reset, discard, overwrite, or relocate unrelated work to make the plan easier.

## Report / handoff

Follow project/user preferences for language, terminology, and answer order. Lead with the **complete list of approved outcomes**, not just the number of completed tasks or a sample.

For each outcome, use a separate status:
- **✅ Achieved:** State the behavior or result and the evidence that supports it.
- **❌ Not achieved:** State the blocking point and what remains; do not represent it as success.
- **⚠️ Not verified:** An edit or action was performed but its effect could not be confirmed; state why.

Then briefly report:
1. **Changes made:** User-visible behavior first; technical file/command details where useful or requested. Distinguish code edits from data or external-system changes.
2. **Verification:** Exact tests/checks run, results, and what was not tested.
3. **Delivery state:** Whether files remain uncommitted, which branch/context contains them, and whether any external state was changed.
4. **Risks and next decision:** Only meaningful remaining issues or required approvals.

Keep mixed outcomes separate: do not use one sentence to claim success and failure simultaneously. If the approved results form a complete checklist, account for every item.

## Stop conditions

Stop at the relevant boundary and report rather than guessing when:
- The approved plan, selected approach, scope, or target is missing or contradictory.
- Project rules require permission not yet granted.
- An action would affect a prohibited environment, object, or side effect.
- Proceeding would endanger unrelated work, data, or credentials.
- New evidence invalidates the agreed plan or requires an additional outcome.
- Verification reveals failure that cannot be repaired within the approved scope.

**Handoff:** Provide the actual execution record for later `review-skill` use. Do not invoke review automatically or edit the shared Skills in response to an execution mistake.
