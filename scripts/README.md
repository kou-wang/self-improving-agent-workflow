# Safe project installer

Use `python3 scripts/install.py --tool cursor|claude|both --target /existing/project` to preview.

Add `--apply` only after reviewing the proposed destinations. The installer requires Python 3 standard library only.

- Cursor installs under `.cursor/skills/`.
- Claude Code installs under `.claude/skills/`.
- Both installs once under `.claude/skills/`, which Cursor also reads.
- Both local configuration templates are installed under `.agent-workflow/`.
- No overwrite or automatic upgrade. Existing destination items are skipped.
- It does not modify `AGENTS.md`, `CLAUDE.md`, existing rules, or existing Skills.
- No source project or company-specific instructions are included.

See [Quickstart](../docs/quickstart.md).
