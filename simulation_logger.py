import time
import sys

class Logger:
    def __init__(self, cores, memory, log_file_path, display_refresh=True):
        self.cores = cores
        self.memory = memory
        self.log_file = open(log_file_path, "w")
        self.stats = {core.core_id: {'hits': 0, 'misses': 0, 'references': 0} for core in cores}
        self.memory_accesses = 0
        self.display_refresh = display_refresh

    def log_cache_state(self):
        if not self.display_refresh or len(self.cores) > 8:
            return  # Skip display if disabled or too many cores

        sys.stdout.write("\x1b[2J\x1b[H")  # Clear screen and move cursor to home
        print("Cache States (refreshing view):")
        for core in self.cores:
            print(f"Core {core.core_id}:")
            for index, cache_set in enumerate(core.cache.sets):
                set_str = ', '.join(f"{line.state}:{line.address if line.valid else 'Empty'}:{line.value if line.valid else ''}"
                                    for line in cache_set)
                print(f" Set {index}: [{set_str}]")
            stats = self.stats[core.core_id]
            print(f" Hits: {stats['hits']}, Misses: {stats['misses']}, References: {stats['references']}")
        time.sleep(1)  # Delay to allow the display to be readable

    def update_stats(self, core_id, hit):
        self.stats[core_id]['references'] += 1
        if hit:
            self.stats[core_id]['hits'] += 1
        else:
            self.stats[core_id]['misses'] += 1

    def log_event(self, message):
        self.log_file.write(f"{message}\n")

    def close(self):
        self.log_file.close()

    def final_stats(self):
        self.log_file.write("Final Statistics:\n")
        for core_id, stats in self.stats.items():
            hit_rate = stats['hits'] / stats['references'] if stats['references'] > 0 else 0
            miss_rate = stats['misses'] / stats['references'] if stats['references'] > 0 else 0
            self.log_file.write(f"{core_id} - Hits: {stats['hits']}, Misses: {stats['misses']}, Hit Rate: {hit_rate:.2f}, Miss Rate: {miss_rate:.2f}\n")
        self.log_file.write(f"Total Memory Accesses: {self.memory_accesses}\n")

    def update_memory_references(self, hit):
        if not hit:
            self.memory_accesses += 1
