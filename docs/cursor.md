# Cursor: install and invoke

See the complete [Quickstart](quickstart.md) before using this in a production project.

From a clone of this repository, first preview:

```bash
python3 scripts/install.py --tool cursor --target /path/to/project
python3 scripts/install.py --tool cursor --target /path/to/project --apply
```

This creates project-local `.cursor/skills/<name>/SKILL.md` for all five Skills and the optional local configuration templates under `.agent-workflow/`. Existing files are never overwritten.

Open **the target project** in Cursor. Invoke `/learn-requirement`, `/investigate`, `/make-plan`, `/execute`, or `/review-skill` as needed. `investigate` currently allows model selection by description; the other four require explicit invocation. Each Skill reads the two local configuration files if present.

For a project shared with Claude Code, choose `--tool both` **instead** of `cursor`: it installs a single canonical copy under `.claude/skills/`, which Cursor also discovers. Avoid installing duplicate names in both directories.

Official reference: https://cursor.com/help/customization/skills
