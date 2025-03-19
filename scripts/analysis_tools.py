# This script is used to analyze the results of the toy brain network simulation.
# It plots the distribution of cycle lengths.

import json
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "../results/"
FIGURES_DIR = "../figures/"

def load_results(filename="toy_results.json"):
    """ Load experiment results from a JSON file """
    with open(os.path.join(RESULTS_DIR, filename), "r") as f:
        return json.load(f)

def plot_cycle_distribution(cycles, filename="cycle_distribution.png"):
    """ Plot the distribution of cycle lengths. """
    cycle_lengths = [len(cycle) for cycle in cycles]
    plt.hist(cycle_lengths, bins=range(1, max(cycle_lengths) + 2), alpha=0.7, color='blue')
    plt.xlabel("Cycle Length")
    plt.ylabel("Frequency")
    plt.title("Distribution of Cycle Lengths in Toy Brain")
    plt.savefig(os.path.join(FIGURES_DIR, filename))
    plt.close()

if __name__ == "__main__":
    # Load and analyze results
    results = load_results()
    cycles = results["cycles"]
    
    # Plot cycle distribution
    plot_cycle_distribution(cycles)
    
    print("Cycle analysis complete. Figures saved in figures directory.")
