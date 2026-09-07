# REPNet Community Edition v1.0 architecture

The public v1.0 architecture is intentionally small and inspectable.

```mermaid
flowchart TD
    A[Optional external forcing] --> B[Node potentials C_i]
    B --> C[Weighted edge differences]
    C --> D[Fluxes J_ij = g_ij C_j - C_i]
    D --> E[Degree-normalized regulatory update]
    E --> B
    B --> F[Closure / Dirichlet energy V(C)]
    D --> G[Total absolute flow]
```

Equivalent high-level loop:

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

The public baseline is therefore deliberately dissipative. New regulatory laws should state explicitly whether they preserve, relax, bound, or amplify the graph energy.

## Observable layer

Community Edition treats observability as part of the architecture rather than an afterthought. The v1.0 public core exposes at least:

- node potentials `C`;
- edge fluxes `J`;
- closure / Dirichlet energy;
- total absolute flow;
- deterministic graph and initialization seeds.

These observables make it possible to compare candidate mechanisms against the same baseline.

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

## Promotion boundary

The public architecture should evolve through a controlled promotion path:

```text
research hypothesis
      ↓
isolated implementation
      ↓
controlled test and baseline comparison
      ↓
replication / failure analysis
      ↓
clean public specification
      ↓
Community Edition
```

Private memory, raw forensic state, unreleased checkpoints, and machine-specific orchestration do not cross this boundary.

## Design principles

1. **Deterministic by default** — fixed seeds should reproduce graph and state initialization.
2. **Inspectable state** — the regulatory potential vector is directly accessible.
3. **Small dependency surface** — v1.0 requires only NumPy.
4. **Observable regulation** — closure energy and total absolute flux are first-class metrics.
5. **No hidden memory** — the public core has no persistent user or conversation state.
6. **No external model requirement** — no LLM, cloud API, or private service is needed for the reference example.
7. **Claims follow tests** — public documentation should distinguish implemented behavior from research hypotheses.
