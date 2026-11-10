# Quickstart: from zero to the first review

**Preferred onboarding:** install the CLI once using `pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git`, then from your project run `agent-workflow install --tool cursor --language zh-CN` and later `agent-workflow update`. Stable Release `v0.2.0` includes the independent Skills, RMA-derived starter preferences, and always-on project rules. The forthcoming `v0.2.1` is a documentation and licensing update. See the [CLI guide](cli.md). The source-checkout procedure below can be used for development.

**Audience:** A new developer using Cursor, Claude Code, or both. **Time requirement:** none; progress at your own pace. **Prerequisites:** Git, Python 3, one supported agent application, an existing project directory, and permission to add project files.

This installs **five independent Skills and useful RMA-derived starter response preferences** (business-first, conclusion-first, concise and structured). They work immediately without a mandated Skill sequence. Review can propose edits to preferences, existing Skills, or new project-local Skills to reduce repeated developer input; it never silently changes files. See [Initialization defaults](initialization.md).

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
  .cursor/rules/agent-workflow.mdc  # Cursor, if selected
  .claude/rules/agent-workflow.md   # Claude, if selected
  .agent-workflow/
    project-rules.md
    user-preferences.md  # prefilled, editable response defaults
    language.md          # chosen response language
    install-state.json   # managed core Skill hashes
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
2. `.agent-workflow/user-preferences.md` — **already contains RMA-derived initial defaults** for concise, business-first answers across task types. Keep, edit, or replace these as your preferences evolve; you do not need to invent a response format before first use.
3. `.agent-workflow/language.md` — selected response language, managed by the installer or switcher. This takes precedence over the language section of general preferences.

These files belong to **you** and are never replaced by the installer on subsequent runs. Do not put passwords, access tokens, or sensitive production details in them.

**Always-on instructions:** The installer creates a small Cursor and/or Claude Code project rule that points to these editable local files, so the response baseline is available **even when no Skill is invoked**. It will not overwrite existing rule files, `AGENTS.md`, or `CLAUDE.md`. Installed Skills also read their relevant local configuration. If an older installation lacks the new rule, re-run an installer version that includes it (existing files are preserved).

## 4. Open the project in your agent

Open **the target project**, not the workflow repository, in Cursor or Claude Code. Start a new chat/session if Skills are not immediately visible. Check the available slash commands. For Cursor, some Skills can also be suggested automatically; to enforce manual-only invocation, see the note below.

Try:

```text
/learn-requirement
```

If a slash command isn't visible, first verify that the installed `SKILL.md` file exists, that you opened the correct project root, and that your client supports project Skills.

## 5. Use any Skill independently

You can paste a PM feature request, error message, or screenshot and type only `/learn-requirement` or `/investigate`. The Agent should explain expected versus actual business behavior, cause and impact, and uncertainty **using your configured response style**, rather than forcing code-centric detail.

A natural, **nonmandatory** workflow is:

`User feedback → /investigate or /learn-requirement → short discussion → /make-plan → /execute`

Use `/make-plan` directly when you already know what you want; it reads the available conversation and project context whether or not an earlier Skill ran. Use `/execute` directly for a sufficiently specific, authorized implementation request, or after approving an existing plan. **No Skill is a prerequisite for another.** Code changes remain uncommitted/unpushed by default; database, production, deployment, and other higher-risk actions still require their specific permissions.

A safe read-only trial: `/investigate A user reports clicking Save sometimes leaves the form unchanged. Explain what is confirmed and what needs evidence; do not modify files.`

You can subsequently discuss findings naturally, invoke planning or execute only when useful, then optionally invoke `/review-skill` to improve the Agent's recurring behavior.

**Not every stage auto-runs:** The five Skills are intentionally separate. `investigate` currently permits automatic model selection by description; the other four are marked `disable-model-invocation: true`. If you prefer strict manual-only operation, add `disable-model-invocation: true` to the installed `investigate/SKILL.md` as a project-local choice.

## 6. Try the self-improvement loop

After a real interaction in which you corrected the Agent's wording, explanation order, or workflow, invoke `/review-skill`. It can learn from **ordinary conversations even when no other Skill was used**. The goal is fewer repeated prompts and better decisions, not simply shorter replies. It should first consider whether the correction belongs in `user-preferences.md`, an existing Skill, or a distinct new project Skill.

Review suggestions are **not** self-applied. To adopt a proposal: approve exactly the desired edit(s) **or new Skill creation**, then separately authorize their application (for example by invoking `/execute` with the approved edit plan). Validate both the original case and an unrelated counterexample. When recurring work merits a new Skill, ask Review to specify the name, trigger, inputs, output, stop conditions, and expected reduction in repeated prompts. Keep new personal/project Skills in your target project, not in this public repository.

## 7. Keep the workflow up to date

For the release-based CLI, simply use `agent-workflow update` after the first stable release has been published. It fetches the release itself, without pulling this repository. `agent-workflow update --check` previews the changes. This is separate from upgrading the CLI application itself; see [CLI guide](cli.md).

### Development-only checkout method

Your custom Skills, project rules and preferences belong to you; the official core can be upgraded separately. After updating this repository checkout (`git pull --ff-only`), run `python3 scripts/update.py --target /absolute/path/to/your-project --check`, then `--apply` after reviewing changes. Conflicts default to **Keep Local**. The updater creates a backup ID for safe rollback. See [Upgrade and rollback](upgrading.md) for full examples and limitations.

## Troubleshooting and safety

- **Skills not detected:** Check the selected directory and restart/reopen the project/session; inspect [Cursor](cursor.md) or [Claude Code](claude-code.md).
- **SKIP existing:** Expected if the destination exists. The installer will not overwrite it or merge files.
- **No changes after first command:** Expected; the installer is dry-run by default. Add `--apply` to write.
- **Both tools:** Do not additionally install a duplicate set into `.cursor/skills/`; Cursor can read the Claude directory.
- **Sensitive data:** Do not paste private conversations, internal logs, credentials, or identifiable business records into public examples or GitHub issues.
- **Execution boundaries:** Approval of a plan does not silently authorize deploys, database writes, commits, or pushes.

## Next steps

Use the stages in your own project, record actual failure cases, and evaluate review suggestions. This guide covers setup and the manual loop, **not** live behavioral compatibility certification for every version of Cursor/Claude Code.
