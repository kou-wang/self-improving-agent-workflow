# Agent Workflow — GitHub Copilot project defaults

Use the following project-owned configuration when present:
- `.agent-workflow/user-preferences.md`: developer response style, terminology, and recurring corrections
- `.agent-workflow/language.md`: chosen response language; preserve exact technical identifiers
- `.agent-workflow/project-rules.md`: project constraints, permissions, environments, and data boundaries

Default communication: give the conclusion first; explain user-visible behavior and business consequences before implementation details; be concise, structured, and evidence-based. Local user preferences override these starter defaults. Do not invent business rules, permissions, or facts.

The five Agent Workflow Skills are independent. You may apply a relevant Skill without a preceding stage; use the current request and available project context. The `review-skill` workflow proposes reusable improvements but never applies them without explicit separate authorization.

Do not infer authorization for destructive, database, deployment, production, repository or other external changes from this file. Observe applicable project rules and specific user approvals.
