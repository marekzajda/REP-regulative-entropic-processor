# REPNet Community Edition v1.0

**REPNet — Regulative Entropic Processor Network** is an open-source experimental architecture for studying distributed regulation, graph-based state dynamics, information flow, perturbation, and closure.

This repository is the **public Community Edition** of the REPNet research program. It contains a cleaned, installable, reproducible reference implementation that anyone can inspect, run, modify, and extend.

> Community Edition is intentionally separated from the private research laboratory. Historical memory, private datasets, raw forensic outputs, machine-specific state, unreleased model checkpoints, and experimental orchestration remain outside this public repository.

## Core idea

Each node carries a scalar regulatory potential `C_i`. Positive edge conductances `g_ij` define local relations between nodes. The instantaneous edge flux is

```text
J_ij = g_ij (C_j - C_i)
```

and the public reference observable is the closure / Dirichlet energy

```text
V(C) = 1/2 Σ_(i,j) g_ij (C_j - C_i)^2.
```

Community Edition v1.0 uses a degree-normalized **dissipative** update: without external forcing, potential differences relax rather than amplify. This makes the system a compact testbed for regulatory dynamics and future extensions such as adaptive conductances, nonlinear fluxes, semantic interfaces, memory, learned readouts, and higher-order closure constraints.

See [docs/CONCEPT.md](docs/CONCEPT.md) for the conceptual and mathematical overview.

## Install

```bash
git clone https://github.com/marekzajda/REP-regulative-entropic-processor.git
cd REP-regulative-entropic-processor
python -m pip install -e .
```

For development and tests:

```bash
python -m pip install -e ".[dev]"
pytest
```

## Minimal example

```python
from repnet_community import REPConfig, REPNet, random_knn_graph

graph = random_knn_graph(n=64, k=6, seed=7)
net = REPNet(graph, REPConfig(seed=11))

history = net.run(steps=200)
print("initial energy:", history[0])
print("final energy:", history[-1])
```

Or run the included example directly:

```bash
python examples/basic_dissipation.py
```

## Repository layout

```text
src/repnet_community/
  core.py              reference regulatory dynamics
  graph.py             deterministic weighted graph primitives
examples/
  basic_dissipation.py
 tests/
  test_core.py
 docs/
  CONCEPT.md
  ARCHITECTURE.md
  COMMUNITY_RESEARCH_BOUNDARY.md
```

## What v1.0 includes

- installable NumPy reference implementation;
- deterministic weighted graphs;
- regulatory potentials and edge fluxes;
- closure-energy and total-flow observables;
- explicit external forcing hook;
- regression tests for dissipative relaxation;
- public CI;
- MIT license and citation metadata.

## What v1.0 does not claim

REPNet Community Edition is a research scaffold, not a claim that the minimal graph model is a complete theory of intelligence, consciousness, thermodynamics, or physics. The term *entropic* refers to the broader research program around regulation, dispersion, information flow, and closure. The scalar `V(C)` used here is specifically a Dirichlet / closure energy.

The public v1.0 implementation is also not a byte-for-byte dump of historical experimental branches. It is a cleaned reference surface built from mechanisms that can be stated and tested openly.

## Community and research track

The project follows a promotion model:

```text
private research → validation → clean specification → Community Edition
```

A mechanism is promoted to the public edition only when it has a clear algorithmic specification, controlled tests, no private state, and a reproducible implementation. See [docs/COMMUNITY_RESEARCH_BOUNDARY.md](docs/COMMUNITY_RESEARCH_BOUNDARY.md).

## Contributing

Contributions are welcome: alternative graph constructors, nonlinear regulatory laws, diagnostics, benchmarks, visualization, documentation, and mathematically explicit extensions are natural starting points. Please keep proposed mechanisms independently testable and avoid hidden external state.

## License

MIT License. See [LICENSE](LICENSE).

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff).

## Version

**REPNet Community Edition 1.0.0 — 7 September 2026**
