import time


class MetricsCounter:
    def __init__(self):
        self.start = time.time()
        self.tick = time.time()
        self.count = 1
        self.wpm = 0
        self.total_characters_typed = 0

    def current_wpm(self):
        self.total_characters_typed += 1

        if self.count % 5 == 0:
            elapsed = self.get_elapsed_time()
            self.wpm = self.total_characters_typed / elapsed / 5
            self.count = 1
            self.tick = time.time()
            return self.wpm
        else:
            self.count += 1
            return self.wpm

    def overall_wpm(self):
        elapsed = self.get_elapsed_time()
        return self.total_characters_typed / elapsed / 5

    def get_elapsed_time(self):
        current_time_minutes = time.time() / 60
        start_time_minutes = self.start / 60
        elapsed_time_minutes = current_time_minutes - start_time_minutes
        return elapsed_time_minutes
