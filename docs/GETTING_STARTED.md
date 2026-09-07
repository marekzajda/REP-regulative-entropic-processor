# Getting Started

REPNet Community Edition v1.0 is designed to run with a small dependency surface and no private services.

## Requirements

- Python 3.10 or newer
- NumPy

For development, `pytest` is included through the optional `dev` extra.

## Clone and install

```bash
git clone https://github.com/marekzajda/REP-regulative-entropic-processor.git
cd REP-regulative-entropic-processor
python -m pip install -e .
```

Development install:

```bash
python -m pip install -e ".[dev]"
pytest
```

## Run the reference example

```bash
python examples/basic_dissipation.py
```

The example builds a deterministic weighted graph, initializes regulatory potentials, evolves the network, and reports the closure / Dirichlet energy over time.

## Minimal Python use

```python
from repnet_community import REPConfig, REPNet, random_knn_graph

graph = random_knn_graph(n=64, k=6, seed=7)
net = REPNet(graph, REPConfig(seed=11))

energy = net.run(steps=200)
print(energy[0], energy[-1])
```

For an unforced dissipative configuration, the final energy should be lower than the initial energy.

## Next steps

- Read `CONCEPT.md` for the mathematical idea.
- Read `ARCHITECTURE.md` for the implementation flow.
- Read `SCIENTIFIC_BACKGROUND.md` for the claim boundary.
- Read `ROADMAP.md` before proposing a larger extension.
- Read `CONTRIBUTING.md` before opening a pull request.
