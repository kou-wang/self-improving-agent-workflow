# Safe version upgrades

The public repository uses a `VERSION` file. This is currently a **development version**, not an official stable release or Git tag. Version tags and changelog entries should accompany future releases.

## One-time install

Run the [Quickstart](quickstart.md). New installs create `.agent-workflow/install-state.json`, containing the version, target platform, and SHA-256 hashes of official Skills managed by the installer. User-created Skills are **not** listed. Project rules, language and preferences remain user-owned.

## Upgrade existing projects

First update your **source checkout**. This tool is intentionally offline; it does not contact GitHub for newer versions:

```bash
cd self-improving-agent-workflow
git pull --ff-only
```

Preview what will change, and then apply safely:

```bash
python3 scripts/update.py --target /absolute/path/to/project --check
python3 scripts/update.py --target /absolute/path/to/project --apply
```

The updater compares upstream Skill file contents against the installed files and recorded hashes. It will:

- Update official files that match the previously managed hash.
- Add an official Skill only if its directory does not already exist.
- Preserve all user-created Skills, language, preferences, project rules and files outside official Skill directories.
- Keep locally changed official Skills unchanged and report a conflict.
- Create a timestamped backup before replacing any file.
- Output a backup ID that can be used for rollback.

A newer checkout is **not** the same as a tested release; prefer a known tag/commit and read release notes when tags are available.

## Conflicts: Keep Local / Use Upstream / Merge

**Keep Local (default):** do nothing to that conflicting Skill. Other nonconflicting updates can still be installed.

**Use Upstream:** after inspecting the differences and accepting that your customization will be replaced, explicitly name the conflicting Skill:

```bash
python3 scripts/update.py --target /absolute/path/to/project --check --use-upstream investigate
python3 scripts/update.py --target /absolute/path/to/project --apply --use-upstream investigate
```

The old file is saved in a backup. This does **not** affect other local Skills or user configuration.

**Merge:** manually compare upstream and local Skill contents, merge intentionally, and keep your customized copy. A future update will still recognize it as customized and report a conflict rather than overwriting it. There is no automatic three-way merge in this version.

For installs made before the version manifest existed, identical official Skill files can be recognized; files differing from the current source are treated as untracked conflicts. Avoid guessing their baseline.

## Roll back

The update prints a backup ID such as `20261110T123456123456Z`. Preview and restore:

```bash
python3 scripts/update.py --target /absolute/path/to/project --rollback BACKUP_ID
python3 scripts/update.py --target /absolute/path/to/project --rollback BACKUP_ID --confirm-rollback
```

Rollback refuses to overwrite any Skill changed **after** the upgrade. It also checks the installation state and original backup contents. If a check fails, stop and reconcile manually rather than forcing a rollback. Backups remain under `.agent-workflow/backups/`.

## Security and limitations

- Do not commit local backup directories, configuration containing private information, or credentials into a public repository.
- The updater never runs `git pull`, never executes a Skill, and never modifies a deployment or database.
- It updates known official Skills only; no automatic migration of custom Skills, arbitrary project rules, or other project files.
- Each Skill update is backed up; power loss or abnormal termination during a multi-file update can require **manual recovery** from the backup directory. This version is not a fully transactional filesystem updater.
- Current version checking examines a **local checkout**, not the latest remote release.
- Real Cursor and Claude Code end-to-end upgrade behavior still requires smoke testing.

