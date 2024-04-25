import random
import argparse
from components import load_config, initialize_system
from vi_protocol import VIProtocol as VI
from msi_protocol import MSIProtocol as MSI
from mesi_protocol import MESIProtocol as MESI
from simulation_logger import Logger  # Assuming you renamed logging.py to simulation_logger.py

def simulate_trace(filename, cores, logger):
    """Simulates the execution of trace commands from a trace file."""
    try:
        with open(filename) as file:
            for line_number, line in enumerate(file, 1):
                try:
                    core_id, function, address = line.strip().split()
                    core = cores[int(core_id[1])]  # Select the correct core by ID
                    address = int(address)
                    if function == 'RD':
                        value = core.read_from_cache(address)
                        hit = value is not None
                    elif function == 'WR':
                        value = random.randint(1, 100)
                        core.write_to_cache(address, value)
                        hit = True  # Assuming always hit on write
                    logger.log_event(f"{core_id} {function} {value} at address {address} - {'Hit' if hit else 'Miss'}")
                    logger.update_memory_references(hit)
                    logger.update_stats(core_id, hit)
                    logger.log_cache_state()
                except Exception as e:
                    print(f"Error processing line {line_number}: {line.strip()} - {e}")
    except FileNotFoundError:
        print(f"Error: Trace file {filename} not found.")
        sys.exit(1)

def main(config_file, trace_file, log_file):
    try:
        config = load_config(config_file)
        cores, memory, bus = initialize_system(config)
    except FileNotFoundError:
        print(f"Error: Configuration file {config_file} not found.")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing necessary configuration key {e}.")
        sys.exit(1)

    protocol_class = {'VI': VI, 'MSI': MSI, 'MESI': MESI}.get(config['protocol'], MSI)
    protocol = protocol_class(cores)
    for core in cores:
        core.protocol = protocol
    logger = Logger(cores, memory, log_file)
    simulate_trace(trace_file, cores, logger)
    logger.final_stats()
    logger.close()

def parse_args():
    parser = argparse.ArgumentParser(description="Run a cache coherence protocol simulation.")
    parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration JSON file.")
    parser.add_argument("--trace", type=str, default="trace.tr", help="Path to the trace file with read/write operations.")
    parser.add_argument("--log", type=str, default="mesi.log", help="Path to the output log file for simulation results.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args.config, args.trace, args.log)
