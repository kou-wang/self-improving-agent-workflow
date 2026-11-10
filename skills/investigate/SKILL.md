---
name: investigate
description: >-
  Investigate a reported failure, unexpected behavior, error message, screenshot,
  or affected object by tracing observable evidence through the relevant code,
  logs, records, and system boundaries. Use when a user asks why something failed,
  what an error means, or what state an operation left behind.
---

# Investigate

Find out **what happened**, **why it happened**, **what is affected**, and **what is still unknown**. Start with the user's observation; follow the actual execution path to the specific value, decision, or event responsible. Classify the failure *before* recommending a fix.

This stage investigates. It does **not** modify source code, database records, configuration, production state, or external services.

## Read project context first

1. Read applicable project rules and user communication preferences if present. They determine terminology, permitted environments, data access, confidentiality, and reporting style.
2. Do not invent an environment, database, log store, or access method. Never assume local, staging, or production is the intended target.
3. Obtain permission when project rules require it. If a choice of target materially changes the investigation and has not been established, ask rather than silently choosing one.
4. Observe the least-privilege principle: use read-only queries and non-mutating commands. Do not attempt a write to prove a hypothesis.
5. If sources are unavailable, describe the limitation; do not imply they were checked.

## 1. Capture the reported evidence

Extract and preserve, when available:

- The **exact** error or unexpected result, including meaningful variable text.
- The user's action, expected outcome, actual outcome, and relevant time.
- The affected object(s) and their identifiers, redacted when reporting outside the project.
- Any apparent successful steps shown alongside the failure.

For messages with generic boilerplate and variable details, separate them. Search the distinctive variable fragment first; the generic advice or recovery sentence is not itself proof of what failed.

A success banner may describe an earlier operation. A button or status visible in the UI is not proof that a server-side write completed.

## 2. Locate the decision or failure boundary

If authorized repository access exists:

1. Search for the exact distinctive message, then a shorter unique fragment if needed.
2. Trace the entry point, caller, callee, validation, error handling, and relevant external-system boundary.
3. Identify the failed condition: which values, states, or predicates were checked and where they came from.
4. Determine when an event or record is written, whether partial success is possible, and which state only changes after success.
5. For batch operations, distinguish a single request from per-item events or errors. Do not infer request counts from row counts.

If the message originates in an external system, trace the caller and available request/response evidence. Never claim to have examined the external implementation without access.

## 3. Correlate logs and records

Use the relevant, **authorized** logs or records to associate the report with a concrete attempt. Prefer a distinctive error fragment, correlation ID, and time window over a guessed identifier.

- Inspect actual schemas or models before composing queries; never assume a table or field exists.
- Inspect the full relevant request/response *when safe and permitted*, not just the message text. Minimize unnecessary sensitive data.
- Treat an absent log entry as a clue, not conclusive proof: the failure could precede logging, occur in a different system/environment, or be unlogged.
- Label every statement as **verified**, **inferred**, or **unknown** when ambiguity matters.

## 4. Trace provenance and changes over time

For the value or state that caused the rejection:

1. Find the record, configuration, user input, or external payload from which it was selected.
2. Find the expected value or rule, and the record against which it was compared.
3. Follow the earlier event or transition that created the mismatch. A current value may differ from the value at creation time.
4. When two views or lists disagree, identify which each operation reads and writes.
5. Check whether the discrepancy is isolated to one object, shared by a class of objects, or dependent on time/environment.

Do not call a mismatch a code defect until the intended behavior is established. Separate a user action, authorized maintenance change, system-generated update, and unverified manual modification.

## 5. Establish the user-visible state

Determine what completed, what failed, what was rolled back, and what remains persisted. Distinguish a requested operation, an attempted operation, and a confirmed persisted result.

Explain what a retry is expected to do **based on evidence**. Do not recommend repeating an unchanged deterministic failure. Do not assume later downstream operations ran merely because an earlier stage succeeded.

## 6. Classify the issue

Use the narrowest evidence-backed classification:

- **Data/configuration mismatch:** Persisted or supplied values violate the rule being enforced.
- **Application/workflow defect:** Code chooses the wrong value, applies the wrong rule, or leaves an allowed workflow in an impossible state.
- **Expected behavior:** The observed rejection matches the intended rule; explain the prerequisite.
- **External/dependency failure:** Another service or system rejected or did not complete the operation, with evidence of the boundary.
- **Undetermined:** Evidence is missing or contradictory; give the smallest useful next check.

A classification may be provisional. State competing explanations when evidence cannot distinguish them. Separate **existing affected records** from **future operations**.

## Report / handoff

Lead with a plain-language summary of what failed and its impact, not a dump of raw fields. Use the user's preferred language and vocabulary if provided.

1. **What happened:** Action, expected vs. observed behavior, and which parts succeeded.
2. **Why:** Rejected value/condition, its source, and the chain of evidence; identify uncertainty.
3. **Impact and current state:** Affected objects/users, persisted state, retry implications, existing vs. future scope.
4. **Recommended next step:** Data correction, code correction, user action, dependency investigation, or more evidence. Distinguish recommendation from authorization.
5. **Urgency:** Evidence-based severity and reason, not a guessed priority.

Attach concise evidence next to important claims (file/function, log reference, record/field, or test result). Do not expose secrets or unnecessary personal data. If no root cause is verified, say so explicitly.

The handoff may inform **make-plan**, but does not authorize **execute**. Stop after the investigation report; no edits, commits, deployments, or state-changing remediation in this stage.
