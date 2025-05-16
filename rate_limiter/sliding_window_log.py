import time
from collections import deque
from threading import Lock


class SlidingWindowLog:
    """
    A simple implementation of the Sliding Window Log algorithm for rate limiting.
    The algorithm allows a request if the number of requests within
    the last `window_size_seconds` is below the `limit`.
    Provides finer-grained control than Fixed Window (no burst at edges).
    """
    def __init__(self, limit, window_size_seconds):
        """
        :param limit: Max allowed requests per window
        :param window_size_seconds: Time window in seconds
        """
        self.limit = limit
        self.window_size = window_size_seconds
        self.timestamps = deque()
        self.lock = Lock()

    def _cleanup(self):
        """
        Remove timestamps that are outside the current sliding window.
        This method is called internally and should not be called directly.
        """
        now = time.time()
        while self.timestamps and (now - self.timestamps[0] > self.window_size):
            self.timestamps.popleft()

    def consume(self):
        """
        Attempt to consume 1 token from the sliding window.
        Returns True if allowed, False otherwise.
        """
        now = time.time()
        with self.lock:
            self._cleanup()
            if len(self.timestamps) < self.limit:
                self.timestamps.append(now)
                return True
            return False