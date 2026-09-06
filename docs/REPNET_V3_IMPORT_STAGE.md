# RepNet V3.0 migration stage — source-only preparation

This stage prepares a public-source copy of the historical local `RepNet_V3_0` tree while preserving the original directory and its persistent learned state.

## Safety boundary

The historical source directory is treated as an immutable research artifact during migration. The import script performs copy-only operations from the source tree and never initializes or runs RepNet.

The following are excluded from the prepared public-source copy by policy:

- Python virtual environments and caches (`.venv`, `venv`, `env`, `__pycache__`, etc.)
- persistent memory/state directories (`memory`, `state`, `persistent_state`, and aliases)
- SQLite/databases, pickle/shelve files, PyTorch checkpoints, NumPy state blobs
- secret/local config (`.env*`, `config.json`) and private keys/certificates
- logs, temporary data, build artifacts and binary payloads

The prepared copy is written to `archive/RepNet_V3_0_source` and accompanied by copied/skipped manifests plus a JSON summary in `migration_audit/`.

## Required review before commit

Do not run `git add`, `git commit`, or `git push` immediately after preparation. First review the prepared copy and audit manifests. Confirm that no private conversations, credentials, memory databases, model state, or unrelated personal files are present.

Only after review should the source-only import be committed to the migration branch.

## Historical state

Persistent RepNet state remains local and must be handled as a separate research artifact. Its integrity should be preserved with SHA-256 hashes and an immutable snapshot before any replay or compatibility experiment.
