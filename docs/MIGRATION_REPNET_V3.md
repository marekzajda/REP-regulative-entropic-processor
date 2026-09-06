# RepNet V3.0 migration plan

Source folder (historical live state):

`C:\Users\Marek Zajda\Desktop\UEST teorie\REP - regulative entropic processor python\RepNet_V3_0`

## Safety principle

The original RepNet V3.0 directory is treated as a historical live-state source. Do not execute, modify, migrate in-place, or overwrite its persistent state before a read-only inventory and cryptographic snapshot are completed.

Known persistent-state files from historical runs include:
- `memory/repnet_state.npz`
- `memory/memory.sqlite`
- `memory/readout_head.pt`

Known runtime architecture:
- `brain_server:app` via uvicorn on `127.0.0.1:8000`
- `adapter_chat.py`
- Ollama backend on `127.0.0.1:11434`
- historical model: `phi3:mini`
- sentence embedding model: `sentence-transformers/all-MiniLM-L6-v2`

## Migration stages

1. Read-only inventory of the source tree.
2. SHA-256 manifest of all files.
3. Separate classification of source code, configuration, persistent memory, logs, outputs and local environments.
4. Snapshot the original persistent state outside the working copy.
5. Import code and documentation into this Git branch.
6. Import persistent memory only if explicitly approved, preferably as an encrypted/offline archival artifact rather than public Git content.
7. Reconstruct a clean runnable environment in a separate working copy.
8. Reproduce the original RepNet V3.0 stack before making architectural changes.
9. Add controlled A/B experiments for RepNet state, Ollama model and memory components.

## GitHub policy

- `main` remains stable.
- Migration work happens on `migration/repnet-v3`.
- No secrets, local credentials, tokens, private logs or raw persistent memory are to be committed automatically.
- Large binary model/state files stay outside Git unless explicitly versioned using an appropriate artifact mechanism.
