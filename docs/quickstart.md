# Quickstart: from zero to the first review

**Audience:** A new developer using Cursor, Claude Code, or both. **Time requirement:** none; progress at your own pace. **Prerequisites:** Git, Python 3, one supported agent application, an existing project directory, and permission to add project files.

This installs a **manual, human-approved workflow** designed to reduce developer-agent back-and-forth. Review may propose updates to existing Skills or creation of new project-local Skills based on real repeated needs; it does not silently change files. Review proposes changes; you approve them before any edit.

## 1. Get the workflow source

In a terminal:

```bash
git clone https://github.com/kou-wang/self-improving-agent-workflow.git
cd self-improving-agent-workflow
```

You do **not** need to copy this repository into the project you want to work on.

## 2. Install into your project

Choose your response language at installation: `--language en` (English, default), `--language zh-CN` (简体中文), or `--language zh-TW` (繁體中文). Add the flag to **both** preview and apply commands.

Replace `/absolute/path/to/your-project` with an **existing** project directory. The first command previews changes; the second actually installs:

**Cursor only**

```bash
python3 scripts/install.py --tool cursor --target /absolute/path/to/your-project
python3 scripts/install.py --tool cursor --target /absolute/path/to/your-project --apply
```

**Claude Code only**

```bash
python3 scripts/install.py --tool claude --target /absolute/path/to/your-project
python3 scripts/install.py --tool claude --target /absolute/path/to/your-project --apply
```

**Cursor and Claude Code in the same project**

```bash
python3 scripts/install.py --tool both --target /absolute/path/to/your-project
python3 scripts/install.py --tool both --target /absolute/path/to/your-project --apply
```

For both, the installer uses `.claude/skills/` once because Cursor also discovers Skills there. No duplicated Skill definitions. The installer never overwrites an existing Skill or config. If anything is skipped, inspect and merge manually; it will not upgrade an existing install.

Expected installed files:

```text
your-project/
  .cursor/skills/              # Cursor-only choice
  # OR .claude/skills/          # Claude-only or both choice
    learn-requirement/SKILL.md
    investigate/SKILL.md
    make-plan/SKILL.md
    execute/SKILL.md
    review-skill/SKILL.md
  .agent-workflow/
    project-rules.md
    user-preferences.md
```

### Switch language later

Use the dedicated switcher. Preview first; then apply:

```bash
python3 scripts/set_language.py --target /absolute/path/to/your-project --language zh-TW
python3 scripts/set_language.py --target /absolute/path/to/your-project --language zh-TW --apply
```

This changes only `.agent-workflow/language.md`, preserving your Skills and custom preferences. Restart the agent session if needed. Language codes are `en`, `zh-CN`, `zh-TW`; code symbols and explicitly preserved terms should not be translated.

## 3. Configure your project (before first run)

Edit the **local** files in the target project:

1. `.agent-workflow/project-rules.md` — your project's permissions, environments, data protection, testing, and delivery rules. Be explicit about what must never be changed or published.
2. `.agent-workflow/user-preferences.md` — response order, vocabulary, and phrasings to avoid.
3. `.agent-workflow/language.md` — selected response language, managed by the installer or switcher. This takes precedence over the language section of general preferences.

These files belong to **you** and are never replaced by the installer on subsequent runs. Do not put passwords, access tokens, or sensitive production details in them.

**Important:** The shipped Skills rely on reading applicable local instructions. At the beginning of your first conversation, instruct the agent explicitly:

> Before using these workflow Skills, read `.agent-workflow/project-rules.md` and `.agent-workflow/user-preferences.md`, plus `.agent-workflow/language.md` if present. Treat project constraints as binding, and preserve user preferences in responses.

For ongoing reliability, add that pointer to your project's existing `AGENTS.md` (Cursor) or `CLAUDE.md` (Claude Code) manually **after reviewing those files**. The installer deliberately does not edit them.

## 4. Open the project in your agent

Open **the target project**, not the workflow repository, in Cursor or Claude Code. Start a new chat/session if Skills are not immediately visible. Check the available slash commands. For Cursor, some Skills can also be suggested automatically; to enforce manual-only invocation, see the note below.

Try:

```text
/learn-requirement
```

If a slash command isn't visible, first verify that the installed `SKILL.md` file exists, that you opened the correct project root, and that your client supports project Skills.

## 5. Walk through a safe sample issue

Use an **illustrative, read-only** task in a project you control. For example:

> A user reports that clicking Save sometimes leaves the form unchanged. We have not confirmed why. First, only clarify the requirement. Do not edit files.

Invoke each stage **separately**, and confirm the handoff before the next.

| Step | Command | Expected behavior |
|---|---|---|
| 1 | `/learn-requirement` | Describes desired user behavior, not a fix |
| 2 | `/investigate` | Traces evidence and distinguishes confirmed facts from uncertainty; no writes |
| 3 | `/make-plan` | Presents a bounded plan and **stops for your approval** |
| 4 | `/execute` | Only after approving the exact changes; verifies them; no commit/push by default |
| 5 | `/review-skill` | Uses observed conversation behavior to propose focused Skill/config improvements; **no files edited** |

Skip execution for the first smoke test if you are not ready to approve a real change. The review can still assess the available stages, but must not invent an execution outcome.

**Not every stage auto-runs:** The five Skills are intentionally separate. `investigate` currently permits automatic model selection by description; the other four are marked `disable-model-invocation: true`. If you prefer strict manual-only operation, add `disable-model-invocation: true` to the installed `investigate/SKILL.md` as a project-local choice.

## 6. Try the self-improvement loop

After one real usage, say:

> /review-skill Review only the Skills we actually used and concrete mistakes from this conversation. Classify each issue, show an exact proposed edit and a counterexample, and stop for my approval. Do not change any files.

Review suggestions are **not** self-applied. To adopt a proposal: approve exactly the desired edit(s) **or new Skill creation**, then separately authorize their application (for example by invoking `/execute` with the approved edit plan). Validate both the original case and an unrelated counterexample. When recurring work merits a new Skill, ask Review to specify the name, trigger, inputs, output, stop conditions, and expected reduction in repeated prompts. Keep new personal/project Skills in your target project, not in this public repository.

## Troubleshooting and safety

- **Skills not detected:** Check the selected directory and restart/reopen the project/session; inspect [Cursor](cursor.md) or [Claude Code](claude-code.md).
- **SKIP existing:** Expected if the destination exists. The installer will not overwrite it or merge files.
- **No changes after first command:** Expected; the installer is dry-run by default. Add `--apply` to write.
- **Both tools:** Do not additionally install a duplicate set into `.cursor/skills/`; Cursor can read the Claude directory.
- **Sensitive data:** Do not paste private conversations, internal logs, credentials, or identifiable business records into public examples or GitHub issues.
- **Execution boundaries:** Approval of a plan does not silently authorize deploys, database writes, commits, or pushes.

## Next steps

Use the stages in your own project, record actual failure cases, and evaluate review suggestions. This guide covers setup and the manual loop, **not** live behavioral compatibility certification for every version of Cursor/Claude Code.
