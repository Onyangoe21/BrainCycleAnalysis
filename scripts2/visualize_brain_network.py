import os
import networkx as nx
import matplotlib.pyplot as plt
import json

RESULTS_DIR = "../results/"
FIGURES_DIR = "../figures/"
os.makedirs(FIGURES_DIR, exist_ok=True)

GRAPH_FILE = os.path.join(RESULTS_DIR, "processed_directed_graph.graphml")

def plot_cycle_distribution():
    """Plot histogram of cycle lengths."""
    with open(os.path.join(RESULTS_DIR, "cycle_stats.json")) as f:
        data = json.load(f)

    plt.hist(data["cycle_lengths"], bins=20, color="blue", alpha=0.7)
    plt.xlabel("Cycle Length")
    plt.ylabel("Count")
    plt.title("Distribution of Cycles in the Directed Brain Graph")
    plt.savefig(os.path.join(FIGURES_DIR, "cycle_distribution.png"))
    plt.show()

def plot_brain_network():
    """Visualize the brain network with cycle hubs highlighted."""
    G = nx.read_graphml(GRAPH_FILE)

    with open(os.path.join(RESULTS_DIR, "hub_nodes.json")) as f:
        hub_data = json.load(f)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, node_color="gray", edge_color="lightgray", node_size=50, alpha=0.3)

    # Highlight hub nodes in red
    nx.draw_networkx_nodes(G, pos, nodelist=hub_data["overlapping_hubs"], node_color="red", node_size=100)

    plt.title("Brain Network with Key Cycle Hubs Highlighted")
    plt.savefig(os.path.join(FIGURES_DIR, "brain_network.png"))
    plt.show()

if __name__ == "__main__":
    plot_cycle_distribution()
    plot_brain_network()
