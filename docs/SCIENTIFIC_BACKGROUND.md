# Scientific Background

REPNet Community Edition is the public, minimal, reproducible branch of a broader research program on regulation, closure, information flow, and graph-based dynamics.

## Mathematical core implemented in v1.0

For an undirected weighted graph with positive conductances `g_ij` and node potentials `C_i`, the public reference implementation uses the edge flux

```text
J_ij = g_ij (C_j - C_i)
```

and the quadratic graph energy

```text
V(C) = 1/2 Σ_(i,j) g_ij (C_j - C_i)^2.
```

This is a Dirichlet-type energy. In the unforced v1.0 reference dynamics, the numerical update is chosen to be dissipative, so differences in `C` relax rather than grow.

## Why this is useful

This minimal system provides a controlled baseline for asking experimentally precise questions about:

- local versus global regulation;
- perturbation and relaxation;
- topology-dependent flow;
- stability and Lyapunov-like observables;
- adaptive conductances;
- higher-order closure constraints;
- interfaces between regulatory state and learned components.

## Interpretability and traceability

A central design motivation of REPNet is **mechanistic traceability of the regulatory process**.

The public implementation exposes the graph, node potentials, edge fluxes, closure energy, total flow, and forcing inputs directly. A run can therefore be replayed and audited step by step, and causal interventions on nodes, edges, conductances, or forcing terms can be measured explicitly.

This differs from the default interpretability posture of a large language model. LLM internals are not inaccessible: activations, attention patterns, residual streams, probes, attribution methods, sparse autoencoders and causal interventions can reveal meaningful structure. However, those internal representations are highly distributed and do not automatically constitute a compact or faithful explanation of why a particular answer was produced.

REPNet's claim is therefore narrower and testable: **the regulatory computation is natively observable and traceable by construction**. It is not a claim that every regulatory variable carries a direct human-level semantic interpretation.

See [REPNet and standard LLM architectures](REPNET_VS_LLM.md) for the full comparison.

## Relation to the wider research program

The broader REP / REPNet research line explores richer mechanisms than those exposed in Community Edition v1.0. Some historical branches also coupled regulatory dynamics to semantic embeddings, memory retrieval, learned readouts, and language-model interfaces.

Those mechanisms are not automatically treated as validated. The public repository follows a promotion rule: a mechanism is added only after it can be stated cleanly, tested reproducibly, and separated from private state or machine-specific artifacts.

## Claim boundary

Community Edition v1.0 does **not** establish that REPNet is:

- a complete theory of intelligence;
- a model of consciousness;
- a complete thermodynamic theory;
- a theory of quantum gravity or spacetime;
- evidence that regulatory graph dynamics alone produce semantic understanding.

It should be read as an open experimental framework whose mathematical and computational claims are limited to what can be tested in the code and examples contained here.

## Research philosophy

The project treats negative results as useful. A mechanism that fails a controlled test should be documented, revised, or rejected rather than protected by interpretation. Public promotion should therefore follow:

```text
hypothesis → implementation → controlled test → replication → public specification
```
