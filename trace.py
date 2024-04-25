import json
import random
import argparse

def load_config(path):
    """Loads configuration settings from a JSON file."""
    with open(path, 'r') as file:
        return json.load(file)

def generate_trace_file(filename, num_operations, num_cores, max_address):
    """Generates a trace file with random read (RD) and write (WR) operations."""
    operations = ['RD', 'WR']  # Define possible operations
    with open(filename, 'w') as file:
        for _ in range(num_operations):
            core_id = f"C{random.randint(0, num_cores - 1)}"  # Random core ID from C0 to C3
            operation = random.choice(operations)  # Randomly choose read or write
            address = random.randint(0, max_address)  # Random memory address within the config limit
            file.write(f"{core_id} {operation} {address}\n")

    print(f"Generated {num_operations} trace entries in '{filename}'.")

def main(config_file, trace_file, num_operations):
    """Main function to generate trace file based on configuration settings."""
    config = load_config(config_file)
    num_cores = config['cores']
    max_address = config['memory']['entries'] - 1  # Zero-indexed address range

    generate_trace_file(trace_file, num_operations, num_cores, max_address)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a trace file for cache coherence simulations based on a configuration file.")
    parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration JSON file.")
    parser.add_argument("--trace", type=str, default="trace.tr", help="Filename for the output trace file.")
    parser.add_argument("--operations", type=int, default=100, help="Number of operations to generate in the trace file.")
    args = parser.parse_args()

    main(args.config, args.trace, args.operations)
