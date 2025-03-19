import networkx as nx
import random
import matplotlib.pyplot as plt
import os
import json
import sys

# Set paths
RESULTS_DIR = "../results/"
FIGURES_DIR = "../figures/"
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

def create_defined_cycles(inhibition_prob=0.0):
    """
    Construct a graph with three predefined cycles (4-node, 5-node, and 6-node cycles),
    assigning inhibitory and excitatory edges as expected by existing functions.
    """
    G = nx.DiGraph()

    # Define nodes for each cycle
    cycle_A = [f"A{i}" for i in range(1, 5)]
    cycle_B = [f"B{i}" for i in range(1, 6)]
    cycle_C = [f"C{i}" for i in range(1, 7)]

    # Add nodes
    G.add_nodes_from(cycle_A + cycle_B + cycle_C)

    def add_cycle_edges(cycle):
        for i in range(len(cycle)):
            edge_type = "excitatory" if random.random() > inhibition_prob else "inhibitory"
            G.add_edge(cycle[i], cycle[(i + 1) % len(cycle)], type=edge_type)

    # Add edges
    add_cycle_edges(cycle_A)
    add_cycle_edges(cycle_B)
    add_cycle_edges(cycle_C)

    return G, [cycle_A, cycle_B, cycle_C]

def create_overlapping_cycles(inhibition_prob=0.0):
    """
    Create cycles that overlap via a central neuron, which activates cycles when it fires.
    """
    G, cycles = create_defined_cycles(inhibition_prob)

    # Add a central activation neuron
    central_node = "Central"
    G.add_node(central_node)

    # Connect central node to cycle entry points
    G.add_edge(central_node, "A1", type="excitatory")
    G.add_edge(central_node, "B1", type="excitatory")
    G.add_edge(central_node, "C1", type="excitatory")

    return G, cycles + [[central_node]]

def generate_toy_brain(n_nodes=20, n_cycles=5, inhibition_prob=0.3):
    """
    Create a random graph with cycles.
    """
    G = nx.DiGraph()
    G.add_nodes_from(range(n_nodes))

    for _ in range(n_nodes * 2):  
        u, v = random.sample(range(n_nodes), 2)
        G.add_edge(u, v, type="excitatory" if random.random() > inhibition_prob else "inhibitory")

    cycles = []
    for _ in range(n_cycles):
        cycle_length = random.randint(3, 6)
        cycle_nodes = random.sample(range(n_nodes), cycle_length)
        for i in range(cycle_length):
            edge_type = "excitatory" if random.random() > inhibition_prob else "inhibitory"
            G.add_edge(cycle_nodes[i], cycle_nodes[(i + 1) % cycle_length], type=edge_type)
        cycles.append(cycle_nodes)

    return G, cycles

def activate_cycles(G, steps=10, activation_rate=0.1, inhibition_threshold=2):
    """
    Simulate activation considering excitatory and inhibitory edges,
    where each neuron is only active for one step.
    """
    active = {node: False for node in G.nodes()}
    initial_active = [node for node in G.nodes() if random.random() < activation_rate]

    for node in initial_active:
        active[node] = True

    history = []

    for _ in range(steps):
        new_active = {node: False for node in G.nodes()}

        for node in G.nodes():
            excitatory_inputs = sum(1 for pr in G.predecessors(node) if active[pr] and G[pr][node]["type"] == "excitatory")
            inhibitory_inputs = sum(1 for pr in G.predecessors(node) if active[pr] and G[pr][node]["type"] == "inhibitory")

            if node == "Central" and excitatory_inputs >= 2:
                new_active[node] = True  

            if excitatory_inputs > 0 and inhibitory_inputs < inhibition_threshold:
                new_active[node] = True  

            if inhibitory_inputs >= inhibition_threshold:
                new_active[node] = False  

        active = new_active
        history.append(active.copy())

    return history

def save_results(G, cycles, activation_history, filename):
    """
    Save graph properties, cycle data, and activation history.
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
    experiment = sys.argv[1] if len(sys.argv) > 1 else "defined_cycles"

    if experiment == "defined_cycles":
        G, cycles = create_defined_cycles()
        filename = "defined_cycles.json"
    elif experiment == "overlapping_cycles":
        G, cycles = create_overlapping_cycles()
        filename = "overlapping_cycles.json"
    elif experiment == "random_graph":
        G, cycles = generate_toy_brain()
        filename = "random_graph.json"
    else:
        print(f"Invalid experiment: {experiment}")
        sys.exit(1)

    activation_history = activate_cycles(G, steps=10, activation_rate=0.1, inhibition_threshold=2)
    save_results(G, cycles, activation_history, filename)

    print(f"Experiment '{experiment}' completed. Results saved in {RESULTS_DIR}/{filename}.")
