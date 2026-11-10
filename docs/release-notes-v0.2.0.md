# v0.2.0 — RMA-derived starter experience

**Status:** `v0.2.0` was published on 2026-11-10.

## Highlights

- **Useful first install:** New Cursor and Claude Code projects receive five independent core Skills and editable response preferences drawn from a previously working RMA developer workflow. The defaults are generalized; no private RMA business logic is included.
- **Responses that developers can understand:** Conclusion and user-visible behavior first, with concise structured explanations, actual impact, evidence-backed investigation, and task-appropriate summaries.
- **Preferences also apply in ordinary chat:** New installs include project-scoped always-on Cursor/Claude rule files that point to the user's editable preferences, even without explicitly calling a Skill.
- **No required Skill pipeline:** `/make-plan` can start from a fresh request or reuse previous investigation context; `/execute` can act on a clear, authorized direct instruction or on an approved plan.
- **Review focuses on reducing repeated input:** `/review-skill` considers user feedback on explanation quality and repeated prompts, including conversations that never invoked other Skills.
- **Customization stays protected:** Installer does not overwrite existing preferences/rules; updater keeps locally edited core Skills by default and leaves custom Skills untouched.
- **CLI compatibility:** Release installer supports legacy v0.1.0 archive contents and requires the always-on rule templates in newer tagged releases.

## Getting started

Install the CLI (if not already installed):

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
```

In a new project:

```bash
agent-workflow install --tool cursor --language zh-CN
```

For an existing project:

```bash
agent-workflow update --check
agent-workflow update
```

**Existing projects:** To add missing project-level always-on rule files, re-run `agent-workflow install --tool cursor --language zh-CN` using v0.2.0 or later. This skips existing files. It does **not** replace customized `.agent-workflow/user-preferences.md` with the new default template; merge desired starter preferences manually.

## Validation and known limitations

- Python installer, CLI, and updater tests passed in GitHub Actions on the merged feature PR and `main`. A manual CLI upgrade and fresh installation in a Cursor project also completed.
- Full live Cursor/Claude Code and upgrade/rollback end-to-end testing remains incomplete by choice. These release notes do **not** claim that behavior is verified across client versions.
- Writing/deployment/database permissions are unchanged: `execute` respects the project rules and requires appropriate authorization.
- This release predates the MIT License added during v0.2.1 preparation. For current licensing, refer to the repository's [LICENSE](../LICENSE).

See [initialization](initialization.md), [quickstart](quickstart.md), and [upgrades](upgrading.md) for details.
