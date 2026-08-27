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

    # A transformation is represented by dependency masks:
    # output bit k is the OR of input bits contained in deps[k].
    good = [0] * B
    good[0] = ((1 << (B - A + 1)) - 1) << (A - 1)
    for k in range(1, B):
        good[k] = 1 << (k - 1)

    bad = good.copy()
    bad[0] = 0

    def compose(first, second):
        """Return the transformation obtained by applying first, then second."""
        result = [0] * B
        for k in range(B):
            selected = second[k]
            dependency = 0
            while selected:
                low = selected & -selected
                j = low.bit_length() - 1
                dependency |= first[j]
                selected -= low
            result[k] = dependency
        return result

    max_bits = N.bit_length()
    powers = [good]
    for _ in range(1, max_bits):
        powers.append(compose(powers[-1], powers[-1]))

    def apply(transform, state):
        result = 0
        for k, dependency in enumerate(transform):
            if dependency & state:
                result |= 1 << k
        return result

    def advance_good(state, steps):
        bit = 0
        while steps:
            if steps & 1:
                state = apply(powers[bit], state)
            steps >>= 1
            bit += 1
        return state

    # Bit k denotes reachability of the square current-k.
    # Initially, square 1 is reachable.
    state = 1
    current = 1

    for L, R in intervals:
        if current >= N:
            break

        # Process the good squares before this bad interval.
        gap = L - current - 1
        if gap > 0:
            state = advance_good(state, gap)
            current += gap

        # Process bad squares. After B consecutive bad squares,
        # every old reachable position has left the sliding window.
        length = R - L + 1
        if length >= B:
            state = 0
        else:
            for _ in range(length):
                state = apply(bad, state)
        current = R

        if state == 0:
            # Reachability can never recover without an initially reachable
            # position, so the final answer is already determined.
            print("No")
            return

    # Process the remaining good suffix, including square N.
    if current < N:
        state = advance_good(state, N - current)

    print("Yes" if (state & 1) else "No")


if __name__ == "__main__":
    solve()