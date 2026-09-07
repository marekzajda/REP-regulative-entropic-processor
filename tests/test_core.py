import numpy as np

from repnet_community import REPConfig, REPNet, chain_graph, random_knn_graph


def assert_nonincreasing(values: np.ndarray, atol: float = 1e-15) -> None:
    diff = np.diff(values)
    assert np.all(diff <= atol), f"energy increased; max delta={float(diff.max())}"


def test_two_node_relaxation_is_dissipative() -> None:
    graph = chain_graph(2)
    net = REPNet(
        graph,
        REPConfig(eta=0.05, closure_gain=0.20, viscosity=0.02, init_sigma=0.0),
        potentials=np.array([-0.5, 0.5]),
    )
    history = net.run(80)
    assert history[-1] < history[0]
    assert_nonincreasing(history)


def test_chain_relaxation_is_dissipative() -> None:
    graph = chain_graph(8)
    state = np.array([1.0, -0.3, 0.7, -1.2, 0.2, 0.9, -0.8, 0.4])
    net = REPNet(graph, REPConfig(eta=0.04, init_sigma=0.0), potentials=state)
    history = net.run(250)
    assert history[-1] < 0.2 * history[0]
    assert_nonincreasing(history)


def test_random_graph_relaxation_is_dissipative() -> None:
    graph = random_knn_graph(n=40, k=5, seed=3)
    rng = np.random.default_rng(19)
    state = rng.normal(size=40)
    net = REPNet(graph, REPConfig(eta=0.03, init_sigma=0.0), potentials=state)
    history = net.run(120)
    assert history[-1] < history[0]
    assert_nonincreasing(history, atol=1e-12)


def test_forcing_is_explicit_and_state_size_is_checked() -> None:
    graph = chain_graph(4)
    net = REPNet(graph, REPConfig(init_sigma=0.0), potentials=np.zeros(4))
    forcing = np.array([1.0, 0.0, 0.0, 0.0])
    before = net.copy_state()
    net.step(forcing=forcing)
    assert not np.allclose(before, net.copy_state())
