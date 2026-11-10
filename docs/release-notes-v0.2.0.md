# v0.2.0 — RMA-derived starter experience

**Status:** release notes prepared; `v0.2.0` is **not yet tagged or published**.

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

In a new project after v0.2.0 is published:

```bash
agent-workflow install --tool cursor --language zh-CN
```

For an existing project:

```bash
agent-workflow update --check
agent-workflow update
```

**Existing projects:** To add missing project-level always-on rule files, re-run `agent-workflow install --tool cursor --language zh-CN` after the v0.2.0 Release is published. This skips existing files. It does **not** replace customized `.agent-workflow/user-preferences.md` with the new default template; merge desired starter preferences manually.

## Validation and known limitations

- Python installer, CLI, and updater checks passed in GitHub Actions on the merged feature PR and `main`; confirm the same on this release candidate.
- Full live Cursor/Claude Code and upgrade/rollback end-to-end testing remains incomplete by choice. These release notes do **not** claim that behavior is verified across client versions.
- Writing/deployment/database permissions are unchanged: `execute` respects the project rules and requires appropriate authorization.
- The project has not yet selected an open-source license; availability on GitHub is not an open-source license grant.

See [initialization](initialization.md), [quickstart](quickstart.md), and [upgrades](upgrading.md) for details.
