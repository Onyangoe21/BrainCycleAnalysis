import networkx as nx
import json
import os
import sys

# Define directories
RESULTS_DIR = "../results/"
os.makedirs(RESULTS_DIR, exist_ok=True)

def create_mini_brain(cycles, additional_edges, initial_active_neurons):
    """
    Creates a brain-like graph with multiple cycles and user-defined connections.
    
    :param cycles: List of cycles (each cycle is a list of node names)
    :param additional_edges: List of edges (u, v, type) where type is 'excitatory' or 'inhibitory'
    :param initial_active_neurons: List of neurons to be active in the first iteration
    :return: The generated graph
    """
    G = nx.DiGraph()

    # Add all cycle nodes
    for cycle in cycles:
        G.add_nodes_from(cycle)

    # Add cycle edges
    for cycle in cycles:
        for i in range(len(cycle)):
            u, v = cycle[i], cycle[(i + 1) % len(cycle)]
            G.add_edge(u, v, type="excitatory")  # Default cycles are excitatory

    # Add additional edges (overwrites existing ones if necessary)
    for u, v, edge_type in additional_edges:
        G.add_edge(u, v, type=edge_type)

    return G

def activate_mini_brain(G, initial_active_neurons, steps=10, inhibition_threshold=2):
    """
    Simulates activation in the mini brain model.
    """
    active = {node: False for node in G.nodes()}

    # Set initial active neurons
    for node in initial_active_neurons:
        if node in active:
            active[node] = True

    history = []

    for _ in range(steps):
        new_active = {node: False for node in G.nodes()}

        for node in G.nodes():
            excitatory_inputs = sum(1 for pr in G.predecessors(node) if active[pr] and G[pr][node]["type"] == "excitatory")
            inhibitory_inputs = sum(1 for pr in G.predecessors(node) if active[pr] and G[pr][node]["type"] == "inhibitory")

            if excitatory_inputs > 0 and inhibitory_inputs < inhibition_threshold:
                new_active[node] = True  

            if inhibitory_inputs >= inhibition_threshold:
                new_active[node] = False  

        active = new_active
        history.append(active.copy())

    return history

def save_mini_brain(G, cycles, activation_history, filename="mini_brain.json"):
    """
    Save the mini brain experiment results.
    """
    data = {
        "nodes": list(G.nodes()),
        "edges": [(u, v, G[u][v]["type"]) for u, v in G.edges()],
        "cycles": cycles,
        "activation_history": activation_history
    }
    
    with open(os.path.join(RESULTS_DIR, filename), "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    # Example: Define cycles, edges, and initial active neurons
    cycles = [
        ["A1", "A2", "A3", "A4"],  # 4-node cycle
        ["B1", "B2", "B3", "B4", "B5"],  # 5-node cycle
        ["C1", "C2", "C3", "C4", "C5", "C6"],  # 6-node cycle
        ["D1", "D2", "D3", "D4", "D5", "D6", "D7"],  # 7-node cycle
    ]

    # additional_edges = [
    #     ("A1", "B3", "excitatory"),  # Connect A1 → B3
    #     ("B5", "C2", "inhibitory"),  # Connect B5 → C2
    #     ("C4", "A2", "excitatory"),  # Connect C4 → A2
    #     ("D7", "A1", "excitatory"),  # Connect D7 → A1
    # ]
    additional_edges = []

    initial_active_neurons = ["A1", "B1"]  # Start activation from A1 and B1

    G = create_mini_brain(cycles, additional_edges, initial_active_neurons)
    activation_history = activate_mini_brain(G, initial_active_neurons)

    save_mini_brain(G, cycles, activation_history)
    print(f"✅ Mini brain experiment completed. Results saved in {RESULTS_DIR}/mini_brain.json.")
