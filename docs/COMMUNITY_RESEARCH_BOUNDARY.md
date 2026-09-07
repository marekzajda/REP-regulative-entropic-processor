# Community / research boundary

REPNet is developed in two deliberately separated tracks.

## Public: REPNet Community Edition

The public repository contains material that is suitable for independent inspection, reuse, modification, and reproduction:

- the conceptual and mathematical core;
- the cleaned reference implementation;
- deterministic examples and tests;
- public documentation;
- public CI;
- future mechanisms only after they have a stable public specification.

## Private: research laboratory

The private research repository remains the place for fast-moving experiments and preserved historical material, including items that should not be bundled with a public downloadable distribution:

- historical conversation memory and persistent state;
- raw forensic outputs and local research artifacts;
- private datasets and machine-specific configuration;
- experimental model checkpoints and research-only readouts;
- unreleased reconstruction branches;
- local orchestration and monitoring infrastructure;
- intermediate tests whose interpretation is not yet stable.

## Promotion rule

A mechanism should move from the private research track into Community Edition only when it can be published with:

1. a clear mathematical or algorithmic specification;
2. a minimal dependency set;
3. deterministic or statistically controlled tests;
4. no private memory, credentials, or machine-specific state;
5. an honest statement of what the mechanism demonstrates and what it does not.

Community Edition is therefore not a dump of the internal laboratory. It is the reproducible public surface of the REPNet research program.
