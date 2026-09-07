# Contributing to REPNet Community Edition

Thank you for helping improve REPNet Community Edition.

## Scope

The public repository is a clean, reproducible reference implementation. Contributions should be understandable without access to private datasets, historical memory, machine-specific state, or unpublished research artifacts.

Good contribution areas include:

- graph constructors and topology utilities;
- alternative dissipative or nonlinear regulatory laws;
- diagnostics and observables;
- benchmarks and reproducible experiments;
- visualization;
- tests and numerical validation;
- documentation and examples.

## Development setup

```bash
git clone https://github.com/marekzajda/REP-regulative-entropic-processor.git
cd REP-regulative-entropic-processor
python -m pip install -e ".[dev]"
pytest
```

## Contribution requirements

1. Keep mechanisms explicit and independently testable.
2. Add tests for behavior that changes the numerical core.
3. Do not add private state, credentials, raw research memory, local database files, model checkpoints, or machine-specific paths.
4. State clearly whether a contribution is a tested implementation, a prototype, or a research proposal.
5. Prefer deterministic examples with fixed seeds where practical.
6. Keep public claims proportional to the evidence in the repository.

## Pull requests

A pull request should explain:

- what changes;
- why it is useful;
- how it was tested;
- whether it changes the mathematical or numerical behavior;
- any limitations or open questions.

Small, focused pull requests are preferred.

## Research-to-community promotion

Mechanisms developed in the private research track are promoted here only after they have a clear specification, reproducible implementation, tests, and no dependency on private state. See `docs/COMMUNITY_RESEARCH_BOUNDARY.md`.
