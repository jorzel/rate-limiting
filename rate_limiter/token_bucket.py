import time
from threading import Lock


class TokenBucket:
    """
    A simple implementation of the Token Bucket algorithm for rate limiting.
    This class allows you to control the rate of requests or actions by
    limiting the number of tokens that can be consumed over time.
    The bucket fills at a specified rate, and tokens can be consumed
    when needed. If there are not enough tokens available, the request
    will be denied until more tokens are added to the bucket.
    """
    def __init__(self, rate, capacity):
        """
        :param rate: Tokens added per second
        :param capacity: Maximum number of tokens in the bucket
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.timestamp = time.time()
        self.lock = Lock()

    def _add_tokens(self):
        """
        Add tokens to the bucket based on the elapsed time since the last update.
        This method is called internally and should not be called directly.
        We do not need periodic loop, and update bucket only when it is needed.
        """

        now = time.time()
        elapsed = now - self.timestamp
        new_tokens = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.timestamp = now

    def consume(self, tokens=1):
        """
        Attempt to consume tokens from the bucket.
        :param tokens: Number of tokens to consume
        :return: True if tokens were consumed, False otherwise
        """
        with self.lock:
            self._add_tokens()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


class TokenBucketRateLimiter:
    """
    Rate limiter for multiple users using the Token Bucket algorithm.
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
