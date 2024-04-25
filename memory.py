import json
import random
import argparse

def load_config(path):
    """
    Load configuration settings from a JSON file.

    Args:
        path (str): Path to the configuration file.

    Returns:
        dict: Configuration dictionary loaded from the file.
    """
    with open(path, 'r') as file:
        return json.load(file)

def initialize_memory(filename, num_entries):
    """
    Initializes a memory file with random values for each memory location.

    Args:
        filename (str): Filename where the memory initialization will be saved.
        num_entries (int): Number of memory entries to initialize.
    """
    with open(filename, 'w') as file:
        for location in range(num_entries):
            value = random.randint(0, 255)  # Generate random values between 0 and 255
            file.write(f"{location} {value}\n")
    print(f"Memory initialized with {num_entries} entries in '{filename}'.")

def main(config_file, output_file):
    """
    Main function to initialize memory based on the configuration settings.

    Args:
        config_file (str): Path to the configuration JSON file.
        output_file (str): Filename for the initialized memory file.
    """
    config = load_config(config_file)
    num_entries = config['memory']['entries']
    initialize_memory(output_file, num_entries)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize a memory file for cache coherence simulations.")
    parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration JSON file.")
    parser.add_argument("--output", type=str, default="memory.mem", help="Filename for the output memory initialization file.")
    args = parser.parse_args()

    main(args.config, args.output)
