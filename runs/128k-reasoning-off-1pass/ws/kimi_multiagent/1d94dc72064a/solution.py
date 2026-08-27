import sys
sys.setrecursionlimit(1 << 25)


def solve_game(A):
    """Brute-force winner for small A. Returns True if Fennec (first player) wins.
    State: tuple of remaining tokens per index, frozenset of claimed indices.
    A move: pick i with tokens>0, decrement; if i not claimed, add to claimed.
    If after move claimed == all indices, mover wins."""
    N = len(A)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def win(state, claimed_mask):
        # player to move; returns True if this player can force a win
        full = (1 << N) - 1
        for i in range(N):
            if state[i] <= 0:
                continue
            new_state = list(state)
            new_state[i] -= 1
            new_mask = claimed_mask | (1 << i)
            if new_mask == full:
                return True  # this move wins immediately
            if not win(tuple(new_state), new_mask):
                return True
        return False

    return win(tuple(A), 0)


def rule(A):
    N = len(A)
    c = sum(1 for a in A if a % 2 == 1)
    if N == 1:
        return True
    if N == 2:
        return False
    if N == 3:
        return c >= 1
    return (c % 2) == 1


def cross_check():
    import itertools
    bad = 0
    for N in range(1, 5):
        for A in itertools.product(range(1, 4), repeat=N):
            b = solve_game(A)
            r = rule(A)
            if b != r:
                bad += 1
                print("MISMATCH", N, A, "brute=", b, "rule=", r)
    print("cross-check done, mismatches =", bad)


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    c = sum(1 for x in a if x & 1)
    if n == 1:
        w = True
    elif n == 2:
        w = False
    elif n == 3:
        w = c >= 1
    else:
        w = (c & 1) == 1
    sys.stdout.write("Fennec\n" if w else "Snuke\n")


if __name__ == "__main__":
    # To run the cross-check instead of solving, invoke with argument "check".
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        cross_check()
    else:
        main()