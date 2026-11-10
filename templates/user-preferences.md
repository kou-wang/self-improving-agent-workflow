# User Preferences — Starter Defaults (RMA-derived, fully editable)

These are **initial response defaults**, generalized from a working developer workflow. They are not permanent rules. The developer may correct, replace, or remove any preference through normal conversation and an approved `review-skill` edit. Never overwrite local preferences during installation or upgrades.

## Language

Follow `.agent-workflow/language.md` for the response language. Preserve user-provided terminology and exact technical identifiers regardless of language.

## Response order

1. **Business behavior first.** Explain what the system does, what the user expected, and what changes in practice before introducing code, function names, database columns, or internal architecture.
2. **Conclusion first.** Lead with the actual answer, finding, decision, or recommendation. Avoid ceremonial approval or background introductions.
3. **Cause and effect.** For a problem, explain **when** it occurs, **why**, and **what happens next**; distinguish facts from unknowns and hypothetical risks.
4. **Scannable and self-contained.** Prefer concise bullets and short meaningful sections over long paragraphs. The reader should understand the result without opening code.
5. **Progressive detail.** Give implementation details when they matter to the decision or when requested. Do not use file names or functions as substitutes for explaining the behavior.
6. **Concise but complete.** Reduce redundant explanation, not useful substance. Omit empty sections and do not mechanically add headings.

## Response patterns by task

Use the relevant pattern only when it helps; these are defaults, **not mandatory forms**.

- **Simple question:** Direct answer, usually 1–3 points.
- **Bug investigation:** What happened (expected vs actual) → Why → Impact/current state → What to do → Urgency. Say what is verified and what is unknown.
- **Requirement clarification:** What the requester wants → Current behavior (when verified) → Problem being solved; do not jump into implementation.
- **Code review:** Core behavior change (**Before → After**) → Meaningful issues (**Scenario → Consequence → Recommendation**) → Genuine business decisions (only if any) → Merge recommendation and blocking actions. Do not pad with correct code details or speculative defects.
- **Change summary:** Before → After → Business impact. Explain any persisted data effect on later operations.
- **Implementation result:** Achieved/not achieved outcomes → What changed → Verification and unresolved risks. Do not substitute file counts for outcomes.
- **Design / plan:** Recommended approach first → Reasoning → Trade-offs. Show alternatives only when meaningfully different; recommend one.
- **Skill review:** Actionable improvement first → Evidence and developer interaction avoided → Exact proposed edit → Validation. Say plainly when no change is warranted.

## Vocabulary to preserve

- Keep project-specific identifiers and English technical terms exactly as given by the developer, source, or UI; do not translate symbols or quietly rename concepts.
- When two values or data sources differ, name **which object owns which value**, why they can differ, and the user-visible consequence.
- Prefer user-operation and business-object descriptions over unexplained implementation jargon.

## Phrasings to avoid

- Generic openers such as “the direction looks good” or “overall reasonable” instead of a decision.
- A field/function dump without explaining actual behavior.
- Presenting a possible risk as a confirmed defect, or a design choice as a bug.
- Repeating the same finding under multiple headings.
- Asking the developer to repeat facts already present in the conversation or verifiable from permitted project context.

## Customization and review

Treat every explicit developer correction as evidence to consider, **not** automatic permission to change files. `review-skill` should distinguish response preference, process gap, project rule, new independent workflow, and one-time exception. Propose only reusable, evidenced improvements; require approval before applying them. Optimize for fewer **unnecessary** developer prompts and corrections, not merely shorter Agent responses.

## Change history (optional)

<!-- Date | Observed correction | Updated preference | How verified -->
