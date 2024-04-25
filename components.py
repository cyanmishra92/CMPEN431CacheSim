import json
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class CacheLine:
    """Represents a single line in a cache set."""
    def __init__(self):
        self.address = None
        self.value = None
        self.valid = False
        self.dirty = False
        self.state = 'I'
        self.last_used = 0

class SetAssociativeCache:
    """Implements set-associative cache logic."""
    def __init__(self, size, associativity, replacement_policy, memory):
        self.size = size
        self.associativity = associativity
        self.replacement_policy = replacement_policy
        self.sets = [[CacheLine() for _ in range(associativity)] for _ in range(size // associativity)]
        self.access_counter = 0
        self.rr_index = [0] * (self.size // self.associativity)
        self.memory = memory

    def flush_line_to_memory(self, line):
        if line.dirty and line.valid:
            self.memory.storage[line.address] = line.value
            line.dirty = False
            logger.debug(f"Flushing modified line to memory at address {line.address}")

    def find_line(self, address):
        return address % (self.size // self.associativity)

    def access_line(self, set_index, address, is_write, value=None):
        set_ = self.sets[set_index]
        for line in set_:
            if line.valid and line.address == address:
                if is_write:
                    line.value = value
                    line.state = 'M'
                    line.dirty = True
                line.last_used = self.access_counter
                self.access_counter += 1
                return line.value
        return self.replace_line(set_index, address, value, is_write)

    def replace_line(self, set_index, address, value, is_write):
        set_ = self.sets[set_index]
        if self.replacement_policy == 'LRU':
            line = min(set_, key=lambda x: x.last_used)
        elif self.replacement_policy == 'RR':
            line = set_[self.rr_index[set_index]]
            self.rr_index[set_index] = (self.rr_index[set_index] + 1) % self.associativity
        else:
            raise ValueError("Unsupported replacement policy")
        self.flush_line_to_memory(line)
        line.address = address
        line.valid = True
        line.value = value if is_write else line.value
        line.state = 'M' if is_write else line.state
        line.last_used = self.access_counter
        self.access_counter += 1
        return None

class Core:
    """Represents a processor core with a local cache."""
    def __init__(self, core_id, bus, cache_size, associativity, replacement_policy, memory):
        self.core_id = core_id
        self.cache = SetAssociativeCache(cache_size, associativity, replacement_policy, memory)
        self.bus = bus

    def read_from_cache(self, address):
        return self.cache.access_line(self.cache.find_line(address), address, is_write=False)

    def write_to_cache(self, address, value):
        self.cache.access_line(self.cache.find_line(address), address, is_write=True, value=value)

class Memory:
    """Represents the main memory."""
    def __init__(self, size):
        self.storage = {i: random.randint(0, 255) for i in range(size)}

class Bus:
    """Represents a bus connecting multiple cores."""
    def __init__(self, cores):
        self.cores = cores

def load_config(path):
    """Loads configuration from a JSON file."""
    with open(path) as file:
        return json.load(file)

def initialize_system(config):
    """Initializes the system based on a configuration."""
    memory = Memory(config['memory']['entries'])
    cores = [Core(f"C{i}", None, config['cache']['size'], config['cache']['associativity'], config['cache']['replacement_policy'], memory) for i in range(config['cores'])]
    bus = Bus(cores)
    for core in cores:
        core.bus = bus
    return cores, memory, bus
