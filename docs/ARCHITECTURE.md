# REPNet Community Edition v1.0 architecture

The public v1.0 architecture is intentionally small.

```text
external forcing (optional)
        ↓
node potentials C_i
        ↓
edge fluxes J_ij = g_ij(C_j-C_i)
        ↓
degree-normalized regulatory update
        ↓
closure-energy measurement V(C)
        ↺
```

## Package layout

```text
src/repnet_community/
  graph.py   # undirected weighted graph primitives
  core.py    # regulatory dynamics and closure-energy observables

examples/
  basic_dissipation.py

tests/
  test_core.py
```

## Reference dynamics

For every edge `(u,v)`:

```text
J = g(C_v - C_u)
ΔC_u += J
ΔC_v -= J
```

The accumulated update is divided by weighted node degree and scaled by

```text
eta * (1 - closure_gain - viscosity).
```

The sign is chosen so that connected potentials relax toward one another in the unforced reference regime.

## Extension points

Community Edition is meant to be extended. Natural research extensions include:

- adaptive or learned conductances;
- nonlinear flux laws;
- vector-valued node states;
- local closure operators beyond pairwise edges;
- semantic encoders and input projections;
- episodic retrieval or external memory;
- learned readout heads;
- multiscale graph construction;
- explicit uncertainty or admissibility constraints.

These are not silently included in v1.0. A contribution should make each added mechanism explicit and testable.

## Design principles

1. **Deterministic by default** — fixed seeds should reproduce graph and state initialization.
2. **Inspectable state** — the regulatory potential vector is directly accessible.
3. **Small dependency surface** — v1.0 requires only NumPy.
4. **Observable regulation** — closure energy and total absolute flux are first-class metrics.
5. **No hidden memory** — the public core has no persistent user or conversation state.
6. **No external model requirement** — no LLM, cloud API, or private service is needed for the reference example.
