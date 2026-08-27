from typing import List
from bisect import bisect_left
from itertools import combinations
import random


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        # Sort by right endpoint while preserving original 0-based indices.
        items = []
        for idx, (l, r, w) in enumerate(intervals):
            items.append((r, l, w, idx))
        items.sort(key=lambda x: (x[0], x[1], x[3]))

        rights = [x[0] for x in items]

        # pref[i] = number of sorted intervals whose right endpoint is
        # strictly less than items[i].l. Strict '<' because touching overlaps.
        pref = [0] * n
        for i, (_, l, _, _) in enumerate(items):
            pref[i] = bisect_left(rights, l)

        def better(a, b) -> bool:
            # True iff a beats b: higher weight, then lexicographically
            # smaller sorted tuple of original indices.
            if b is None:
                return True
            return a[0] > b[0] or (a[0] == b[0] and a[1] < b[1])

        # dp[i][k] = best (weight, sorted_original_index_tuple) using exactly
        # k intervals among the first i intervals in right-endpoint order.
        dp = [[None] * 5 for _ in range(n + 1)]
        dp[0][0] = (0, ())

        for i in range(1, n + 1):
            _, l, w, idx = items[i - 1]
            p = pref[i - 1]

            for k in range(5):
                best = dp[i - 1][k]  # skip current interval

                if k > 0:
                    prev_state = dp[p][k - 1]
                    if prev_state is not None:
                        cand_tuple = tuple(sorted(prev_state[1] + (idx,)))
                        cand = (prev_state[0] + w, cand_tuple)
                        if better(cand, best):
                            best = cand

                dp[i][k] = best

        ans = dp[n][0]
        for k in range(1, 5):
            cand = dp[n][k]
            if cand is not None and better(cand, ans):
                ans = cand

        return list(ans[1])


def brute_force(intervals: List[List[int]]) -> List[int]:
    """Exhaustively check every subset of size <= 4."""
    n = len(intervals)
    best_w = 0
    best_t = ()

    for k in range(0, min(4, n) + 1):
        for comb in combinations(range(n), k):
            ok = True
            for a in range(k):
                for b in range(a + 1, k):
                    i, j = comb[a], comb[b]
                    l1, r1, _ = intervals[i]
                    l2, r2, _ = intervals[j]
                    # Non-overlapping iff one ends strictly before the other starts.
                    if not (r1 < l2 or r2 < l1):
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue

            w = sum(intervals[i][2] for i in comb)
            t = tuple(sorted(comb))
            if w > best_w or (w == best_w and t < best_t):
                best_w, best_t = w, t

    return list(best_t)


def check_case(intervals: List[List[int]], expected=None) -> None:
    got = Solution().maximumWeight(intervals)
    ref = brute_force(intervals)
    if got != ref:
        print("MISMATCH")
        print("intervals =", intervals)
        print("dp        =", got)
        print("brute     =", ref)
        raise AssertionError("DP disagrees with brute force")
    if expected is not None and got != expected:
        print("BAD EXPECTED")
        print("intervals =", intervals)
        print("got       =", got)
        print("expected  =", expected)
        raise AssertionError("Fixed example failed")


def make_random_intervals(n: int, stress: bool) -> List[List[int]]:
    if stress:
        # Tiny coordinate/weight ranges force many ties, touches, and duplicates.
        coord_hi, weight_hi = 6, 4
    else:
        coord_hi, weight_hi = 12, 20

    out = []
    for _ in range(n):
        a = random.randint(1, coord_hi)
        b = random.randint(1, coord_hi)
        l, r = min(a, b), max(a, b)
        w = random.randint(1, weight_hi)
        out.append([l, r, w])
    return out


def main() -> None:
    random.seed(12345)

    # Provided examples.
    check_case(
        [[1, 3, 2], [4, 5, 2], [1, 5, 5], [6, 9, 3], [6, 7, 1], [8, 9, 1]],
        [2, 3],
    )
    check_case(
        [[5, 8, 1], [6, 7, 7], [4, 7, 3], [9, 10, 6], [7, 8, 2], [11, 14, 3], [3, 5, 5]],
        [1, 3, 5, 6],
    )

    # Fixed edge cases.
    check_case([[1, 2, 5]], [0])                       # single interval
    check_case([[1, 2, 5], [2, 3, 100]], [1])          # touching endpoints overlap
    check_case([[1, 2, 5], [3, 4, 5]], [0, 1])         # strict gap allows chaining
    check_case([[1, 10, 5], [2, 3, 2], [4, 5, 3]], [0])# equal weight: (0,) < (1,2)
    check_case([[1, 5, 4], [2, 5, 4], [6, 7, 1]], [0, 2]) # equal right endpoints cannot chain
    check_case([[5, 8, 1], [1, 2, 7], [3, 4, 6], [6, 7, 5]], [1, 2, 3])

    # Random exhaustive verification on tiny inputs.
    trials = 4000
    for t in range(trials):
        n = random.randint(1, 9)
        intervals = make_random_intervals(n, stress=(t % 2 == 0))
        check_case(intervals)
        if (t + 1) % 500 == 0:
            print(f"passed {t + 1}/{trials} random trials")

    print("OK: DP matched brute force on fixed edges and", trials, "random tiny cases")


if __name__ == "__main__":
    main()