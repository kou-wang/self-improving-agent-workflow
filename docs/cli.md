# CLI: install and update without git pull

The CLI uses **published stable GitHub Releases** as its source of official Skills. It does not need a clone of this repository after CLI installation.

## Install the CLI once

With [pipx](https://pipx.pypa.io/) installed:

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
```

This one-time command uses Git to acquire the CLI source. Future **Skill** updates do not require `git pull`. The CLI itself may need a separate software upgrade in the future (e.g. `pipx upgrade self-improving-agent-workflow`), which is different from updating installed Skills. The package is **not yet published to PyPI**. Do not use `pipx install self-improving-agent-workflow` until a package is published.

## Install the Skills

In the target project directory, or supply `--target /path/to/project`:

```bash
agent-workflow install --tool cursor --language zh-CN
```

For Claude Code use `--tool claude`, for both `--tool both`. Available response languages are `en`, `zh-CN`, `zh-TW`. Run with `--check` to preview before installing.

## Update official Skills with one command

```bash
agent-workflow update
```

The CLI checks GitHub's latest non-prerelease Release, verifies the release archive's version and expected Skill/config files, then calls the safe updater. This preserves your project-local Skills, preferences, and language. Official Skills with local edits are **not overwritten** by default.

Preview first if desired:

```bash
agent-workflow update --check
```

To explicitly replace one conflicting official Skill **after comparing it**:

```bash
agent-workflow update --check --use-upstream investigate
agent-workflow update --use-upstream investigate
```

## Rollback

An applied update displays its backup ID. Preview and then restore:

```bash
agent-workflow rollback BACKUP_ID
agent-workflow rollback BACKUP_ID --apply
```

Rollback refuses to overwrite edits made after the upgrade.

## Release policy and limitations

- **Stable Release `v0.2.0` is published.** The CLI installs/updates from the latest published stable tag, not an unreleased branch. RMA-derived defaults and always-on project rules are included from v0.2.0 onward. v0.2.1 is a documentation/license maintenance release.
- GitHub Releases must be named `vMAJOR.MINOR.PATCH`, and their source archive must contain a matching `VERSION` file.
- Release archives are downloaded over HTTPS and validated against a restricted list of filenames, sizes and sources before the installer reads them. This is **not a signed-release or supply-chain-attestation system**; trust in the repository and GitHub remains necessary.
- Only **Skill source updates** are automatic. A new CLI implementation may require updating the pipx package separately.
- GitHub API rate limits and offline operation may prevent the check; the CLI reports an error rather than silently using an arbitrary branch.
- An existing local install created before version tracking may have unresolved conflicts; default is Keep Local.
- The underlying multi-file updater currently writes files individually and can require manual recovery from a backup after abnormal termination; it is not a fully transactional upgrade.
- Review CI and record any remaining Cursor/Claude Code compatibility or rollback limitations before publishing future releases.

See [upgrading.md](upgrading.md) for conflict and version-state details.
