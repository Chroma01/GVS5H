import sys


def solve():
    input = sys.stdin.readline
    N, M, A, B = map(int, input().split())
    intervals = [tuple(map(int, input().split())) for _ in range(M)]

    full = (1 << B) - 1
    candidate_mask = ((1 << (B - A + 1)) - 1) << (A - 1)

    def free_step(state):
        can_reach = state & candidate_mask
        return ((state << 1) & full) | (1 if can_reach else 0)

    def advance_free(state, count):
        if count <= 0 or state == 0:
            return state

        if A == B:
            shift = count % B
            if shift == 0:
                return state
            return ((state << shift) & full) | (state >> (B - shift))

        if state == full:
            return state

        # Every integer s >= A * (A - 1) can be represented
        # using jumps A and A + 1.
        threshold = A * (A - 1)

        # From any reachable position represented in the state, first
        # take a jump of B, then use A/A+1 jumps. This guarantees that
        # after this many free positions the whole rolling window is
        # reachable.
        limit = threshold + 2 * B - 1
        steps = min(count, limit)

        for _ in range(steps):
            state = free_step(state)
            if state == full:
                break

        return state

    def advance_bad(state, count):
        if count <= 0:
            return state
        if count >= B:
            return 0
        return (state << count) & full

    current = 1
    state = 1

    for left, right in intervals:
        state = advance_free(state, left - current - 1)
        state = advance_bad(state, right - left + 1)
        current = right

    state = advance_free(state, N - current)

    print("Yes" if (state & 1) else "No")


if __name__ == "__main__":
    solve()