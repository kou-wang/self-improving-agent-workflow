---
name: make-plan
description: >-
  Turn a request already clarified in the conversation into a bounded,
  actionable plan with verifiable outcomes, prerequisites, and one recommended
  approach. Use explicitly when asked to plan a change or test, not to execute it.
disable-model-invocation: true
---

# Make Plan

Translate an **already established request** into a plan a person can review, approve, and carry out. Preserve the agreed problem, intended outcome, and scope; do not reinterpret the request or quietly broaden it.

**This Skill produces a plan only. Stop before implementing, editing files or data, creating commits, deploying, or invoking external write actions.**

## Inputs and authority

1. Read the relevant conversation, accessible requirement and investigation outputs, and any applicable project rules and user preferences. Do not claim earlier stages ran if their evidence is unavailable.
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

Follow the user's preferred language, ordering, and terminology when such preferences exist. Otherwise use a concise format with the **recommendation first**:

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

Ask the user to approve or revise the **outcomes and scope**, not merely a numbered option. If approval is partial, the subsequent execution must be limited to what was actually approved.

## Special case: test-only request

If the user asks for a **test plan**, do not turn it into an implementation plan. Provide setup/preconditions, test cases and steps, expected observable results, data/environment limits, cleanup needs, and explicit exclusions. Do not perform the tests in this stage.

## Non-negotiable boundaries

- Never expand a one-time correction into a permanent policy or a local fix into a system-wide rewrite without explicit approval.
- An instruction such as "handle it the existing way" is not an executable step: specify the real operation and preconditions.
- Do not silently add requirements or changes to adjacent workflows.
- Do not use implementation-specific identifiers when the user wants only outcome-level planning; include them when they materially improve executable precision.
- If information is unavailable, describe the uncertainty and the smallest check that would resolve it.
- Do not change code, data, configuration, permissions, branches, or any external state. The plan ends here.
