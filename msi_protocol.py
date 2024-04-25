class MSIProtocol:
    def __init__(self, cores):
        self.cores = cores

    def read(self, core, address):
        # Check if any other core has this line in 'Modified' state
        for c in self.cores:
            if c != core:
                other_line = self.find_line_in_cache(c.cache, address)
                if other_line and other_line.state == 'M':
                    # Flush to memory and change to 'Shared'
                    self.flush_line_to_memory(other_line)
                    other_line.state = 'S'

        # Handle the read on the requesting core
        line = self.find_line_in_cache(core.cache, address)
        if line:
            if line.state == 'I':
                # If the line is invalid, load from memory and set as 'Shared'
                line = self.load_line_from_memory(core, address)
            return line.value
        else:
            # If the line is not in the cache, load it as 'Shared'
            line = self.load_line_from_memory(core, address)
            return line.value

    def write(self, core, address, value):
        # Invalidate all other caches' lines
        self.invalidate_others(core, address)

        # Handle the write on the requesting core
        line = self.find_line_in_cache(core.cache, address)
        if not line:
            line = self.load_line_from_memory(core, address)
        line.value = value
        line.state = 'M'

    def invalidate_others(self, core, address):
        for other_core in self.cores:
            other_line = self.find_line_in_cache(other_core.cache, address)
            if other_line and other_line.state != 'I':
                other_line.state = 'I'

    def load_line_from_memory(self, core, address):
        line = core.cache.replace_line(core.cache.find_line(address), address, core.memory.storage[address], False)
        line.state = 'S'  # Set as Shared since it may be read by others
        return line

    def flush_line_to_memory(self, line):
        if line.state == 'M':
            line.memory.storage[line.address] = line.value
            line.dirty = False

    def find_line_in_cache(self, cache, address):
        set_index = cache.find_line(address)
        set_ = cache.sets[set_index]
        for line in set_:
            if line.address == address and line.valid:
                return line
        return None
