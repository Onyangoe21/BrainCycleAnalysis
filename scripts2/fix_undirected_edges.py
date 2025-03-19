import os
import xml.etree.ElementTree as ET
import shutil
import subprocess

# Define directories
RAW_DATA_DIR = "../directed_graphml/"    # Original dataset
PROCESSED_DATA_DIR = "../processed_graphml/"  # New processed dataset
CLONED_REPO_DIR = "../processed_repo/"   # New cloned repo

# Ensure output directories exist
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(CLONED_REPO_DIR, exist_ok=True)

def fix_graphml(file_path, output_path):
    """Convert undirected edges into bidirectional edges in a GraphML file."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespace = "{http://graphml.graphdrawing.org/xmlns}"
    graph = root.find(f"{namespace}graph")

    new_edges = []

    for edge in graph.findall(f"{namespace}edge"):
        if edge.get("directed") == "false":
            source = edge.get("source")
            target = edge.get("target")

            # Remove the directed attribute
            edge.attrib.pop("directed", None)

            # Create a reverse edge
            reverse_edge = ET.Element(f"{namespace}edge", source=target, target=source)

            # Copy all child data elements from the original edge
            for child in edge:
                reverse_edge.append(child)

            new_edges.append(reverse_edge)

    # Append new bidirectional edges to the graph
    for new_edge in new_edges:
        graph.append(new_edge)

    # Save the modified graphml file
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"✅ Fixed {file_path} → Saved to {output_path}")

def process_all_graphml():
    """Process all GraphML files and save fixed versions."""
    for file in os.listdir(RAW_DATA_DIR):
        if file.endswith(".graphml"):
            input_path = os.path.join(RAW_DATA_DIR, file)
            output_path = os.path.join(PROCESSED_DATA_DIR, file)
            fix_graphml(input_path, output_path)

def create_cloned_repo():
    """Clone the processed dataset into a new Git repository."""
    print("🚀 Creating cloned repository for processed files...")

    # Copy processed files into new repo directory
    shutil.copytree(PROCESSED_DATA_DIR, os.path.join(CLONED_REPO_DIR, "processed_graphml"), dirs_exist_ok=True)

    # Initialize Git repo
    subprocess.run(["git", "init"], cwd=CLONED_REPO_DIR)
    subprocess.run(["git", "add", "."], cwd=CLONED_REPO_DIR)
    subprocess.run(["git", "commit", "-m", "Initial commit of processed brain graphs"], cwd=CLONED_REPO_DIR)

    print(f"✅ Cloned repo created at: {CLONED_REPO_DIR}")

if __name__ == "__main__":
    print("🔄 Fixing undirected edges in GraphML files...")
    process_all_graphml()

    print("📂 Cloning processed files into a new repository...")
    create_cloned_repo()

    print("✅ All tasks completed successfully!")
