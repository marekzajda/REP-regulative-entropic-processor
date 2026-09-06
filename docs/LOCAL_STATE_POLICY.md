# REP / RepNet Local State Preservation Policy

RepNet on Marek's workstation may already contain persistent historical memory/state from earlier interactive sessions. That state is considered **local canonical evidence** and must not be overwritten, reset, migrated, or published automatically by the GitHub connector.

## Connector rule

The GitHub connector operates on source code, approved test jobs, and generated test summaries. It must treat any RepNet memory/state store as an external local dependency.

The connector therefore follows these rules:

1. **No destructive writes** to historical RepNet memory/state during inventory or baseline testing.
2. **No automatic upload** of conversation memory, personal interaction history, local databases, checkpoints, or opaque persistent state to the public repository.
3. **No schema migration** of a memory database until its format and backup strategy are understood.
4. Before any experiment that could modify memory/state, create a timestamped local backup and record a cryptographic manifest where practical.
5. Prefer read-only inspection for the first reconstruction pass.
6. Tests that require a writable memory layer should use a disposable copy/sandbox, never the canonical historical state.

## Recommended local layout

```text
REP historical source/                # original source tree
REP local canonical state/            # historical RepNet memory; private and protected
REP-regulative-entropic-processor/    # Git working clone + connector
REP test sandboxes/                   # disposable experiment copies
```

The actual existing directory structure should be inventoried before anything is moved or renamed.

## Scientific provenance

Historical RepNet state may contain useful evidence about the evolution of REP/RepNet concepts and human–agent interaction. Preservation does not imply that its contents are scientifically valid by themselves; it means they should remain available for later controlled analysis with provenance intact.
