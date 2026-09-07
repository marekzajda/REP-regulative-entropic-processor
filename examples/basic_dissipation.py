from repnet_community import REPConfig, REPNet, random_knn_graph


def main() -> None:
    graph = random_knn_graph(n=64, k=6, seed=7)
    net = REPNet(graph, REPConfig(eta=0.05, closure_gain=0.20, viscosity=0.02, seed=11))

    history = net.run(steps=200)
    initial = float(history[0])
    final = float(history[-1])

    print(f"nodes={graph.n} edges={graph.m}")
    print(f"initial_closure_energy={initial:.12e}")
    print(f"final_closure_energy={final:.12e}")
    print(f"energy_ratio={final / initial:.6f}")


if __name__ == "__main__":
    main()
