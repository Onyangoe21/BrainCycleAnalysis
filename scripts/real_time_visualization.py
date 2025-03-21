import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
import numpy as np
# Define directories
RESULTS_DIR = "../results/"
FIGURES_DIR = "../figures/"
os.makedirs(FIGURES_DIR, exist_ok=True)

def load_results(filename="toy_results.json"):
    """Load experiment results from a JSON file."""
    with open(os.path.join(RESULTS_DIR, filename), "r") as f:
        return json.load(f)
    
def get_custom_layout(G, cycles, min_distance=1.5):
    """
    Generate a custom layout where cycles are placed in separate circular regions.
    Ensures no two nodes are placed too close together.
    
    :param G: Graph object
    :param cycles: List of cycles
    :param min_distance: Minimum distance between any two nodes
    :return: Position dictionary for nodes
    """
    pos = {}
    center_x, center_y = 0, 0
    spacing = 6  # Distance between cycle centers

    def is_far_enough(new_x, new_y):
        """Check if a new position is sufficiently far from all existing positions."""
        for x, y in pos.values():
            if np.sqrt((new_x - x) ** 2 + (new_y - y) ** 2) < min_distance:
                return False
        return True

    for i, cycle in enumerate(cycles):
        angle_step = 2 * np.pi / len(cycle)
        cycle_center = (center_x + i * spacing, center_y)
        
        for j, node in enumerate(cycle):
            x = cycle_center[0] + 2 * np.cos(j * angle_step)
            y = cycle_center[1] + 2 * np.sin(j * angle_step)

            # Adjust position if too close to an existing node
            while not is_far_enough(x, y):
                x += 0.2  # Push outward
                y += 0.2  # Adjust diagonally

            pos[node] = (x, y)

    # Place additional nodes separately
    remaining_nodes = set(G.nodes()) - set(pos.keys())
    for i, node in enumerate(remaining_nodes):
        x, y = center_x + (i + 1) * spacing, center_y - spacing

        # Adjust position to avoid overlap
        while not is_far_enough(x, y):
            x += 0.2
            y += 0.2

        pos[node] = (x, y)

    return pos

def get_fixed_positions(G, cycles):
    """
    Generate fixed positions for better cycle visualization.
    
    :param G: NetworkX graph
    :param cycles: List of cycles in the graph
    :return: Dictionary of fixed positions for nodes
    """
    pos = {}

    # Define base coordinates for arranging cycles
    base_x = 0
    base_y = 0
    spacing = 10  # Space between cycle groups

    for i, cycle in enumerate(cycles):
        # Compute circular layout for each cycle
        cycle_pos = nx.circular_layout(cycle, scale=5)  # Adjust scale for spacing

        # Shift the cycle so they don't overlap
        shift_x = base_x + (i % 3) * spacing
        shift_y = base_y + (i // 3) * spacing
        for node, (x, y) in cycle_pos.items():
            pos[node] = (x + shift_x, y + shift_y)

    return pos

def animate_activation(G, activation_history, cycles, save_as="activation_animation.mp4"):
    """
    Animate activation patterns with fixed positions for better visibility.

    :param G: NetworkX graph
    :param activation_history: List of activation states per time step
    :param cycles: List of cycles to define fixed positions
    :param save_as: Name of the output animation file
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Get fixed positions for better cycle visualization
    # pos = get_fixed_positions(G, cycles)
    pos = get_custom_layout(G, cycles)

    def update(frame):
        ax.clear()
        active_nodes = [node for node, active in activation_history[frame].items() if active]

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
    experiment = sys.argv[1] if len(sys.argv) > 1 else "defined_cycles"
    results = load_results(f"../results/{experiment}.json")

    G = nx.DiGraph()
    for u, v, edge_type in results["edges"]:
        G.add_edge(u, v, type=edge_type)

    activation_history = results["activation_history"]
    cycles = results["cycles"]  # Load cycles from JSON

    animate_activation(G, activation_history, cycles)
