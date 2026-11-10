# Agent Workflow — project defaults

Read the installed project configuration when available:
- `.agent-workflow/user-preferences.md`: response ordering, structure, terminology, developer corrections.
- `.agent-workflow/language.md`: output language (keep exact code and business identifiers).
- `.agent-workflow/project-rules.md`: data/operation permissions and project constraints.

Default responses: **conclusion first; explain business behavior, cause, and impact before code; concise, structured, self-contained; task-specific format, without unnecessary headings**. Prefer customized local preferences over these initial defaults. Never assume project-specific rules or permissions.

Each Skill stands alone. Use conversation and project context without making the developer repeat known facts; `make-plan` and `execute` do not require preceding Skill invocations. Respect approval gates for destructive, production, deployment, and data-changing operations.
