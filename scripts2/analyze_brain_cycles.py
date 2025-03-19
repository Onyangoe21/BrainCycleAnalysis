import os
import networkx as nx
import json
import signal
from collections import Counter

# Directories
RESULTS_DIR = "../results/"
GRAPH_FILE = "/Users/edwinomondi/Dartmouth/lisp/BrainCycleAnalysis/processed_graphml/100307_connectome_scale500_directed.graphml"

# Timeout Exception Class
class TimeoutException(Exception):
    pass

# Timeout Signal Handler
def timeout_handler(signum, frame):
    raise TimeoutException()

def detect_cycles(G, time_limit=60, max_length=6):
    """
    Detect cycles up to `max_length` with a time limit.
    Uses a path-based method for efficiency.
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(time_limit)  # Set timeout

    try:
        print("⏳ Detecting cycles (this may take some time)...")
        cycles = [cycle for cycle in nx.simple_cycles(G) if len(cycle) <= max_length]
        signal.alarm(0)  # Cancel timeout if successful
    except TimeoutException:
        print("⚠ Timeout: Cycle detection took too long!")
        return []

    print(f"✅ Found {len(cycles)} cycles (≤ {max_length} nodes).")
    
    # Save cycle statistics
    with open(os.path.join(RESULTS_DIR, "cycle_stats.json"), "w") as f:
        json.dump({"total_cycles": len(cycles), "cycle_lengths": [len(c) for c in cycles]}, f, indent=4)

    return cycles

def find_overlapping_hubs(cycles):
    """Find nodes that participate in multiple cycles."""
    node_counts = Counter(node for cycle in cycles for node in cycle)
    overlapping_nodes = [node for node, count in node_counts.items() if count > 3]

    print(f"🔄 Nodes in multiple cycles: {overlapping_nodes}")

    with open(os.path.join(RESULTS_DIR, "hub_nodes.json"), "w") as f:
        json.dump({"overlapping_hubs": overlapping_nodes}, f, indent=4)

    return overlapping_nodes

if __name__ == "__main__":
    print("🔄 Loading brain graph...")
    G = nx.read_graphml(GRAPH_FILE)

    # Convert MultiDiGraph to simple DiGraph if necessary
    if isinstance(G, nx.MultiDiGraph):
        print("⚠ MultiDiGraph detected. Converting to DiGraph (merging edges).")
        G = nx.DiGraph(G)

    # Reduce graph by removing weak edges
    threshold = 0.0  # Adjust based on dataset
    for u, v, data in G.edges(data=True):
        print(f"Edge {u} → {v}, Weight: {data.get('weight', 0)}")
    G = nx.DiGraph((u, v, d) for u, v, d in G.edges(data=True) if d.get("weight", 0) > threshold)
    print(f"✅ Reduced graph to {len(G.nodes())} nodes and {len(G.edges())} edges.")

    # Detect cycles efficiently
    cycles = detect_cycles(G)

    # Find overlapping nodes in cycles
    find_overlapping_hubs(cycles)

    print("✅ Cycle detection completed.")
