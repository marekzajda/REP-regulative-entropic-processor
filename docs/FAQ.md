# REPNet Community Edition FAQ

## What is REPNet?

REPNet is an experimental regulatory network architecture for studying graph-based state dynamics, local flux, perturbation, relaxation, and closure-like observables.

## What does “entropic” mean here?

In Community Edition v1.0, the implemented scalar observable is a Dirichlet / closure energy over graph potential differences. The broader term “entropic” belongs to the wider research program and should not be read as a claim that the current minimal implementation is a full thermodynamic model.

## Is REPNet an AI model?

The public v1.0 core is not a language model and does not claim intelligence or consciousness. It is a regulatory graph dynamics scaffold that can later be coupled to other interfaces or learned components.

## Is this the original historical REPNet source?

No. Community Edition is a cleaned public reference implementation. Historical experimental branches contain legacy behavior, private state, and research artifacts that are intentionally kept outside this repository.

## Why is the v1.0 update dissipative?

For the reference core, the unforced system is designed so that potential differences relax rather than amplify. This gives a simple, testable stability baseline.

## Can I use my own graph?

Yes. The core is designed around a weighted undirected graph abstraction. Additional graph constructors are welcome.

## Does the project use private datasets or cloud services?

Not for the public reference core. Community Edition should remain reproducible without private memory, private datasets, or hidden external state.

## How are new mechanisms added?

The project uses a promotion model:

```text
private research → validation → clean specification → Community Edition
```

A mechanism should be independently testable and documented before promotion.

## How do I contribute?

See `CONTRIBUTING.md` and open a focused issue or pull request.
