import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    N = next(it)
    M = next(it)
    A = next(it)
    B = next(it)

    intervals = [(next(it), next(it)) for _ in range(M)]

    limit = (1 << B) - 1
    source_mask = ((1 << (B - A + 1)) - 1) << (A - 1)

    def good_step(state):
        reachable = 1 if (state & source_mask) else 0
        return ((state << 1) & limit) | reachable

    def advance_good(state, count):
        if count == 0:
            return state

        # The state machine has only B bits. In fact, for A < B it quickly
        # reaches either the all-zero or all-one fixed state; for A == B it
        # becomes periodic with period A. Cycle detection fast-forwards any
        # very long uninterrupted good segment.
        seen = {}
        steps = 0

        while steps < count:
            previous = seen.get(state, -1)
            if previous != -1:
                period = steps - previous
                remaining = (count - steps) % period
                for _ in range(remaining):
                    state = good_step(state)
                return state

            seen[state] = steps
            state = good_step(state)
            steps += 1

        return state

    def advance_bad(state, count):
        if count >= B:
            return 0
        return (state << count) & limit

    # Bit 0 represents reachability of the current coordinate.
    # Initially, square 1 is reachable.
    state = 1
    current = 1

    for left, right in intervals:
        good_count = left - current - 1
        state = advance_good(state, good_count)

        bad_count = right - left + 1
        state = advance_bad(state, bad_count)
        current = right

    state = advance_good(state, N - current)

    print("Yes" if (state & 1) else "No")


if __name__ == "__main__":
    solve()