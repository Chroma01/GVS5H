import sys


def compose(outer, inner):
    """Return the transformation outer ∘ inner."""
    result = []
    for row in outer:
        value = row
        combined = 0
        while value:
            bit = value & -value
            idx = bit.bit_length() - 1
            combined |= inner[idx]
            value ^= bit
        result.append(combined)
    return result


def apply_transform(transform, mask):
    result = 0
    for out_bit, dependencies in enumerate(transform):
        if mask & dependencies:
            result |= 1 << out_bit
    return result


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, A, B = data[0:4]
    intervals = []
    pos = 4
    for _ in range(M):
        L, R = data[pos], data[pos + 1]
        pos += 2
        intervals.append((L, R))

    full_mask = (1 << B) - 1

    # State bit k stores reachability of current_position - k.
    # One safe-position transition:
    #   new bit 0 = OR of old bits A-1 through B-1
    #   new bit k = old bit k-1 for k >= 1
    safe = [0] * B
    safe[0] = ((1 << B) - 1) ^ ((1 << (A - 1)) - 1)
    for k in range(1, B):
        safe[k] = 1 << (k - 1)

    # Powers of the safe transition, up to lengths relevant for N.
    powers = [safe]
    for _ in range(N.bit_length()):
        powers.append(compose(powers[-1], powers[-1]))

    def process_safe(mask, length):
        bit = 0
        while length:
            if length & 1:
                mask = apply_transform(powers[bit], mask)
            length >>= 1
            bit += 1
        return mask

    def process_bad(mask, length):
        if length >= B:
            return 0
        return (mask << length) & full_mask

    # Square 1 is reachable and is safe because every bad interval starts > 1.
    state = 1
    current = 2

    for L, R in intervals:
        if current < L:
            state = process_safe(state, L - current)

        state = process_bad(state, R - L + 1)
        current = R + 1

    if current <= N:
        state = process_safe(state, N - current + 1)

    print("Yes" if (state & 1) else "No")


if __name__ == "__main__":
    main()