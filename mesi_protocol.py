class MESIProtocol:
    def __init__(self, cores):
        self.cores = cores

    def read(self, core, address):
        sharing_cores = [c for c in self.cores if c != core and self.find_line_in_cache(c.cache, address)]
        line = self.find_line_in_cache(core.cache, address)

        if not line:
            line = self.load_line_from_memory(core, address, sharing_cores)

        if line.state == 'I':
            if any(c.cache.find_line_in_cache(address).state == 'M' for c in sharing_cores):
                for c in sharing_cores:
                    self.flush_if_modified(c.cache.find_line_in_cache(address))
                    c.cache.find_line_in_cache(address).state = 'S'
            line.state = 'S' if sharing_cores else 'E'

        return line.value

    def write(self, core, address, value):
        self.invalidate_others(core, address)
        line = self.find_line_in_cache(core.cache, address)
        if not line:
            line = self.load_line_from_memory(core, address)

        if line.state == 'E' or line.state == 'S':
            self.flush_if_modified(line)
        
        line.value = value
        line.state = 'M'

    def invalidate_others(self, core, address):
        for other_core in self.cores:
            if other_core != core:
                line = self.find_line_in_cache(other_core.cache, address)
                if line and line.state != 'I':
                    self.flush_if_modified(line)
                    line.state = 'I'

    def load_line_from_memory(self, core, address, sharing_cores):
        is_shared = any(self.find_line_in_cache(c.cache, address) for c in sharing_cores if c != core)
        line = core.cache.replace_line(core.cache.find_line(address), address, core.memory.storage[address], False)
        line.state = 'S' if is_shared else 'E'
        return line

    def find_line_in_cache(self, cache, address):
        set_index = cache.find_line(address)
        set_ = cache.sets[set_index]
        for line in set_:
            if line.address == address and line.valid:
                return line
        return None

    def flush_if_modified(self, line):
        if line.state == 'M':
            line.memory.storage[line.address] = line.value  # Flush to memory
            line.dirty = False
