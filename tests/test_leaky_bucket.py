import time

from rate_limiter.leaky_bucket import LeakyBucket


def test_accepts_requests_when_bucket_not_full():
    bucket = LeakyBucket(rate=2, capacity=5)
    for _ in range(5):
        assert bucket.consume()  # Should be accepted


def test_rejects_requests_when_bucket_full():
    bucket = LeakyBucket(rate=1, capacity=3)
    # Fill bucket
    for _ in range(3):
        assert bucket.consume()

    # This should be rejected
    assert not bucket.consume()


def test_leaks_over_time():
    bucket = LeakyBucket(rate=2, capacity=4)
    for _ in range(4):
        assert bucket.consume()

    # Should now be full
    assert not bucket.consume()

    # Wait 1.1 sec → should leak ~2.2 tokens
    time.sleep(1.1)
    assert bucket.consume()
    assert bucket.consume()

    # Probably full again now
    assert not bucket.consume()


def test_partial_leak():
    bucket = LeakyBucket(rate=1, capacity=3)
    for _ in range(3):
        assert bucket.consume()

    time.sleep(0.5)  # Not enough to leak a full token
    assert not bucket.consume()

    time.sleep(0.6)  # Total ~1.1 sec, enough for 1 token to leak
    assert bucket.consume()


def test_consume_multiple_tokens():
    bucket = LeakyBucket(rate=2, capacity=5)
    assert bucket.consume(tokens=3)
    assert bucket.consume(tokens=2)
    assert not bucket.consume()  # Full now

    time.sleep(0.6)  # Leaks ~1.2 tokens
    assert bucket.consume(tokens=1)
