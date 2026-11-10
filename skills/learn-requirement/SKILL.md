---
name: learn-requirement
description: >-
  Clarify the intended user-visible outcome of a request from messages,
  screenshots, or other supplied context. Invoke explicitly to describe what
  is wanted without proposing implementation.
disable-model-invocation: true
---

# Learn Requirement

Turn a request into an accurate, concise, implementation-neutral description of the desired behavior. The purpose of this stage is to understand **what** the requester wants, not **how** to build it.

## Inputs

Use the user's request, attached screenshots, referenced product context, and other accessible evidence. If materials are missing, say so rather than inventing details.

Before responding, follow any available, applicable project-specific instructions and user response preferences. If none exist, use a clear, neutral style in the user's language. Project rules control **whether** files, data, and tools may be accessed or changed; this Skill never overrides them.

## Procedure

1. Read the exact wording and any screenshots together. Identify who is requesting a change, where the behavior appears, what action or state is expected, and what successful completion looks like.
2. Distinguish **observed current behavior**, **stated desired behavior**, and **unknowns**. Treat screenshots as evidence of what is visible, not proof of hidden system causes.
3. If necessary and permitted, inspect only enough relevant product context to clarify names, controls, or existing behavior. Stop researching once the request can be described accurately.
4. Clarify scope: Is this a one-time action, an ongoing behavior change, or ambiguous? Do not turn a one-time request into a permanent rule.
5. Produce the handoff below, omitting empty sections. Ask one focused question only when a missing detail prevents an accurate interpretation.

## Output / handoff

Start with a one- or two-sentence statement of the request in business or user-facing terms.

- **Requested outcome:** Who should be able to do what, in which context, and what should happen afterward.
- **Current behavior (if supported):** What is currently visible or verified, without attributing an unverified cause.
- **Problem to solve:** What is blocked, missing, or confusing for the requester.
- **Scope and constraints:** One-time versus ongoing, explicit exclusions, and any relevant acceptance conditions.
- **Open questions (only if needed):** Unknowns that materially change the meaning.

The resulting statement is the input to a later investigation or planning stage. Do **not** claim those stages have run.

## Guardrails

- Do not propose a fix, architecture, implementation sequence, or code changes unless the user explicitly requests them.
- Do not modify files, databases, settings, or external systems in this stage.
- Use terminology from the request and product interface. Explain technical names only when necessary for understanding.
- Do not include function names, fields, or file paths unless the user asks for implementation detail.
- Describe risks, data loss, or overwrites only when supported by evidence; label uncertainty explicitly.
- Never silently fill gaps with assumptions that change the scope.
