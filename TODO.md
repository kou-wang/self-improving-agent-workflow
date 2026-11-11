# Roadmap and TODO

This roadmap distinguishes shipped configuration/instructions from features that still require implementation and real-client verification. Items are **not** commitments to autonomous actions.

## Near-term: onboarding and quality

- [ ] Release and live-test GitHub Copilot integration (v0.3.0): VS Code agent mode, skill discovery, update, rollback

- [x] Five canonical, human-in-the-loop Skills
- [x] Review can **propose** editing an existing Skill or creating a new project-local Skill
- [x] Three response language choices: `en` / `zh-CN` / `zh-TW`
- [x] Safe, non-overwriting project installer and separate language switcher
- [x] Add version file, installation manifest, offline safe updater, conflict protection and rollback
- [x] Package `agent-workflow` CLI and implement stable GitHub Releases discovery/download without recurring `git pull`
- [x] Run and verify CLI packaging and mocked GitHub Release tests in CI
- [x] Publish first stable GitHub Release (v0.1.0; license added in v0.2.1 preparation)
- [x] Run installer **and upgrade** unit tests and confirm CI on GitHub
- [ ] Validate update/rollback against both Cursor and Claude Code projects
- [x] Publish semantic-versioned GitHub release tags and changelog (v0.1.0, v0.2.0)
- [ ] Consider opt-in update notifications; CLI already checks the remote latest stable Release when invoked
- [ ] End-to-end smoke test in a fresh Cursor project
- [ ] End-to-end smoke test in a fresh Claude Code project
- [ ] Validate Review proposals on real cases, including updates vs. new Skills
- [ ] Add reproducible Review regression tests and counterexamples
- [ ] Publish v0.2.1 with MIT License after CI passes

## Future capabilities (not implemented)

### 1. Reduce token usage

- [ ] Minimize duplicated Skill instructions and unnecessary context loading.
- [ ] Use compact stage handoffs instead of repeating entire histories where safe.
- [ ] Load only relevant project rules, examples, and reference files when needed.
- [ ] Benchmark token usage and response quality before and after optimization.
- [ ] Ensure shorter context does **not** suppress safety rules, required evidence, or critical approvals.

**Success criterion:** Measured lower token consumption for comparable tasks **without** worse task accuracy, correctness, or safety. No unsupported percentage claims.

### 2. Configurable database interactions

- [ ] Define an optional project-local DB policy (per connection/environment).
- [ ] Distinguish **read** (`SELECT`/metadata inspection) from **write** (including DML, DDL, migrations, procedures, and side-effecting functions); never trust SQL-prefix classification alone.
- [ ] Default to read-only where possible. Require explicit user approval for writes and specific target confirmation.
- [ ] Add least-privilege, transaction, audit, data-redaction, and failure/rollback guidance.
- [ ] Test read-only access, rejected write attempts, and authorized write workflows; do not store credentials in Skills.

**Success criterion:** Read operations are allowed only by project policy; all mutations have explicit authorization and verified targets, and unsafe requests stop.

### 3. GitHub and GitLab interactions

- [ ] Define provider-neutral Git workflow interfaces with GitHub and GitLab adapters/instructions.
- [ ] Support project configuration for repositories, branches, pull requests/merge requests, and allowed commands.
- [ ] Provide read-only workflows first: inspect branches, issues, PRs/MRs, diffs, pipeline results.
- [ ] Gate state-changing actions: commit, push, issue edits, PR/MR creation, merge, releases, CI/CD triggers.
- [ ] Avoid hardcoding account, host, token, or internal company URLs; use existing authenticated tools.
- [ ] Test with sandbox repositories on **both** platforms.

**Success criterion:** Same core workflow works on both providers, with explicit and auditable approval for write actions.

### 4. Reduce end-user runtime and installation dependencies

- [ ] Provide a standalone cross-platform CLI executable for Windows, macOS, and Linux, so end users do not need to preinstall Python, pipx, or Git.
- [ ] Keep the CLI isolated from the target project's Python interpreter, virtual environment, and dependency graph.
- [ ] Design and test a simple first-install and upgrade flow with no repository clone required.
- [ ] Sign releases or publish verifiable checksums and document the provenance/verification process.
- [ ] Test installation, upgrades, conflict protection, and rollback across supported OSes and representative non-Python projects.
- [ ] Document supported architectures, package manager options, and a fallback install method.

**Success criterion:** A new user can install and update the workflow without configuring a Python runtime or changing their existing project's dependencies.

## Guiding principle

**Make the agent adapt to the developer, reducing repeated corrections and handoffs over time.** Review should suggest an existing Skill update first, and a new project-local Skill only when there is a distinct recurring workflow with evidence. Both changes require human approval and verification. More Skills or fewer tokens are not goals if they degrade reliability.
