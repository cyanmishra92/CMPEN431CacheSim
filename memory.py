import json
import random
import argparse
import uuid

def load_config(path):
    """Load configuration settings from a JSON file."""
    with open(path, 'r') as file:
        return json.load(file)

def read_uuid_from_file(uuid_file):
    """Reads the UUID from a file."""
    with open(uuid_file, 'r') as file:
        return file.read().strip()

def initialize_memory(filename, num_entries, seed):
    """Initializes a memory file with random values for each memory location."""
    # Seed the random number generator for reproducibility
    seed_uuid = uuid.UUID(seed)
    random.seed(seed_uuid.int)  # Convert UUID to a large integer for seeding
    with open(filename, 'w') as file:
        for location in range(num_entries):
            value = random.randint(0, 255)  # Generate random values between 0 and 255
            file.write(f"{location} {value}\n")
    print(f"Memory initialized with {num_entries} entries in '{filename}'.")

def main(config_file, output_file, uuid_file):
    """Main function to initialize memory based on the configuration settings and a UUID."""
    config = load_config(config_file)
    num_entries = config['memory']['entries']
    seed = read_uuid_from_file(uuid_file)
    initialize_memory(output_file, num_entries, seed)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize a memory file for cache coherence simulations.")
    parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration JSON file.")
    parser.add_argument("--output", type=str, default="memory.mem", help="Filename for the output memory initialization file.")
    parser.add_argument("--uuid", type=str, default="seed_uuid.txt", help="Path to the file containing the UUID seed.")
    args = parser.parse_args()

    main(args.config, args.output, args.uuid)
