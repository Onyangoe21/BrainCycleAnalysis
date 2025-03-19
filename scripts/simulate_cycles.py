# This is what this script does in a nutshell
# 1. Generate a random directed graph simulating a toy brain network.
# 2. Introduce random cycles to mimic feedback loops in the brain.
# 3. Implement a simple activation model to observe which cycles persist over time.
# 4. Save the results in the results/ directory.

import networkx as nx
import random
import matplotlib.pyplot as plt
import os
import json

# Set paths
RESULTS_DIR = "../results/"
FIGURES_DIR = "../figures/"
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

def create_defined_cycles(inhibition_prob=0.3):
    """
    Construct a graph with three predefined cycles (4-node, 5-node, and 6-node cycles),
    assigning inhibitory and excitatory edges as expected by existing functions.
    
    :param inhibition_prob: Probability that an edge is inhibitory
    :return: A directed graph G with three distinct cycles
    """
    G = nx.DiGraph()

    # Define nodes for each cycle
    cycle_A = [f"A{i}" for i in range(1, 5)]  # A1 → A2 → A3 → A4 → A1
    cycle_B = [f"B{i}" for i in range(1, 6)]  # B1 → B2 → B3 → B4 → B5 → B1
    cycle_C = [f"C{i}" for i in range(1, 7)]  # C1 → C2 → C3 → C4 → C5 → C6 → C1

    # Add nodes
    G.add_nodes_from(cycle_A + cycle_B + cycle_C)

    # Function to add edges with inhibitory/excitatory labels
    def add_cycle_edges(cycle):
        for i in range(len(cycle)):
            edge_type = "excitatory" if random.random() > inhibition_prob else "inhibitory"
            G.add_edge(cycle[i], cycle[(i + 1) % len(cycle)], type=edge_type)

    # Add edges to the cycles
    add_cycle_edges(cycle_A)
    add_cycle_edges(cycle_B)
    add_cycle_edges(cycle_C)

    return G, [cycle_A, cycle_B, cycle_C]



def generate_toy_brain(n_nodes=20, n_cycles=5, inhibition_prob=0.3):
    """
    Create a directed graph with cycles and inhibitory/excitatory edges.

    :param n_nodes: Number of nodes
    :param n_cycles: Number of cycles to introduce
    :param inhibition_prob: Probability that an edge is inhibitory
    :return: Directed graph G with labeled edges
    """
    G = nx.DiGraph()
    G.add_nodes_from(range(n_nodes))

    # Randomly add directed edges
    for _ in range(n_nodes * 2):  
        u, v = random.sample(range(n_nodes), 2)
        G.add_edge(u, v, type="excitatory" if random.random() > inhibition_prob else "inhibitory")

    # Inject cycles with mixed edge types
    cycles = []
    for _ in range(n_cycles):
        cycle_length = random.randint(3, 6)
        cycle_nodes = random.sample(range(n_nodes), cycle_length)
        for i in range(cycle_length):
            edge_type = "excitatory" if random.random() > inhibition_prob else "inhibitory"
            G.add_edge(cycle_nodes[i], cycle_nodes[(i + 1) % cycle_length], type=edge_type)
        cycles.append(cycle_nodes)

    return G, cycles

def detect_cycles(G):
    """
    Detect all cycles in the directed graph using Johnson’s algorithm.
    :param G: NetworkX directed graph
    :return: List of cycles
    """
    return list(nx.simple_cycles(G))

def visualize_graph(G, filename="toy_brain.png"):
    """
    Visualize the graph and save it.
    :param G: NetworkX directed graph
    :param filename: Name of the output file
    """
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=500, font_size=10)
    plt.title("Toy Brain Graph with Random Cycles")
    plt.savefig(os.path.join(FIGURES_DIR, filename))
    plt.close()

def activate_cycles(G, steps=10, activation_rate=0.1, inhibition_threshold=2):
    """
    Simulate cycle activation considering excitatory and inhibitory edges,
    where each neuron is only active for one step.

    :param G: NetworkX directed graph
    :param steps: Number of time steps
    :param activation_rate: Fraction of initially active neurons
    :param inhibition_threshold: Number of inhibitory inputs required to deactivate a neuron
    :return: List of activation states per time step
    """
    active = {node: False for node in G.nodes()}
    initial_active = [node for node in G.nodes() if random.random() < activation_rate]

    for node in initial_active:
        active[node] = True  # Initially active neurons fire once

    history = []

    for _ in range(steps):
        new_active = {node: False for node in G.nodes()}  # All neurons default to inactive

        for node in G.nodes():
            excitatory_inputs = sum(1 for pr in G.predecessors(node) if active[pr] and G[pr][node]["type"] == "excitatory")
            inhibitory_inputs = sum(1 for pr in G.predecessors(node) if active[pr] and G[pr][node]["type"] == "inhibitory")

            # Activation rule: neuron activates if it gets enough excitatory input
            if excitatory_inputs > 0 and inhibitory_inputs < inhibition_threshold:
                new_active[node] = True  # Activates but only for this step

            # Inhibition rule: neuron deactivates if too many inhibitory inputs
            if inhibitory_inputs >= inhibition_threshold:
                new_active[node] = False  # Stays off

        active = new_active  # Update for the next step
        history.append(active.copy())

    return history




def save_results(G, cycles, activation_history, filename="toy_results.json"):
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
    # Generate toy brain network
    # G, injected_cycles = generate_toy_brain(n_nodes=20, n_cycles=5, inhibition_prob=0.3)
    G, injected_cycles = create_defined_cycles()
    # Detect cycles
    detected_cycles = detect_cycles(G)

    # Simulate activation
    activation_history = activate_cycles(G, steps=10, activation_rate=0.1, inhibition_threshold=2)

    # Save results
    save_results(G, injected_cycles, activation_history)

    # Visualize graph
    visualize_graph(G)
    
    print(f"Graph generated with {len(G.nodes())} nodes and {len(G.edges())} edges.")
    print(f"Injected {len(injected_cycles)} cycles.")
    print(f"Results saved in {RESULTS_DIR}")
