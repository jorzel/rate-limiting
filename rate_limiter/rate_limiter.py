from threading import Lock

from .token_bucket import TokenBucket


class TokenBucketRateLimiter:
    """
    Rate limiter for multiple users using algorithm.
    Each user gets their own token bucket.
    """
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.buckets = {}
        self.locks = {}
        self.global_lock = Lock()  # To protect creation of per-user locks and buckets

    def _get_bucket(self, user_id):
        if user_id not in self.buckets:
            with self.global_lock:
                if user_id not in self.buckets:
                    self.buckets[user_id] = TokenBucket(self.rate, self.capacity)
                    self.locks[user_id] = Lock()
        return self.buckets[user_id], self.locks[user_id]

    def consume(self, user_id, tokens=1):
        bucket, lock = self._get_bucket(user_id)
        with lock:
            return bucket.consume(tokens)
