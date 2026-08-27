import sys

def main():
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
    jump_bits = ((1 << B) - 1) ^ ((1 << (A - 1)) - 1)

    # Bit k means that the currently processed position minus k is reachable.
    mask = 1  # Square 1 is reachable.
    current = 1

    def advance_bad(mask, length):
        if length >= B:
            return 0
        return (mask << length) & limit

    if A == B:
        d = A

        def advance_good(mask, length):
            shift = length % d
            if shift == 0:
                return mask
            return ((mask << shift) & limit) | (mask >> (d - shift))
    else:
        # Every sufficiently large integer is representable by A and A+1.
        # C is a valid conductor for those two jump lengths.
        conductor = A * (A - 1)

        # From any reachable position among the previous B positions, one can
        # first jump directly into the good run within A positions.  Afterwards,
        # all sufficiently distant positions are reachable.  This bound also
        # ensures all B stored positions lie in the good run.
        saturation_steps = conductor + A + B - 1

        def advance_good(mask, length):
            if mask == 0:
                return 0

            if length >= saturation_steps:
                return limit

            for _ in range(length):
                new_reachable = 1 if (mask & jump_bits) else 0
                mask = ((mask << 1) & limit) | new_reachable
            return mask

    for L, R in intervals:
        good_length = L - current - 1
        if good_length:
            mask = advance_good(mask, good_length)

        bad_length = R - L + 1
        mask = advance_bad(mask, bad_length)
        current = R

    mask = advance_good(mask, N - current)

    print("Yes" if (mask & 1) else "No")

if __name__ == "__main__":
    main()