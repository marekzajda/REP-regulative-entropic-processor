# REP — Regulative Entropic Processor

This repository is the working and archival home for **REP / RepNet (Regulative Entropic Processor)** and its reproducible test connector.

The repository is intentionally split into two roles:

- preservation of the historical REP / RepNet code lineage;
- controlled, reproducible execution of approved tests on a local workstation.

## Connector v1

`connector/rep_connector.py` is a deliberately restrictive local runner. It reads JSON jobs from `jobs/inbox/`, validates them against an allowlist in `connector/config.json`, executes only explicitly approved Python entry points, and writes machine-readable results to `results/`.

The connector does **not** execute arbitrary shell commands from GitHub jobs.

Typical flow:

```text
GitHub repository
      ↓ git pull --ff-only
jobs/inbox/*.json
      ↓
REP Connector v1
      ↓
allowlisted local Python test
      ↓
results/<run_id>/
      ↓ git commit + push
GitHub repository
```

## Local workstation

The historical source directory should remain untouched during the first inventory/reconstruction stage. Work from a cloned or copied repository rather than modifying the historical source tree in place.

No credentials, tokens, private datasets, virtual environments, caches, large generated outputs, or local machine secrets should be committed.

See `docs/CONNECTOR_V1.md` for setup and safety details.
