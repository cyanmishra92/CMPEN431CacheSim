import json
import random
import argparse
import uuid

def load_config(path):
    """Loads configuration settings from a JSON file."""
    with open(path, 'r') as file:
        return json.load(file)

def read_uuid_from_file(uuid_file):
    """Reads the UUID from a file."""
    with open(uuid_file, 'r') as file:
        return file.read().strip()

def generate_trace_file(filename, num_operations, num_cores, max_address, seed):
    """Generates a trace file with random read (RD) and write (WR) operations."""
    # Convert the seed from UUID string to an integer
    seed_uuid = uuid.UUID(seed)
    random.seed(seed_uuid.int)  # Seed the random number generator for reproducibility
    operations = ['RD', 'WR']
    with open(filename, 'w') as file:
        for _ in range(num_operations):
            core_id = f"C{random.randint(0, num_cores - 1)}"
            operation = random.choice(operations)
            address = random.randint(0, max_address)
            file.write(f"{core_id} {operation} {address}\n")

    print(f"Generated {num_operations} trace entries in '{filename}'.")

def main(config_file, trace_file, num_operations, uuid_file):
    """Main function to generate trace file based on configuration settings and UUID."""
    config = load_config(config_file)
    num_cores = config['cores']
    max_address = config['memory']['entries'] - 1  # Zero-indexed address range
    seed = read_uuid_from_file(uuid_file)

    generate_trace_file(trace_file, num_operations, num_cores, max_address, seed)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a trace file for cache coherence simulations based on a configuration file.")
    parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration JSON file.")
    parser.add_argument("--trace", type=str, default="trace.tr", help="Filename for the output trace file.")
    parser.add_argument("--operations", type=int, default=100, help="Number of operations to generate in the trace file.")
    parser.add_argument("--uuid", type=str, default="seed_uuid.txt", help="Path to the file containing the UUID seed.")
    args = parser.parse_args()

    main(args.config, args.trace, args.operations, args.uuid)
