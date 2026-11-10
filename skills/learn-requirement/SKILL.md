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

**Local configuration:** Before following this Skill, read `.agent-workflow/project-rules.md`, `.agent-workflow/user-preferences.md`, and `.agent-workflow/language.md` in the active project if present. Use `language.md` for the response language (`en` = English, `zh-CN` = Simplified Chinese, `zh-TW` = Traditional Chinese), while keeping code identifiers and user-specified exact terminology unchanged. Project rules never grant permission beyond actual tool or user authorization.

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

Lead with **what the requester wants**, in one or two plain-language sentences: who, where, what behavior, and what happens afterward. Then use these short sections when they add value:

- **Current situation:** What the user sees or what existing behavior has actually been verified.
- **Problem to solve:** What is missing or blocked, and what would become possible after the change.
- **Scope / question (only if material):** One-time versus ongoing, a supported exclusion, or a single ambiguity that changes the requirement.

Prefer the project's RMA-derived response defaults in `.agent-workflow/user-preferences.md`; if the user has customized them, those choices win. Do not pad the response with headings or technical implementation detail.

This Skill is **standalone**. Its result may inform later discussion, planning, or execution, but none of those Skills is required to have run, and invoking this Skill does not invoke them.

## Guardrails

- Do not propose a fix, architecture, implementation sequence, or code changes unless the user explicitly requests them.
- Do not modify files, databases, settings, or external systems in this stage.
- Use terminology from the request and product interface. Explain technical names only when necessary for understanding.
- Do not include function names, fields, or file paths unless the user asks for implementation detail.
- Describe risks, data loss, or overwrites only when supported by evidence; label uncertainty explicitly.
- Never silently fill gaps with assumptions that change the scope.
