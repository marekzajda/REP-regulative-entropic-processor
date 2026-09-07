# REPNet Community Edition v1.0

[![REPNet Community CI](https://github.com/marekzajda/REP-regulative-entropic-processor/actions/workflows/community-ci.yml/badge.svg)](https://github.com/marekzajda/REP-regulative-entropic-processor/actions/workflows/community-ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**REPNet — Regulative Entropic Processor Network** is an open-source experimental architecture for studying distributed regulation, graph-based state dynamics, information flow, perturbation, relaxation, and closure.

This repository is the **public Community Edition** of the REPNet research program. It contains a cleaned, installable, reproducible reference implementation that anyone can inspect, run, modify, test, and extend.

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

Community Edition v1.0 uses a degree-normalized **dissipative** update: without external forcing, potential differences relax rather than amplify. This gives the project a compact, testable baseline for regulatory dynamics and future extensions.

```mermaid
flowchart TD
    A[Optional external forcing] --> B[Node potentials C_i]
    B --> C[Edge fluxes J_ij]
    C --> D[Degree-normalized regulatory update]
    D --> B
    B --> E[Closure / Dirichlet energy V(C)]
    C --> F[Total flow diagnostics]
```

## Why REPNet is different from a standard LLM

REPNet is not primarily a next-token predictor. Its public core is an **explicit regulatory dynamical system** whose internal state evolution can be inspected directly.

A major design advantage is **native mechanistic traceability**: during a run, a researcher can follow node potentials, edge fluxes, closure energy, total flow, graph topology, conductances, and the effect of perturbations step by step. This makes causal intervention and replay of the regulatory process straightforward.

By contrast, modern LLMs have very strong semantic and generative capabilities, but their internal computation is distributed across high-dimensional activations. Those internals can be studied with attention analysis, probes, attribution, sparse autoencoders and other mechanistic-interpretability tools, but they do not naturally provide a compact, faithful decision trace.

This distinction is important: REPNet aims to make the **regulatory computation traceable by construction**. It does **not** claim that every internal state automatically corresponds to a human-readable semantic reason.

See [REPNet and standard LLM architectures](docs/REPNET_VS_LLM.md) for a detailed comparison of advantages, limitations, and the hybrid research direction.

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

See [Getting Started](docs/GETTING_STARTED.md) for the full quick-start path.

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
  core.py                     reference regulatory dynamics
  graph.py                    deterministic weighted graph primitives
examples/
  basic_dissipation.py
tests/
  test_core.py
docs/
  GETTING_STARTED.md          installation and first run
  CONCEPT.md                  conceptual and mathematical overview
  ARCHITECTURE.md             implementation architecture
  REPNET_VS_LLM.md            comparison with standard LLM architectures
  SCIENTIFIC_BACKGROUND.md    scientific scope and claim boundary
  COMMUNITY_RESEARCH_BOUNDARY.md
  FAQ.md
```

## What v1.0 includes

- installable NumPy reference implementation;
- deterministic weighted graphs;
- regulatory potentials and edge fluxes;
- closure-energy and total-flow observables;
- explicit external forcing hook;
- regression tests for dissipative relaxation;
- public CI on supported Python versions;
- MIT license and citation metadata;
- contribution, security, roadmap, issue and pull-request guidance.

## What v1.0 does not claim

REPNet Community Edition is a research scaffold, not a claim that the minimal graph model is a complete theory of intelligence, consciousness, thermodynamics, or physics. The term *entropic* refers to the broader research program around regulation, dispersion, information flow, and closure. The scalar `V(C)` implemented here is specifically a Dirichlet / closure energy.

The public v1.0 implementation is also not a byte-for-byte dump of historical experimental branches. It is a cleaned reference surface built from mechanisms that can be stated and tested openly.

See [Scientific Background](docs/SCIENTIFIC_BACKGROUND.md) for the explicit research and claim boundary.

## Community and research track

The project follows a promotion model:

```text
private research → validation → clean specification → Community Edition
```

A mechanism is promoted to the public edition only when it has a clear algorithmic specification, controlled tests, no private state, and a reproducible implementation. See [Community / Research Boundary](docs/COMMUNITY_RESEARCH_BOUNDARY.md).

## Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [Concept](docs/CONCEPT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [REPNet vs standard LLM architectures](docs/REPNET_VS_LLM.md)
- [Scientific Background](docs/SCIENTIFIC_BACKGROUND.md)
- [FAQ](docs/FAQ.md)
- [Community / Research Boundary](docs/COMMUNITY_RESEARCH_BOUNDARY.md)
- [Roadmap](ROADMAP.md)

## Contributing

Contributions are welcome: graph constructors, nonlinear regulatory laws, diagnostics, benchmarks, visualization, documentation, mathematically explicit extensions, and negative-result replications are all useful.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Please keep proposed mechanisms independently testable and avoid hidden external state.

## Community standards and security

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- GitHub issue templates are provided for bugs and research/feature proposals.

## Roadmap

Community Edition development is intentionally conservative: private research mechanisms are promoted only after validation. See [ROADMAP.md](ROADMAP.md) for the public v1.x direction.

## License

MIT License. See [LICENSE](LICENSE).

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff).

## Version

**REPNet Community Edition 1.0.0 — 7 September 2026**
