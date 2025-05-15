import time

from rate_limiter.rate_limiter import TokenBucketRateLimiter


def test_single_user_consumption():
    limiter = TokenBucketRateLimiter(rate=2, capacity=4)
    user_id = "al"

    # Initially, 4 tokens available
    assert limiter.consume(user_id)  # 1
    assert limiter.consume(user_id)  # 2
    assert limiter.consume(user_id)  # 3
    assert limiter.consume(user_id)  # 4

    # No tokens left
    assert not limiter.consume(user_id)

    # Wait 1 second (2 tokens added)
    time.sleep(1.1)
    assert limiter.consume(user_id)
    assert limiter.consume(user_id)
    assert not limiter.consume(user_id)  # 3rd should fail


def test_consume_multiple_tokens():
    limiter = TokenBucketRateLimiter(rate=1, capacity=5)
    user_id = "ted"

    assert limiter.consume(user_id, tokens=3)
    assert limiter.consume(user_id, tokens=2)
    assert not limiter.consume(user_id)  # Should be empty now

    # Wait 1 second (1 token)
    time.sleep(1.1)
    assert not limiter.consume(user_id, tokens=2)  # Not enough
    assert limiter.consume(user_id)  # 1 token


def test_multiple_users_independent():
    limiter = TokenBucketRateLimiter(rate=1, capacity=2)
    u1, u2 = "user1", "user2"

    # Each user starts with 2 tokens
    assert limiter.consume(u1)
    assert limiter.consume(u1)
    assert not limiter.consume(u1)

    assert limiter.consume(u2)
    assert limiter.consume(u2)
    assert not limiter.consume(u2)
