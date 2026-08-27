import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, a, b = data[0:4]
    intervals = []
    p = 4
    for _ in range(m):
        l, r = data[p], data[p + 1]
        p += 2
        intervals.append((l, r))

    full_mask = (1 << b) - 1
    transition_mask = ((1 << (b - a + 1)) - 1) << (a - 1)

    def advance_free(state: int, length: int) -> int:
        if length <= 0 or state == 0:
            return state

        if a == b:
            # dp[x] = dp[x-a], so the B-bit state rotates periodically.
            for _ in range(length % a):
                oldest = (state >> (a - 1)) & 1
                state = ((state << 1) & full_mask) | oldest
            return state

        # Since [a, b] contains both a and a+1, every integer at least
        # a*(a-1) is representable as a sum of allowed step lengths.
        # Therefore every nonzero state reaches all ones within this many
        # appended free positions.
        limit = min(length, a * (a - 1) + b)

        for _ in range(limit):
            new_bit = 1 if (state & transition_mask) else 0
            state = ((state << 1) & full_mask) | new_bit
            if state == full_mask:
                return full_mask

        return state

    # Bit k stores reachability of current_position - k.
    state = 1  # square 1 is reachable
    current = 1

    for left, right in intervals:
        free_length = left - current - 1
        state = advance_free(state, free_length)
        current = left - 1

        bad_length = right - left + 1
        if bad_length >= b:
            state = 0
        else:
            state = (state << bad_length) & full_mask
        current = right

    state = advance_free(state, n - current)
    print("Yes" if (state & 1) else "No")


if __name__ == "__main__":
    solve()