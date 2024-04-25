import json
import argparse

def get_input(prompt, default=None):
    """ Helper function to get input with a default value.
    :param prompt: The prompt to display to the user.
    :param default: The default value to return if no input is provided.
    :return: The user's input or the default value if no input is provided.
    """
    user_input = input(f"{prompt} (default {default}): ").strip()
    return user_input if user_input else default

def create_config(output_file):
    """ Creates and saves a configuration file based on user input.
    :param output_file: The filename where the configuration will be saved.
    """
    print("Configuration Setup for Cache Coherence Simulation")

    # Cache configuration with default values
    cache_size = int(get_input("Enter total number of cache lines", "8"))
    associativity = int(get_input("Enter cache associativity (e.g., 2 for 2-way set associative)", "2"))
    replacement_policy = get_input("Enter replacement policy (LRU or RR)", "LRU")
    
    # Cores configuration with default values
    cores = int(get_input("Enter the number of cores", "4"))
    
    # Memory configuration with default values
    memory_entries = int(get_input("Enter the total number of memory locations", "16"))
    
    # Protocol selection with default values
    protocol = get_input("Enter the cache coherence protocol (VI, MSI, or MESI)", "MSI")
    
    # Log file location with default values
    log_file = get_input("Enter log file name", "simulation.log")
    
    # Create the configuration dictionary
    config = {
        "cache": {
            "size": cache_size,
            "associativity": associativity,
            "replacement_policy": replacement_policy
        },
        "cores": cores,
        "memory": {
            "entries": memory_entries
        },
        "protocol": protocol,
        "log_file": log_file
    }
    
    # Write to JSON file
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a configuration file for cache coherence simulation.")
    parser.add_argument("--output", type=str, default="config.json", help="Filename for the output configuration JSON file.")
    args = parser.parse_args()

    create_config(args.output)
