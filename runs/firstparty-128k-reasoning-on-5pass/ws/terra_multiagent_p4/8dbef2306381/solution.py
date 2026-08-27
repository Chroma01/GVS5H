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

    full = (1 << B) - 1
    mask = 1  # bit d: reachability of current_position - d
    current = 1

    if A < B:
        d = B - A
        c = B - 1 + A * ((A - 1 + d - 1) // d)

        def advance_good(mask, length):
            if length <= 0 or mask == 0:
                return mask

            steps = min(length, c)
            for _ in range(steps):
                reachable = (mask >> (A - 1)) & ((1 << (B - A + 1)) - 1)
                mask = ((mask << 1) & full) | (1 if reachable else 0)

            if length > steps and mask:
                mask = full
            return mask

    else:
        def advance_good(mask, length):
            if length == 0 or mask == 0:
                return mask
            r = length % B
            if r == 0:
                return mask
            return ((mask << r) & full) | (mask >> (B - r))

    def advance_bad(mask, length):
        if length >= B:
            return 0
        return (mask << length) & full

    for L, R in intervals:
        good_length = L - current - 1
        mask = advance_good(mask, good_length)

        bad_length = R - L + 1
        mask = advance_bad(mask, bad_length)
        current = R

    mask = advance_good(mask, N - current)

    print("Yes" if (mask & 1) else "No")


if __name__ == "__main__":
    solve()