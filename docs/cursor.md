# Cursor: install and invoke

See the complete [Quickstart](quickstart.md) before using this in a production project.

From a clone of this repository, first preview:

```bash
python3 scripts/install.py --tool cursor --target /path/to/project
python3 scripts/install.py --tool cursor --target /path/to/project --apply
```

This creates five independent project-local `.cursor/skills/<name>/SKILL.md` files, the editable RMA-derived response defaults under `.agent-workflow/`, and an always-on `.cursor/rules/agent-workflow.mdc` rule. The rule makes the default style available even when no Skill is called. Existing files are never overwritten.

Open **the target project** in Cursor. Invoke `/learn-requirement`, `/investigate`, `/make-plan`, `/execute`, or `/review-skill` as needed. `investigate` currently allows model selection by description; the other four require explicit invocation. Each Skill reads local project rules, editable response preferences, and the selected language if present. `make-plan` and `execute` can be invoked directly without previous Skill calls.

For a project shared with Claude Code, choose `--tool both` **instead** of `cursor`: it installs a single canonical copy under `.claude/skills/`, which Cursor also discovers. Avoid installing duplicate names in both directories.

Official reference: https://cursor.com/help/customization/skills
