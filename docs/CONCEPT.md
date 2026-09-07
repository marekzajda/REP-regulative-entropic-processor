# REPNet concept

**REPNet — Regulative Entropic Processor Network** is an experimental computing architecture built around a simple idea: computation can be organized as the regulation of distributed state under local constraints, rather than only as feed-forward symbol transformation.

REPNet Community Edition v1.0 exposes the smallest reproducible core of that idea.

## State, conductance, flux

Let an undirected graph have node potentials `C_i` and positive edge conductances `g_ij`. For every edge `(i,j)` define the flux

```text
J_ij = g_ij (C_j - C_i)
```

and the closure / Dirichlet energy

```text
V(C) = 1/2 Σ_(i,j) g_ij (C_j - C_i)^2.
```

`V` measures unresolved potential differences across the graph. The Community Edition evolves the state with a degree-normalized dissipative update, so that in the unforced reference regime the network relaxes these differences.

This makes REPNet useful as a laboratory for questions such as:

- how local regulatory constraints produce global relaxation;
- how perturbations propagate through a structured network;
- how different graph topologies change the path to a regulated state;
- how external forcing competes with internal closure dynamics;
- how learned conductances, semantic interfaces, memory, or higher-order constraints could later be added without changing the basic regulatory interpretation.

## Why “regulative”

The core object is not a prediction layer. It is a dynamical state that is continually adjusted according to compatibility relations encoded in the graph. The system therefore has a natural distinction between:

1. **state** — what is currently present in the network;
2. **constraint / conductance** — what relations are permitted or emphasized;
3. **flux** — how disagreement between connected states is transported;
4. **closure** — the reduction of unresolved relational mismatch.

## Why “entropic”

The word *entropic* is used here in the architectural and research-program sense: REPNet studies regulation, dispersion, relaxation, information flow, and closure-like observables. The scalar `V(C)` in Community Edition v1.0 is a Dirichlet / closure energy, not by itself a claim of thermodynamic entropy.

## Scientific scope

Community Edition v1.0 is a **reference implementation and research scaffold**. It does not claim that the minimal graph model is a complete theory of intelligence, consciousness, thermodynamics, or physics. Historical and private REP research explored additional memory, language, readout, and adaptive layers; those are deliberately not bundled into the public reference core until they have a clean, reproducible public specification.

## Historical note

Earlier experimental REPNet branches contained several exploratory mechanisms. The Community Edition intentionally uses the **dissipative sign** consistent with the closure-energy formulation above. It is therefore a cleaned reference implementation, not a byte-for-byte publication of every historical runtime branch.
