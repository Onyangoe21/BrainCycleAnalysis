import networkx as nx
import os

DATA_DIR = "../directed_graphml/"

def check_graph_directedness():
    """Check if all graphs in the dataset are properly directed."""
    for file in os.listdir(DATA_DIR):
        if file.endswith(".graphml"):
            path = os.path.join(DATA_DIR, file)
            try:
                G = nx.read_graphml(path)

                # Check if the graph is actually directed
                if not G.is_directed():
                    print(f"❌ ERROR: {file} contains undirected edges!")
                else:
                    print(f"✅ {file} is properly directed.")

            except Exception as e:
                print(f"❌ ERROR reading {file}: {e}")

if __name__ == "__main__":
    check_graph_directedness()
