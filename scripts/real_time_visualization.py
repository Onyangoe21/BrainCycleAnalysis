import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys

# Define directories
RESULTS_DIR = "../results/"
FIGURES_DIR = "../figures/"
os.makedirs(FIGURES_DIR, exist_ok=True)

def load_results(filename="toy_results.json"):
    """Load experiment results from a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

def animate_activation(G, activation_history, save_as="activation_animation.mp4"):
    """
    Animate activation patterns with inhibitory/excitatory edges.

    :param G: NetworkX graph
    :param activation_history: List of activation states per time step
    :param save_as: Name of the output animation file
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)

    def update(frame):
        ax.clear()
        active_nodes = [node for node, active in activation_history[frame].items() if active]  # ✅ Correct

        # Separate edges by type
        excitatory_edges = [(u, v) for u, v in G.edges() if G[u][v]["type"] == "excitatory"]
        inhibitory_edges = [(u, v) for u, v in G.edges() if G[u][v]["type"] == "inhibitory"]

        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=excitatory_edges, edge_color="red", alpha=0.7)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=inhibitory_edges, edge_color="blue", alpha=0.7, style="dashed")

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color="gray", node_size=300)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=active_nodes, node_color="red", node_size=300)

        # Draw labels
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="black")

        ax.set_title(f"Activation Step {frame + 1}")

    ani = animation.FuncAnimation(fig, update, frames=len(activation_history), interval=1500, repeat=True)

    ani.save(os.path.join(FIGURES_DIR, save_as), writer="ffmpeg", fps=1)
    plt.show()

if __name__ == "__main__":
    # Load results
    experiment = sys.argv[1] if len(sys.argv) > 1 else "defined_cycles"
    results = load_results(f"/Users/edwinomondi/Dartmouth/lisp/BrainCycleAnalysis/results/{experiment}.json")

    # Reconstruct the graph
    G = nx.DiGraph()
    for u, v, edge_type in results["edges"]:
        G.add_edge(u, v, type=edge_type)

    # Extract activation history
    activation_history = results["activation_history"]

    # Animate activation and inhibition
    animate_activation(G, activation_history)
