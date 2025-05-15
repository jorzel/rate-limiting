import time
from rate_limiter.token_bucket import TokenBucket


def test_initial_state():
    bucket = TokenBucket(rate=1, capacity=5)

    assert bucket.consume()  # Should be able to consume immediately


def test_capacity_limit():
    _capacity = 3
    bucket = TokenBucket(rate=1, capacity=_capacity)
    for _ in range(_capacity):
        assert bucket.consume()

    assert not bucket.consume()  # Exceeds capacity


def test_token_replenishment():
    _capacity = 5
    bucket = TokenBucket(rate=2, capacity=_capacity)
    for _ in range(_capacity):
        assert bucket.consume()
    assert not bucket.consume()

    time.sleep(1)  # Wait for 2 tokens to be added
    assert bucket.consume()
    assert bucket.consume()
    assert not bucket.consume()


def test_partial_token_addition():
    _capacity = 5
    bucket = TokenBucket(rate=1, capacity=_capacity)
    for _ in range(_capacity):
        assert bucket.consume()

    time.sleep(0.5)
    assert not bucket.consume()  # Not enough tokens yet
    time.sleep(0.6)  # Now it should have at least 1 token
    assert bucket.consume()
