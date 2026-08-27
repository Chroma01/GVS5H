import sys


def compose(first, second, width):
    """Return the dependency transform obtained by applying first, then second."""
    result = [0] * width
    for out_bit in range(width):
        deps = second[out_bit]
        combined = 0
        while deps:
            low = deps & -deps
            k = low.bit_length() - 1
            combined |= first[k]
            deps ^= low
        result[out_bit] = combined
    return result


def apply_transform(state, deps, width):
    result = 0
    for out_bit in range(width):
        if state & deps[out_bit]:
            result |= 1 << out_bit
    return result


def build_lifts(base, width, levels):
    lifts = [base]
    for _ in range(1, levels):
        lifts.append(compose(lifts[-1], lifts[-1], width))
    return lifts


def apply_power(state, length, lifts, width):
    bit = 0
    while length:
        if length & 1:
            state = apply_transform(state, lifts[bit], width)
        length >>= 1
        bit += 1
    return state


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, a, b = data[0:4]
    intervals = []
    pos = 4
    for _ in range(m):
        l, r = data[pos], data[pos + 1]
        pos += 2
        intervals.append((l, r))

    width = b

    # One open position:
    # output bit 0 depends on old bits A-1 through B-1;
    # every other output bit is the previous bit immediately to its left.
    open_base = [0] * width
    for bit in range(a - 1, b):
        open_base[0] |= 1 << bit
    for out_bit in range(1, width):
        open_base[out_bit] = 1 << (out_bit - 1)

    # One blocked position: the new position is unreachable, while the
    # previous positions are shifted in the same way.
    blocked_base = [0] * width
    for out_bit in range(1, width):
        blocked_base[out_bit] = 1 << (out_bit - 1)

    levels = n.bit_length() + 1
    open_lifts = build_lifts(open_base, width, levels)
    blocked_lifts = build_lifts(blocked_base, width, levels)

    # Bit 0 denotes the current square; square 1 is initially reachable.
    state = 1
    current = 1

    for left, right in intervals:
        open_length = left - 1 - current
        if open_length:
            state = apply_power(state, open_length, open_lifts, width)

        blocked_length = right - left + 1
        state = apply_power(state, blocked_length, blocked_lifts, width)
        current = right

    remaining = n - current
    if remaining:
        state = apply_power(state, remaining, open_lifts, width)

    print("Yes" if (state & 1) else "No")


if __name__ == "__main__":
    main()