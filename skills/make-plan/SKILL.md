---
name: make-plan
description: >-
  Independently plan a task from the user's current request and available
  project or conversation context. Recommend a feasible approach, show meaningful
  alternatives, and define verifiable outcomes without implementing.
disable-model-invocation: true
---

# Make Plan

Turn **either a direct request or an existing conversation decision** into a plan a person can review, approve, and carry out. This Skill is standalone: do not require a prior `learn-requirement` or `investigate` invocation. Reuse their findings if they exist; otherwise inspect the relevant project context yourself, as allowed. Preserve the user's intent and scope; do not quietly broaden either.

**This Skill produces a plan only. Stop before implementing, editing files or data, creating commits, deploying, or invoking external write actions.**

**Local configuration:** Before following this Skill, read `.agent-workflow/project-rules.md`, `.agent-workflow/user-preferences.md`, and `.agent-workflow/language.md` in the active project if present. Use `language.md` for the response language (`en` = English, `zh-CN` = Simplified Chinese, `zh-TW` = Traditional Chinese), while keeping code identifiers and user-specified exact terminology unchanged. Project rules never grant permission beyond actual tool or user authorization.

## Inputs and authority

1. Read the **current request first**, then any relevant accessible conversation, requirement/investigation findings if present, project rules, and user preferences. Never require the user to repeat known information or invoke another Skill as a prerequisite. Do not claim earlier stages ran when they did not.
2. Establish **who needs what**, **what is true now**, **what success would look like**, and **whether the action is one-time or ongoing**.
3. If the goal, critical constraints, authorization, or target environment is materially unresolved, identify exactly what must be decided and stop. Never default silently to local, staging, production, or any other potentially consequential target.
4. Treat project-specific permissions and safety constraints as authoritative. A suggested plan is **not** permission to perform its steps.

## Planning procedure

1. **Fix the scope.** Restate the accepted problem and explicit exclusions. Separate confirmed facts from hypotheses and unknowns.
2. **Find feasible approaches.** Inspect only the information needed to determine whether each approach can actually achieve the agreed outcome. State feasibility limits; do not list speculative approaches as ready to execute.
3. **Define independently approvable results.** Describe each observable outcome separately. Surface any newly persisted data, new ongoing behavior, change to an additional operation, destructive effect, or irreversible side effect as its own approval item. Explicitly state when no new persistent data is introduced.
4. **Recommend one approach.** Give concrete ordered steps, owners when known, prerequisites, stop conditions, validation and rollback/recovery considerations where relevant. Only present alternative approaches when they differ meaningfully in outcome, trade-offs, or risk; do not generate alternatives just to reach a quota.
5. **Check coverage.** Map each problem or requirement already raised in the conversation to a concrete plan step. Mark anything not addressed as **not covered** rather than obscuring it.
6. **Stop for human review.** The user can accept, reject, or modify individual outcomes. Never treat the recommended approach as approved merely because it was written.

## Output / handoff

Follow the user's preferred language, ordering, and terminology, including the RMA-derived defaults from the installed preferences. Explain proposed **business behavior and impact before implementation mechanics**. Otherwise use a concise format with the **recommendation first**; omit empty or redundant headings rather than forcing a lengthy report:

### Recommendation: outcomes to approve

List the proposed, verifiable outcomes separately. Indicate who performs each when established; distinguish one-time actions from ongoing behavior. Call out storage, data-loss, scope, and behavior changes.

### Recommended approach

- **What changes:** Scope and intended user-visible results.
- **How:** Specific ordered actions that someone with appropriate access can execute.
- **Before starting:** Required evidence, decisions, permissions, dependencies, and stop-if conditions.
- **After completion:** Acceptance checks, expected new state, consequences, and recovery if applicable.
- **Out of scope:** What this plan intentionally does not change.

### Alternatives (only when meaningful)

Explain the different outcome, prerequisites, risks, and trade-offs; do not restate the preferred approach in other words. Do not present an infeasible approach as recommended.

### Requirement coverage

For each explicitly raised issue, identify the recommended step that addresses it. Label gaps **not covered**.

### Approval required

Ask the user to approve or revise the **outcomes and scope**, not merely a numbered option. If approval is partial, a later execution must be limited to what was actually approved. Do not insist that the user run any other Skill first. A user can also invoke `execute` directly on an independently clear, authorized task.

## Special case: test-only request

If the user asks for a **test plan**, do not turn it into an implementation plan. Provide setup/preconditions, test cases and steps, expected observable results, data/environment limits, cleanup needs, and explicit exclusions. Do not perform the tests in this stage.

## Non-negotiable boundaries

- Never expand a one-time correction into a permanent policy or a local fix into a system-wide rewrite without explicit approval.
- An instruction such as "handle it the existing way" is not an executable step: specify the real operation and preconditions.
- Do not silently add requirements or changes to adjacent workflows.
- Do not use implementation-specific identifiers when the user wants only outcome-level planning; include them when they materially improve executable precision.
- If information is unavailable, describe the uncertainty and the smallest check that would resolve it.
- Do not change code, data, configuration, permissions, branches, or any external state. The plan ends here.
