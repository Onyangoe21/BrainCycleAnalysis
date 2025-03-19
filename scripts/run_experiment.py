import os
import sys

# Define experiment types
EXPERIMENTS = ["defined_cycles", "overlapping_cycles", "random_graph"]

def run_experiment(experiment):
    """
    Run the specified experiment by calling `simulate_cycles.py`
    and then `real_time_visualization.py`.
    
    :param experiment: Name of the experiment to run
    """
    if experiment not in EXPERIMENTS:
        print(f"❌ Error: Unknown experiment '{experiment}'. Choose from: {EXPERIMENTS}")
        sys.exit(1)

    print(f"🚀 Running experiment: {experiment}")

    # Run the simulation script
    os.system(f"python simulate_cycles.py {experiment}")

    # Run visualization after simulation
    os.system(f"python real_time_visualization.py {experiment}")

    print(f"✅ Experiment '{experiment}' completed successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"❌ Error: No experiment specified. Usage: python run_experiment.py <experiment>")
        print(f"Available experiments: {EXPERIMENTS}")
        sys.exit(1)

    experiment_name = sys.argv[1]
    run_experiment(experiment_name)
