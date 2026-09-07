from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .graph import Graph


@dataclass(frozen=True)
class REPConfig:
    """Configuration for the Community Edition reference dynamics."""

    eta: float = 0.05
    closure_gain: float = 0.20
    viscosity: float = 0.02
    init_sigma: float = 1e-3
    seed: int = 0

    def effective_gain(self) -> float:
        gain = 1.0 - float(self.closure_gain) - float(self.viscosity)
        if not (0.0 < gain <= 1.0):
            raise ValueError("1 - closure_gain - viscosity must lie in (0, 1]")
        if not (0.0 < float(self.eta) <= 1.0):
            raise ValueError("eta must lie in (0, 1]")
        if float(self.init_sigma) < 0.0:
            raise ValueError("init_sigma must be >= 0")
        return gain


class REPNet:
    """Minimal open reference implementation of REPNet.

    Each node carries a scalar regulatory potential C_i. For an undirected
    weighted edge (i, j), the instantaneous flux is

        J_ij = g_ij (C_j - C_i)

    and the closure / Dirichlet energy is

        V(C) = 1/2 sum_ij g_ij (C_j - C_i)^2.

    The Community Edition uses the dissipative sign: in the absence of external
    forcing, a sufficiently small explicit step relaxes potential differences
    rather than amplifying them.
    """

    def __init__(
        self,
        graph: Graph,
        config: REPConfig | None = None,
        potentials: np.ndarray | None = None,
    ) -> None:
        self.graph = graph
        self.config = config or REPConfig()
        self._gain = self.config.effective_gain()
        self.degree = graph.weighted_degree()

        if potentials is None:
            rng = np.random.default_rng(self.config.seed)
            self.C = rng.normal(
                0.0,
                self.config.init_sigma,
                size=self.graph.n,
            ).astype(np.float64)
        else:
            c = np.asarray(potentials, dtype=np.float64).reshape(-1)
            if c.size != self.graph.n:
                raise ValueError("potentials length must equal graph.n")
            if np.any(~np.isfinite(c)):
                raise ValueError("potentials must be finite")
            self.C = c.copy()

        self.step_index = 0

    def currents(self) -> np.ndarray:
        d = self.C[self.graph.edges_v] - self.C[self.graph.edges_u]
        return self.graph.weights * d

    def closure_energy(self) -> float:
        d = self.C[self.graph.edges_v] - self.C[self.graph.edges_u]
        return float(0.5 * np.sum(self.graph.weights * d * d))

    def flow_l1(self) -> float:
        return float(np.sum(np.abs(self.currents())))

    def inject(self, forcing: np.ndarray) -> None:
        f = np.asarray(forcing, dtype=np.float64).reshape(-1)
        if f.size != self.graph.n:
            raise ValueError("forcing length must equal graph.n")
        if np.any(~np.isfinite(f)):
            raise ValueError("forcing must be finite")
        self.C += f

    def step(self, forcing: np.ndarray | None = None) -> float:
        """Advance one regulatory relaxation step and return closure energy."""

        if forcing is not None:
            self.inject(forcing)

        j = self.currents()
        delta = np.zeros_like(self.C)

        # Negative-gradient / dissipative orientation.
        np.add.at(delta, self.graph.edges_u, +j)
        np.add.at(delta, self.graph.edges_v, -j)

        normalized = delta / self.degree
        self.C += float(self.config.eta) * self._gain * normalized
        self.step_index += 1
        return self.closure_energy()

    def run(
        self,
        steps: int,
        forcing_schedule: Callable[[int, "REPNet"], np.ndarray | None] | None = None,
    ) -> np.ndarray:
        """Run multiple steps and return the energy history, including t=0."""

        steps = int(steps)
        if steps < 0:
            raise ValueError("steps must be >= 0")

        history = [self.closure_energy()]
        for k in range(steps):
            forcing = None if forcing_schedule is None else forcing_schedule(k, self)
            history.append(self.step(forcing))
        return np.asarray(history, dtype=np.float64)

    def copy_state(self) -> np.ndarray:
        return self.C.copy()
