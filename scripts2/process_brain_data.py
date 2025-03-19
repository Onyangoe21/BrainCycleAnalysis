import os
import networkx as nx
import json

DATA_DIR = "../processed_graphml"
RESULTS_DIR = "../results/"
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_brain_graph(file_path):
    """Load and standardize a brain connectome graph."""
    G = nx.read_graphml(file_path)

    # Ensure nodes have proper labels
    G = nx.relabel_nodes(G, {node: f"Region_{node}" for node in G.nodes()})

    if isinstance(G, nx.MultiDiGraph):  # ✅ Check if the graph is a MultiDiGraph
        for u, v, k, data in G.edges(keys=True, data=True):  # ✅ Handle multi-edges
            if "weight" not in data:  
                G.edges[u, v, k].update({"weight": 1})  
                print(f"⚠ Added default weight to multi-edge: {u} → {v} (key={k})")  
    else:
        for u, v, data in G.edges(data=True):  
            if "weight" not in data:  
                G.edges[u, v].update({"weight": 1})  
                print(f"⚠ Added default weight to edge: {u} → {v}")  

    return G

def process_all_graphs():
    """Load all directed brain graphs, clean them, and save results."""
    graphs = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".graphml"):
            path = os.path.join(DATA_DIR, file)
            G = load_brain_graph(path)
            graphs.append(G)
            print(f"Processed {file}: {len(G.nodes())} nodes, {len(G.edges())} edges.")

            # Save cleaned graph
            nx.write_graphml(G, os.path.join(RESULTS_DIR, f"processed_{file}"))

    print("✅ All graphs processed and saved.")

if __name__ == "__main__":
    process_all_graphs()
