import networkx as nx
import json
import os
import sys

# Define directories
RESULTS_DIR = "../results/"
os.makedirs(RESULTS_DIR, exist_ok=True)

def create_mini_brain(cycles, additional_edges, initial_active_neurons, neuron_thresholds=None):
    """
    Creates a brain-like graph with multiple cycles and user-defined connections.
    
    :param cycles: List of cycles (each cycle is a list of node names)
    :param additional_edges: List of edges (u, v, type) where type is 'excitatory' or 'inhibitory'
    :param initial_active_neurons: List of neurons to be active in the first iteration
    :param neuron_thresholds: Dictionary mapping neurons to activation thresholds
    :return: The generated graph
    """
    G = nx.DiGraph()

    # Add all cycle nodes
    for cycle in cycles:
        G.add_nodes_from(cycle)

    # Assign default threshold if none is provided
    if neuron_thresholds is None:
        neuron_thresholds = {node: 1 for cycle in cycles for node in cycle}

    # Store thresholds as node attributes
    for node, threshold in neuron_thresholds.items():
        G.nodes[node]["threshold"] = threshold

    # Add cycle edges
    for cycle in cycles:
        for i in range(len(cycle)):
            u, v = cycle[i], cycle[(i + 1) % len(cycle)]
            G.add_edge(u, v, type="excitatory")  # Default cycles are excitatory

    # Add additional edges (overwrites existing ones if necessary)
    for u, v, edge_type in additional_edges:
        G.add_edge(u, v, type=edge_type)

    return G

def activate_mini_brain(G, initial_active_neurons, steps=25):
    """
    Simulates activation in the mini brain model with neuron activation thresholds.
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

            # Get neuron-specific threshold
            activation_threshold = G.nodes[node].get("threshold", 1)  # Default threshold = 1

            # Activation rule: neuron activates if excitatory input ≥ threshold
            if excitatory_inputs >= activation_threshold and inhibitory_inputs == 0:
                new_active[node] = True  

            # Inhibition rule: neuron deactivates if inhibitory inputs exist
            if inhibitory_inputs > 0:
                new_active[node] = False  

        active = new_active
        history.append(active.copy())

    return history

def save_mini_brain(G, cycles, activation_history, filename="mini_brain.json"):
    """
    Save the mini brain experiment results.
    """
    for node in G.nodes():
        print(node, G.nodes[node])
    data = {
        "nodes": {node: {"threshold": G.nodes[node]["threshold"]} for node in G.nodes()},
        "edges": [(u, v, G[u][v]["type"]) for u, v in G.edges()],
        "cycles": cycles,
        "activation_history": activation_history
    }
    
    with open(os.path.join(RESULTS_DIR, filename), "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    # Example: Define cycles, edges, and initial active neurons
    cycles = [
        ["E1"],
        ["A1", "A2", "A3", "A4"],  # 4-node cycle
        ["B1", "B2", "B3", "B4", "B5"],  # 5-node cycle
        ["C1", "C2", "C3", "C4", "C5", "C6"],  # 6-node cycle
        ["D1", "D2", "D3", "D4", "D5", "D6", "D7"],  # 7-node cycle
        ["F1", "F2"],
    ]

    additional_edges = [
        ("A3", "E1", "excitatory"),  # Connect A1 → B3
        ("E1", "C5", "excitatory"),  # Connect B5 → C2
        ("B3", "E1", "excitatory"),  # Connect C4 → A2
        ("D7", "A1", "excitatory"),  # Connect D7 → A1
        ("F1", "F2", "excitatory"),  # Connect F1 → F2
    ]

    initial_active_neurons = ["A1", "B1"]  # Start activation from A1 and B1

    # Define custom activation thresholds for certain neurons
    neuron_thresholds = {
        "E1": 2,
        "F1": 2,
        "F2": 2,
        "A1": 1,
        "A2": 1,
        "A3": 1,
        "A4": 1,
        "B1": 1,
        "B2": 1,
        "B3": 1,
        "B4": 1,
        "B5": 1,
        "C1": 1,
        "C2": 1,
        "C3": 1,
        "C4": 1,
        "C5": 1,
        "C6": 1,
        "D1": 1,
        "D2": 1,
        "D3": 1,
        "D4": 1,
        "D5": 1,
        "D6": 1,
        "D7": 1,
    }

    G = create_mini_brain(cycles, additional_edges, initial_active_neurons, neuron_thresholds)
    activation_history = activate_mini_brain(G, initial_active_neurons)

    save_mini_brain(G, cycles, activation_history)
    print(f"✅ Mini brain experiment completed. Results saved in {RESULTS_DIR}/mini_brain.json.")
