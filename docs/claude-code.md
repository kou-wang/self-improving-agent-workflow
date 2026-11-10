# Claude Code: install and invoke

See the complete [Quickstart](quickstart.md) before use.

From a clone of this repository, preview and then apply:

```bash
python3 scripts/install.py --tool claude --target /path/to/project
python3 scripts/install.py --tool claude --target /path/to/project --apply
```

This creates project-local `.claude/skills/<name>/SKILL.md` and project-local configuration templates in `.agent-workflow/`. It never overwrites existing files.

Open **the target project** in Claude Code. Invoke `/learn-requirement`, `/investigate`, `/make-plan`, `/execute`, and `/review-skill` individually. Approve a plan explicitly before executing; Review always stops at proposals. If detection is stale, restart the Claude Code session and confirm the files exist.

For a project used by **both** Claude Code and Cursor, choose `--tool both`. The same `.claude/skills/` files are readable by Cursor, avoiding duplicated Skill definitions.

Official reference: https://code.claude.com/docs/en/skills
