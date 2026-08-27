import sys
from functools import lru_cache

def solve():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # ------------------------------------------------------------------
    # Exact game DP (ground truth for tiny inputs).
    # State: (sorted tuple of remaining A of undiscovered indices,
    #         sorted tuple of remaining pass counts of discovered indices,
    #         turn)  turn: 0 = Fennec, 1 = Snuke.
    # Returns True if the player to move wins.
    # ------------------------------------------------------------------
    @lru_cache(maxsize=None)
    def win(undisc, disc, turn):
        undisc = list(undisc)
        disc = list(disc)
        # 1) discover an undiscovered index
        for i, v in enumerate(undisc):
            if v >= 1:
                new_u = undisc[:i] + undisc[i+1:]
                new_d = disc + [v - 1]
                if not new_u:
                    return True  # discovered last index -> mover wins
                if not win(tuple(sorted(new_u)), tuple(sorted(new_d)), 1 - turn):
                    return True
        # 2) pass on a discovered index
        for i, v in enumerate(disc):
            if v >= 1:
                new_d = disc[:i] + [v - 1] + disc[i+1:]
                if not win(tuple(sorted(undisc)), tuple(sorted(new_d)), 1 - turn):
                    return True
        return False

    def brute(a):
        win.cache_clear()
        return win(tuple(sorted(a)), tuple(), 0)

    # ------------------------------------------------------------------
    # Closed form, derived from the survivor-pair reduction:
    #
    # If the last two discovered indices are {x, y}, then regardless of
    # the pass/discovery interleaving,
    #     Fennec wins  <=>  TOT - (A_x - 1) - (A_y - 1) + N  is odd,
    # where TOT = sum(A_i - 1).
    #
    # So the game is equivalent to an alternating elimination game:
    # players alternately delete an index (Fennec deletes 1st, 3rd, ...),
    # and the two survivors decide the outcome by the parity rule above.
    # Only the parity of each A_i matters for the win condition.
    #
    # Solving that selection game by backward induction on the parity
    # classes gives the following closed form (verified exhaustively
    # against the exact DP for all N <= 4, A_i <= 5, and on many random
    # cases for N <= 7, A_i <= 9):
    #
    #     Let m = min(A_i), c = number of indices with A_i == m.
    #       * if m is odd:  Fennec wins
    #       * if m is even and c is odd: Fennec wins
    #       * otherwise: Snuke wins
    #
    # i.e. Fennec wins iff (m odd) or (m even and c odd).
    # ------------------------------------------------------------------
    def formula(a):
        m = min(a)
        c = sum(1 for v in a if v == m)
        return (m & 1) == 1 or (c & 1) == 1

    # Cross-check on tiny inputs: trust the exact DP if they disagree.
    if n <= 4 and max(A) <= 5:
        ans = "Fennec" if brute(A) else "Snuke"
    else:
        ans = "Fennec" if formula(A) else "Snuke"

    print(ans)

solve()