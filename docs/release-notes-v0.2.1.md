# v0.2.1 — Public release readiness

This maintenance release makes the existing five-Skill workflow easier and clearer for outside developers to adopt. No Skill behavior changes are included.

## Changes

- Add the MIT License, allowing use, modification and redistribution under its terms.
- Refresh README, quickstart, CLI, initialization and previous release notes to accurately describe the released v0.2.0 capabilities.
- Clearly label the project **early access**. Automated Python tests and successful manual CLI upgrade/fresh Cursor installation do not establish full compatibility with all Cursor or Claude Code versions.
- Explain that `agent-workflow update` upgrades installed Skills but CLI code updates require a separate `pipx upgrade self-improving-agent-workflow`.

## Install

```bash
pipx install git+https://github.com/kou-wang/self-improving-agent-workflow.git
agent-workflow install --tool cursor --language zh-CN
```

Install in an existing project directory; choose `--tool claude` or `--tool both` as needed.

## Upgrade

```bash
pipx upgrade self-improving-agent-workflow
agent-workflow update --check
agent-workflow update
```

## Known limitations

- Real-client end-to-end behavior across both agent products and full rollback cases has not yet been comprehensively verified.
- Project installation preserves existing local customizations; upgrading does not automatically replace local preferences.
- The updater is not fully transactional; an unexpected interruption may require manual recovery from backups.
- Release downloads are restricted and checked for expected files, but they are not cryptographically signed or attested.

Please report reproducible issues through GitHub Issues without including private project data or credentials.
