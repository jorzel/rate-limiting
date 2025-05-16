import time
from rate_limiter.fixed_window import FixedWindow


def test_allows_within_limit():
    fw = FixedWindow(limit=5, window_size_seconds=2)
    for _ in range(5):
        assert fw.consume()


def test_blocks_when_limit_exceeded():
    fw = FixedWindow(limit=3, window_size_seconds=2)
    for _ in range(3):
        assert fw.consume()
    assert not fw.consume()


def test_resets_after_window():
    fw = FixedWindow(limit=2, window_size_seconds=1)
    assert fw.consume()
    assert fw.consume()
    assert not fw.consume()
    time.sleep(1.1)  # Move into new window
    assert fw.consume()


def test_consume_multiple_tokens():
    fw = FixedWindow(limit=5, window_size_seconds=2)
    assert fw.consume(tokens=3)
    assert fw.consume(tokens=2)
    assert not fw.consume(tokens=1)
