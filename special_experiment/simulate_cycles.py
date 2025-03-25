# simulate/simulate_cycles.py

import json
import os
import networkx as nx
import random

RESULTS_DIR = "../results/"
os.makedirs(RESULTS_DIR, exist_ok=True)

CYCLE_LENGTH = 3
ACTIVATION_STEPS = 10
DECAY_PROB = 1.0

def build_graph():
    G = nx.DiGraph()

    # Define named cycles
    leopard_cycle = [f"C{i}L" for i in range(1, CYCLE_LENGTH + 1)]
    run_cycle = [f"C{i}R" for i in range(1, CYCLE_LENGTH + 1)]
    merge_cycle = [f"MCL{i}" for i in range(1, 3)]

    def add_cycle_edges(cycle):
        for i in range(len(cycle)):
            G.add_edge(cycle[i], cycle[(i + 1) % len(cycle)], type="excitatory")

    add_cycle_edges(leopard_cycle)
    add_cycle_edges(run_cycle)
    add_cycle_edges(merge_cycle)

    # Cross-cycle links
    G.add_edge("C3L", "MCL1", type="excitatory")
    G.add_edge("MCL1", "MCL2", type="excitatory")
    G.add_edge("MCL2", "C1R", type="excitatory")

    # Inhibitory example
    G.add_edge("C2R", "C1R", type="inhibitory")

    cycles = [leopard_cycle, run_cycle, merge_cycle]
    return G, cycles

def simulate_activation(G, cycles):
    activation_history = []
    active_nodes = set(cycles[0])  # Initial perception (e.g., see leopard)

    for step in range(ACTIVATION_STEPS):
        # Record current activation
        snapshot = {node: (node in active_nodes) for node in G.nodes}
        activation_history.append(snapshot)

        # Compute next active set: only include nodes activated by input
        new_active = set()

        for node in G.nodes:
            # For each incoming connection, check if it was active
            incoming = G.in_edges(node)
            for u, _ in incoming:
                if snapshot[u] and G[u][node]["type"] == "excitatory":
                    new_active.add(node)
                    break  # Only need one excitatory input to fire

        # Optionally apply inhibitory suppression
        inhibited = set()
        for u, v in G.edges():
            if G[u][v]["type"] == "inhibitory" and snapshot[u]:
                inhibited.add(v)

        # Remove inhibited nodes from activation
        active_nodes = new_active - inhibited

    return activation_history

def save_results(G, cycles, activation_history, filename="defined_cycles.json"):
    data = {
        "edges": [(u, v, G[u][v]["type"]) for u, v in G.edges()],
        "cycles": cycles,
        "activation_history": activation_history
    }

    with open(os.path.join(RESULTS_DIR, filename), "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    G, cycles = build_graph()
    history = simulate_activation(G, cycles)
    save_results(G, cycles, history)
