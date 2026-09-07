from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class Graph:
    """Undirected weighted graph stored as a de-duplicated half-edge list."""

    n: int
    edges_u: np.ndarray
    edges_v: np.ndarray
    weights: np.ndarray

    def __post_init__(self) -> None:
        self.n = int(self.n)
        self.edges_u = np.asarray(self.edges_u, dtype=np.int64)
        self.edges_v = np.asarray(self.edges_v, dtype=np.int64)
        self.weights = np.asarray(self.weights, dtype=np.float64)

        if self.n <= 0:
            raise ValueError("n must be > 0")
        if not (self.edges_u.shape == self.edges_v.shape == self.weights.shape):
            raise ValueError("edge arrays must have identical shapes")
        if self.edges_u.ndim != 1:
            raise ValueError("edge arrays must be one-dimensional")
        if self.edges_u.size == 0:
            raise ValueError("graph must contain at least one edge")
        if np.any(self.edges_u < 0) or np.any(self.edges_v < 0):
            raise ValueError("negative node index")
        if np.any(self.edges_u >= self.n) or np.any(self.edges_v >= self.n):
            raise ValueError("edge index out of range")
        if np.any(self.edges_u >= self.edges_v):
            raise ValueError("edges must be stored with u < v")
        if np.any(~np.isfinite(self.weights)) or np.any(self.weights <= 0.0):
            raise ValueError("weights must be finite and strictly positive")

        pairs = np.stack([self.edges_u, self.edges_v], axis=1)
        if np.unique(pairs, axis=0).shape[0] != pairs.shape[0]:
            raise ValueError("duplicate edges are not allowed")

    @property
    def m(self) -> int:
        return int(self.edges_u.size)

    @classmethod
    def from_edges(
        cls,
        n: int,
        edges: Iterable[tuple[int, int]],
        weights: Iterable[float] | None = None,
    ) -> "Graph":
        normalized: list[tuple[int, int]] = []
        for u, v in edges:
            u, v = int(u), int(v)
            if u == v:
                continue
            if u > v:
                u, v = v, u
            normalized.append((u, v))

        normalized = sorted(set(normalized))
        if not normalized:
            raise ValueError("graph must contain at least one non-self edge")

        if weights is None:
            w = np.ones(len(normalized), dtype=np.float64)
        else:
            w = np.asarray(list(weights), dtype=np.float64)
            if w.size != len(normalized):
                raise ValueError("weights length must match normalized edge count")

        return cls(
            n=int(n),
            edges_u=np.asarray([u for u, _ in normalized], dtype=np.int64),
            edges_v=np.asarray([v for _, v in normalized], dtype=np.int64),
            weights=w,
        )

    def weighted_degree(self) -> np.ndarray:
        degree = np.zeros(self.n, dtype=np.float64)
        np.add.at(degree, self.edges_u, self.weights)
        np.add.at(degree, self.edges_v, self.weights)
        return np.maximum(degree, 1.0)


def chain_graph(n: int, weight: float = 1.0) -> Graph:
    if n < 2:
        raise ValueError("chain_graph requires n >= 2")
    return Graph.from_edges(
        n=n,
        edges=[(i, i + 1) for i in range(n - 1)],
        weights=[float(weight)] * (n - 1),
    )


def random_knn_graph(n: int, k: int = 6, seed: int = 0) -> Graph:
    """Build a deterministic 3-D k-nearest-neighbour graph.

    The geometry is only a convenient graph generator; REPNet itself does not
    require an embedding space.
    """

    n = int(n)
    k = int(k)
    if n < 2:
        raise ValueError("n must be >= 2")
    if k < 1:
        raise ValueError("k must be >= 1")
    k = min(k, n - 1)

    rng = np.random.default_rng(seed)
    points = rng.random((n, 3))
    diff = points[:, None, :] - points[None, :, :]
    distance = np.sqrt(np.sum(diff * diff, axis=-1))
    np.fill_diagonal(distance, np.inf)

    edge_set: set[tuple[int, int]] = set()
    for i in range(n):
        for j in np.argsort(distance[i])[:k]:
            j = int(j)
            u, v = (i, j) if i < j else (j, i)
            edge_set.add((u, v))

    return Graph.from_edges(n=n, edges=sorted(edge_set))
