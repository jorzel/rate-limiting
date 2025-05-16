import time
from threading import Lock


class FixedWindow:
    """
    A simple implementation of the Fixed Window algorithm for rate limiting.
    This class allows you to control the rate of requests or actions by
    limiting the number of requests that can be made in a fixed time window.
    The window resets after the specified time period, allowing a new set
    of requests to be made.
    This algorithms allows burst traffic at the edge of the window.
    """
    def __init__(self, limit, window_size_seconds):
        """
        :param limit: Max number of allowed requests per window
        :param window_size_seconds: Time window in seconds
        """
        self.limit = limit
        self.window_size = window_size_seconds
        self.window_start = int(time.time() // self.window_size)
        self.counter = 0
        self.lock = Lock()

    def _get_current_window(self):
        return int(time.time() // self.window_size)

    def consume(self, tokens=1):
        """
        Attempt to consume 'tokens' from the bucket.
        Returns True if allowed, False otherwise.
        """
        with self.lock:
            current_window = self._get_current_window()
            if current_window != self.window_start:
                # New window: reset
                self.window_start = current_window
                self.counter = 0

            if self.counter + tokens <= self.limit:
                self.counter += tokens
                return True
            return False
