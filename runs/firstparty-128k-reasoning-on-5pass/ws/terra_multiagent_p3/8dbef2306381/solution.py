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

    full = (1 << B) - 1
    jump_mask = ((1 << (B - A + 1)) - 1) << (A - 1)

    # state bit k: reachability of current processed position - k.
    # Initially, position 1 is reachable and has been processed.
    state = 1
    pos = 1

    def step_safe(s):
        can_reach = 1 if (s & jump_mask) else 0
        return ((s << 1) & full) | can_reach

    def advance_bad(s, length):
        if length >= B:
            return 0
        return (s << length) & full

    def advance_safe_fixed(s, length):
        # For A == B, the state transition is a rotation of A bits.
        for _ in range(length % A):
            can_reach = (s >> (A - 1)) & 1
            s = ((s << 1) & full) | can_reach
        return s

    def advance_safe_variable(s, length):
        if length == 0 or s == 0:
            return s

        if length <= saturation_steps:
            for _ in range(length):
                s = step_safe(s)
            return s

        # Process enough initial positions to determine whether any reachable
        # square enters this safe segment. Afterwards, for A < B, all
        # sufficiently later positions become reachable.
        for _ in range(saturation_steps):
            s = step_safe(s)

        # The proof of saturation gives exactly these two possible states.
        return full if s else 0

    if A < B:
        # For k >= K, [kA, kB] and [(k+1)A, (k+1)B] overlap/touch.
        # Thus every distance at least K*A is representable.
        K = (A - 1 + (B - A) - 1) // (B - A)
        saturation_steps = 2 * B + K * A

    def advance_safe(s, length):
        if length <= 0:
            return s
        if A == B:
            return advance_safe_fixed(s, length)
        return advance_safe_variable(s, length)

    for L, R in intervals:
        # Safe positions strictly after pos and before the bad interval.
        safe_length = L - pos - 1
        state = advance_safe(state, safe_length)
        pos = L - 1

        # Process bad positions L through R.
        state = advance_bad(state, R - L + 1)
        pos = R

    # Process all remaining safe positions through N.
    state = advance_safe(state, N - pos)

    print("Yes" if (state & 1) else "No")


if __name__ == "__main__":
    main()