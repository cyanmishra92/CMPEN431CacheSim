class VIProtocol:
    def __init__(self, cores):
        self.cores = cores

    def read(self, core, address):
        # Attempt to read the address from the cache
        result = core.cache.access_line(core.cache.find_line(address), address, is_write=False)
        if result is None:
            # Cache miss, handle loading from memory and updating the cache
            line = core.cache.replace_line(core.cache.find_line(address), address, core.memory.storage[address], False)
            line.state = 'V'  # Mark as Valid after loading into cache
        return result

    def write(self, core, address, value):
        # Invalidate all other cores' lines before writing
        self.invalidate_others(core, address)
        # Write the value to the cache, marking the line as Valid
        line = core.cache.access_line(core.cache.find_line(address), address, is_write=True, value=value)
        if line is None:
            # If the line was not in cache, replace a line and write to it
            line = core.cache.replace_line(core.cache.find_line(address), address, value, True)
        line.state = 'V'  # Mark as Valid because it's being written to

    def invalidate_others(self, core, address):
        # Invalidate the line in all other cores
        for other_core in self.cores:
            if other_core != core:
                set_index = other_core.cache.find_line(address)
                set_ = other_core.cache.sets[set_index]
                for line in set_:
                    if line.address == address and line.valid:
                        line.state = 'I'
                        # Optionally flush the line to memory if it's dirty before invalidating
                        other_core.cache.flush_line_to_memory(line)
                        line.valid = False  # Mark the line as invalid

