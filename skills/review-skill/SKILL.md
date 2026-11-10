---
name: review-skill
description: >-
  Review Skills actually used in the accessible conversation against observed
  behavior, outcomes, and user corrections. Propose evidence-based improvements
  to existing or new project Skills, core Skills, project rules, or user preferences; do not apply changes.
disable-model-invocation: true
---

# Review Skill

Review what **actually happened** against the instructions **actually in effect**. Help the agent adapt to its developer over repeated real tasks, so the developer spends less time repeating corrections, clarifying conventions, or manually prompting routine workflows. Identify reusable fixes without turning a one-time incident into a universal rule. The number of Skills may grow when a proven, distinct recurring workflow justifies a new one; growth is not itself a goal.

**This stage is proposal-only. Do not edit Skill files, rules, preferences, tests, or any other files; do not commit, push, or execute corrective actions.** Human approval and a separate execution step are required for every proposed change.

**Local configuration:** Before following this Skill, read `.agent-workflow/project-rules.md`, `.agent-workflow/user-preferences.md`, and `.agent-workflow/language.md` in the active project if present. Use `language.md` for the response language (`en` = English, `zh-CN` = Simplified Chinese, `zh-TW` = Traditional Chinese), while keeping code identifiers and user-specified exact terminology unchanged. Project rules never grant permission beyond actual tool or user authorization.

## 1. Establish review scope and evidence

1. Identify Skills **actually used in this conversation**, including Skills supplied by the user. Do not review every installed Skill by default. A Skill merely discussed, proposed, or installed is not necessarily used.
2. Re-read the **current contents** of each in-scope Skill, including linked instructions actually governing its behavior. Do not rely on remembered or summarized versions.
3. Read applicable **project rules**, **user preferences**, and `.agent-workflow/language.md` if available. Do not assume a file or convention exists. Identify the actual instruction source for each behavior.
4. Collect concrete evidence from the accessible conversation, task artifacts, observed edits, test results, and explicit user corrections. For each candidate issue, identify the behavior, intended outcome, and evidence of mismatch.
5. If conversation history, files, execution results, or instruction versions are unavailable, disclose the gap. Do not claim complete review or infer a missing event.
6. If an instruction was updated during the conversation, compare the observation against its **latest text**. Do not propose a fix already present there. If the behavior preceded the update, distinguish that timing.

Review only gaps **demonstrated in the accessible task**. Do not generate speculative failure lists or invent feedback to justify a change.

## 2. Determine whether a change is warranted

For each observed issue:

- **Instruction gap:** Was the desired behavior absent or ambiguous in the governing instructions?
- **Execution error:** Did the Agent violate an instruction that was already clear? A repeated violation might warrant clearer checks or examples, but rewriting a correct rule is not automatically justified.
- **Missing evidence:** Is the apparent problem only an unverified interpretation or incomplete history?
- **Already resolved:** Does the current instruction already cover the correction?
- **One-off exception:** Was it an isolated request or a preference the user later withdrew?

Prefer **no change** for unverified, already-covered, withdrawn, or one-time behavior. Only propose a change that follows from evidence and has a concrete mechanism for avoiding recurrence.

## 3. Route findings to the right ownership layer

| Finding | Target | Reason |
|---|---|---|
| Response language, ordering, vocabulary, phrasing, style | User preferences | User- or project-local communication choices |
| Environment, data permissions, business rules, delivery conventions | Project rules | Project-local constraints that must not enter the shared package |
| A reusable missing step, handoff, approval gate, or verification check | Existing core Skill | Generalizable workflow behavior |
| Repeated, distinct project workflow with reliable inputs, outputs, triggers, and boundaries | New project-local Skill | Developer-specific capability that does not belong in a generic core Skill |
| Repeated project workflow already covered by an existing Skill | Update that Skill | Avoid duplicating or fragmenting Skills |
| No actionable gap | No file | Do not persist noise |

Distinguish **Response Review** (communication), **Process Review** (how stages were followed), and **Outcome Review** (whether the task actually succeeded). A bad outcome alone does not prove a Skill defect. Prefer updating an existing Skill. Propose a **new** Skill only when evidence shows a distinct recurring workflow, with a clear trigger, inputs, outputs, stop conditions, permission boundaries, and a meaningful benefit in reducing repeated developer-agent interactions. Do not create a Skill for one-off corrections, ordinary preferences, or overlapping behaviors. Default to project-local Skills; do not modify the shared public repository as a side effect.

Project rules and preferences are owned by each adopter. Do not propose placing their contents into the public repository. Never quote or publish private conversation content, sensitive identifiers, credentials, or internal infrastructure.

## 4. Construct a precise improvement proposal

For each accepted candidate finding, provide:

1. **Observed evidence:** The specific correction, failed step, or check result. Label uncertainty.
2. **Root cause assessment:** Instruction gap, instruction not followed, conflicting rules, missing context, or unknown. Do not assert a root cause unsupported by evidence.
3. **Classification and target:** Response / Process / Outcome; core Skill / project rules / user preferences, with the actual file path if known.
4. **Exact suggested change:** For an update, quote or paraphrase the smallest addition/replacement and location. For a new Skill, propose its name, destination (`.cursor/skills/<name>/SKILL.md` or `.claude/skills/<name>/SKILL.md`), description/trigger, inputs, steps, outputs, approval gates, and an initial SKILL.md draft. Minimize contradictions and duplication.
5. **Interaction cost:** Explain what repeated question, correction, or manual handoff this would eliminate and what user control remains. Do not invent time-savings metrics.
6. **Risks and counterexample:** Describe a different case in which the new rule should **not** apply, to avoid overgeneralization.
7. **Verification plan:** Define a reproducible scenario based on the issue, expected behavior, and a check for conflict with existing rules. Explicitly distinguish:
   - **Static check:** The intended instruction exists and conflicts are absent.
   - **Behavioral check:** A fresh agent run handles the scenario correctly.
   - **Outcome check:** The actual user goal is confirmed in the relevant environment.

Do not claim behavioral or outcome verification from static text inspection.

## 5. Approval and change cycle (handoff only)

1. Output proposals **without applying them**.
2. Require explicit human approval of **which proposals** to apply and their scope.
3. A later, separately authorized execution updates existing Skills or creates approved project-local Skills; it checks name collisions, overlap, tool-specific discovery, and safety boundaries first. Do not interpret a generic wish to improve as blanket approval.
4. After an edit, verify the *current* files, perform relevant static checks and scenario tests when feasible, compare with a counterexample, and report limitations.
5. A later review can assess that execution's actual evidence. Do not automatically invoke another Skill or claim the workflow has permanently learned anything.

## Report format

Follow applicable communication preferences. Lead with findings that **still need action**; if none, state that clearly.

### Proposed changes (approval required)

For each proposal, provide a concise record:

- **Target / category:** File or owning layer and Response, Process, or Outcome.
- **Evidence and cause:** What actually happened; what is established versus inferred.
- **Suggested edit or new Skill:** Smallest specific change, or proposed new Skill with trigger, destination, and initial content.
- **Developer interaction avoided:** What recurrent manual prompting or correction the proposal is designed to reduce.
- **Why this scope:** Why it belongs here, not in the core or personal layer.
- **Validation:** Original failure scenario, expected behavior, and counterexample.

### No changes needed

Identify observed behavior already covered by the current instructions, corrections already integrated, or issues that do not warrant persistence. Omit this section if none.

### Limitations

State unavailable history, files, or validation results that materially affect confidence. Omit if none.

### Next decision

Ask for approval or rejection of individual proposed edits. If there are no proposals, do not request approval.

**Stop here. Do not mutate any file or external state.**
