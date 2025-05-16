import time

from rate_limiter.sliding_window_counter import SlidingWindowCounter


def test_allows_within_limit():
    limiter = SlidingWindowCounter(limit=5, window_size_seconds=2)
    for _ in range(5):
        assert limiter.consume()
    assert not limiter.consume()


def test_resets_after_window_rollover():
    limiter = SlidingWindowCounter(limit=3, window_size_seconds=1)
    assert limiter.consume()
    assert limiter.consume()
    assert limiter.consume()
    assert not limiter.consume()
    time.sleep(1.05)  # move to next window
    assert limiter.consume()


def test_gradual_rollover():
    limiter = SlidingWindowCounter(limit=4, window_size_seconds=1)
    assert limiter.consume()
    time.sleep(0.5)
    assert limiter.consume()
    time.sleep(0.5)
    assert limiter.consume()
    assert limiter.consume()
    assert not limiter.consume()
