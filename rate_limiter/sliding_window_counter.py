import time
from threading import Lock

class SlidingWindowCounter:
    """
    This algorithm smooths request rate enforcement by approximating a true sliding window
    using two adjacent fixed-size windows (current and previous). It allows up to `limit`
    requests per `window_size_seconds`, calculated using a weighted average of the two windows.

    Compared to the Sliding Window Log, this uses significantly less memory while offering
    nearly the same accuracy — at the cost of being an approximation. 
    """
    def __init__(self, limit, window_size_seconds):
        """
        :param limit: Max allowed requests per sliding window
        :param window_size_seconds: Length of each window in seconds
        """
        self.limit = limit
        self.window_size = window_size_seconds
        self.lock = Lock()

        self._curr_window = 0
        self._prev_window = 0
        self._curr_count = 0
        self._prev_count = 0

    def consume(self):
        now = time.time()
        window_key = self._get_window_key(now)
        weight = self._get_weight(now)

        with self.lock:
            self._rotate_windows_if_needed(window_key)

            estimated_count = self._estimate_total(weight)
            if estimated_count + 1 <= self.limit:
                self._curr_count += 1
                return True
            return False

    def _get_window_key(self, timestamp):
        return int(timestamp // self.window_size)

    def _get_weight(self, timestamp):
        return (timestamp % self.window_size) / self.window_size

    def _rotate_windows_if_needed(self, window_key):
        if window_key != self._curr_window:
            if window_key == self._curr_window + 1:
                # Shift current to previous
                self._prev_window = self._curr_window
                self._prev_count = self._curr_count
            else:
                # Skipped one or more windows: reset both
                self._prev_window = window_key - 1
                self._prev_count = 0
            self._curr_window = window_key
            self._curr_count = 0

    def _estimate_total(self, weight):
        return self._prev_count * (1 - weight) + self._curr_count