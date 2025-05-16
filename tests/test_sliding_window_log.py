import time

from rate_limiter.sliding_window_log import SlidingWindowLog


def test_allows_within_limit():
    limiter = SlidingWindowLog(limit=3, window_size_seconds=2)
    assert limiter.consume()
    assert limiter.consume()
    assert limiter.consume()
    assert not limiter.consume()


def test_expiry_allows_new_requests():
    limiter = SlidingWindowLog(limit=2, window_size_seconds=1)
    assert limiter.consume()
    assert limiter.consume()
    assert not limiter.consume()
    time.sleep(1.1)
    assert limiter.consume()
    assert limiter.consume()
    assert not limiter.consume()
