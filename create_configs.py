import json
import argparse

def create_config(output_file, cache_size, associativity, replacement_policy, cores, memory_entries, protocol):
    """ Creates and saves a configuration file based on provided parameters. """
    print(f"Creating configuration: {output_file}")
    
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
        "log_file": f"log_{output_file.split('.')[0]}.log"  # Unique log file for each config
    }
    
    # Write to JSON file
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=4)

def generate_configs():
    """ Generate multiple configuration files based on predefined combinations of parameters. """
    memory_sizes = [16, 64]
    cache_sizes = [4, 16]
    associativities = {
        4: [1, 2, 4],
        16: [1, 2, 8, 16]
    }
    policies = ["LRU", "RR"]
    cores = 4  # Default number of cores
    protocol = "VI"  # Default protocol

    for policy in policies:
        for memory_size in memory_sizes:
            for cache_size in cache_sizes:
                for assoc in associativities[cache_size]:
                    filename = f"{policy}M{memory_size:02}C{cache_size:02}W{assoc:02}.json"
                    create_config(filename, cache_size, assoc, policy, cores, memory_size, protocol)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate multiple configuration files for cache coherence simulation.")
    parser.add_argument("--generate", action="store_true", help="Generate all predefined configurations.")
    args = parser.parse_args()

    if args.generate:
        generate_configs()
    else:
        print("Use --generate to create configuration files.")

