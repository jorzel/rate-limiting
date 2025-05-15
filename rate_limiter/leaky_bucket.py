import time
import threading


class LeakyBucket:
    """
    Leaky bucket rate limiter: allows requests at a fixed leak rate.
    If the bucket is full, incoming requests are rejected.
    """
    def __init__(self, rate: float, capacity: int):
        """
        :param rate: Leak rate (requests per second)
        :param capacity: Max number of requests the bucket can hold
        """
        self.rate = rate  # leak rate in requests per second
        self.capacity = capacity
        self.queue = 0
        self.last_check = time.monotonic()
        self.lock = threading.Lock()

    def _leak(self):
        now = time.monotonic()
        elapsed = now - self.last_check
        leaked = elapsed * self.rate
        self.queue = max(0, self.queue - leaked)
        self.last_check = now

    def consume(self, tokens: int = 1) -> bool:
        """
        Try to add tokens to the bucket.
        :param tokens: Number of tokens to add (default: 1)
        :return: True if allowed, False if rejected
        """
        with self.lock:
            self._leak()
            if self.queue + tokens <= self.capacity:
                self.queue += tokens
                return True
            else:
                return False
