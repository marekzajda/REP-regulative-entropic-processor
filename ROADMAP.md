# REPNet Community Edition Roadmap

This roadmap describes the public, reproducible branch of REPNet. It does not expose private research state or unpublished internal experiments.

## v1.0 — Reference regulatory core

Status: released on `main`.

- installable NumPy implementation;
- deterministic weighted graphs;
- scalar regulatory potentials;
- edge flux and closure / Dirichlet energy;
- dissipative degree-normalized dynamics;
- external forcing hook;
- tests, examples, CI, license and citation metadata.

## v1.1 — Diagnostics and visualization

Planned:

- richer energy and flow diagnostics;
- graph-state summaries;
- reproducible benchmark fixtures;
- plotting examples;
- clearer numerical stability documentation.

## v1.2 — Adaptive regulation

Candidate public mechanisms, subject to validation:

- adaptive positive conductances;
- bounded/nonlinear flux laws;
- local closure penalties;
- perturbation-response benchmarks.

## v1.3 — Interfaces and readouts

Only mechanisms that survive controlled research validation will be promoted.

Candidates include:

- semantic input interfaces;
- learned readouts;
- memory adapters with explicit provenance;
- modular controller interfaces.

## Longer-term research questions

- Which local update rules guarantee global Lyapunov descent?
- Which adaptive conductance laws preserve stability?
- Which observables are genuinely causal rather than merely correlated?
- How much functionality can be obtained from regulation alone before adding learned components?
- Which higher-order closure constraints remain tractable and falsifiable?

The roadmap is intentionally conservative: public versions should contain mechanisms that can be specified, tested, and reproduced without access to private research artifacts.
