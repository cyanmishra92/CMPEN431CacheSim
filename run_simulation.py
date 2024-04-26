import subprocess
import os
from concurrent.futures import ProcessPoolExecutor

def run_command(command):
    """ Execute a shell command and handle errors. """
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as error:
        return f"Failed to execute {command}: {error}"

def process_config(config):
    """ Process each configuration: memory, trace, and run main.py """
    config_base = os.path.splitext(config)[0]
    folder_name = config_base[:5]  # Assuming 'LRUM16' or 'RRM16' like prefixes

    # Generate memory and trace files (run only once per batch, check if already run to avoid repetition)
    if not os.path.exists(f"memory{folder_name[-2:]}.mem"):
        run_command(f"python memory.py --config {config}")
        run_command(f"python trace.py --config {config}")

    # Run main simulation
    run_command(f"python main.py --config {config} --log {config_base}.log")

    # Ensure the directory exists and move files
    os.makedirs(folder_name, exist_ok=True)
    subprocess.run(f"mv {config_base}.log {folder_name}/", shell=True)
    subprocess.run(f"mv memory.mem memory{folder_name[-2:]}.mem", shell=True, check=False)
    subprocess.run(f"mv trace.tr trace{folder_name[-2:]}.tr", shell=True, check=False)

def list_json_files(directory):
    """ List all json files in the given directory """
    return [f for f in os.listdir(directory) if f.endswith('.json')]

def main():
    directory = '.'  # Set this to the directory containing your config files
    config_files = list_json_files(directory)

    # Process all configs in parallel maximizing core usage
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_config, config_files))

    for result in results:
        print(result)

if __name__ == "__main__":
    main()

