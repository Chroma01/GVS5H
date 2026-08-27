import sys


def solve():
    input = sys.stdin.readline
    N, M, A, B = map(int, input().split())
    intervals = [tuple(map(int, input().split())) for _ in range(M)]

    full = (1 << B) - 1
    source_mask = full ^ ((1 << (A - 1)) - 1)

    # Bit k represents reachability of position current - k.
    mask = 1  # square 1 is reachable
    current = 1

    def advance_clear(mask, steps):
        if steps <= 0:
            return mask

        if A == B:
            # The transition cyclically rotates the B-bit state.
            shift = steps % B
            for _ in range(shift):
                mask = ((mask << 1) & full) | (mask >> (B - 1))
            return mask

        # For A < B, every nonzero state eventually reaches full.
        # Zero and full are both stable, so long clear stretches can stop early.
        while steps and mask != 0 and mask != full:
            new_bit = 1 if (mask & source_mask) else 0
            mask = ((mask << 1) & full) | new_bit
            steps -= 1

        return mask

    for left, right in intervals:
        # Process the clear region before this blocked interval.
        clear_length = left - 1 - current
        mask = advance_clear(mask, clear_length)
        current = left - 1

        # Every square in the blocked interval contributes an unreachable bit.
        blocked_length = right - left + 1
        if blocked_length >= B:
            mask = 0
        else:
            mask = (mask << blocked_length) & full
        current = right

        if mask == 0:
            print("No")
            return

    mask = advance_clear(mask, N - current)
    print("Yes" if (mask & 1) else "No")


if __name__ == "__main__":
    solve()