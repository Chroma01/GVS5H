import sys


def compose(left, right, b):
    """Return the Boolean matrix left ○ right, represented by row bitmasks."""
    result = [0] * b
    for i, mask in enumerate(left):
        row = 0
        while mask:
            low = mask & -mask
            j = low.bit_length() - 1
            row |= right[j]
            mask -= low
        result[i] = row
    return result


def apply_matrix(mat, vec):
    """Apply a Boolean matrix, represented by row bitmasks, to a bit vector."""
    out = 0
    for i, row in enumerate(mat):
        if row & vec:
            out |= 1 << i
    return out


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, a, b = data[:4]
    intervals = []
    p = 4
    for _ in range(m):
        l, r = data[p], data[p + 1]
        intervals.append((l, r))
        p += 2

    # State bit k means: dp[current_position - k] is reachable.
    # Matrix for appending one safe position.
    safe = [0] * b
    for d in range(a, b + 1):
        safe[0] |= 1 << (d - 1)
    for i in range(1, b):
        safe[i] = 1 << (i - 1)

    powers = [safe]
    for _ in range(1, n.bit_length()):
        powers.append(compose(powers[-1], powers[-1], b))

    mask_b = (1 << b) - 1

    def advance_safe(vec, count):
        bit = 0
        while count:
            if count & 1:
                vec = apply_matrix(powers[bit], vec)
            count >>= 1
            bit += 1
        return vec

    current = 1
    state = 1  # Square 1 is initially reachable.

    for l, r in intervals:
        # Process safe squares from current+1 through l-1.
        state = advance_safe(state, l - current - 1)

        # Every bad square appends a zero reachability bit.
        bad_length = r - l + 1
        if bad_length >= b:
            state = 0
        else:
            state = (state << bad_length) & mask_b

        current = r

    # Process the final safe segment through square N.
    state = advance_safe(state, n - current)

    print("Yes" if (state & 1) else "No")


if __name__ == "__main__":
    main()