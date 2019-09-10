import time


class Timer:
    def __init__(self):
        self.start = time.time()
        self.elapsed = None

    def tick(self):
        if (self.elapsed == None):
            self.elapsed = time.time()
            return 0.0
        else:
            now = time.time()
            elapsed = now - self.elapsed
            self.elapsed = now
            return elapsed

    def stop(self):
        return time.time() - self.start

class Metrics:
    def __init__(self):
        self.start = time.time()
        self.tick = time.time()
        self.count = 1
        self.cpm = 0
        self.total_characters_typed = 0

    def current_cpm(self):
        self.total_characters_typed += 1

        if self.count % 5 == 0:
            elapsed = self.get_elapsed_time()
            self.cpm = self.total_characters_typed / elapsed
            self.count = 1
            self.tick = time.time()
            return self.cpm
        else:
            self.count += 1
            return self.cpm

    def overall_cpm(self):
        elapsed = self.get_elapsed_time()
        return self.total_characters_typed / elapsed

    def get_elapsed_time(self):
        current_time_minutes = time.time() / 60
        start_time_minutes = self.start / 60
        elapsed_time_minutes = current_time_minutes - start_time_minutes
        return elapsed_time_minutes

