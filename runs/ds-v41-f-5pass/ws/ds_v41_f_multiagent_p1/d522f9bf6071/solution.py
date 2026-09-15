import random
from itertools import combinations
from bisect import bisect_left
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # sort by (right endpoint, left endpoint, weight, original index)
        items = sorted((r, l, w, i) for i, (l, r, w) in enumerate(intervals))
        rs = [it[0] for it in items]
        # p[k] = number of sorted intervals whose right endpoint < l_k
        # (exactly the intervals compatible with k, strict inequality)
        p = [bisect_left(rs, items[k][1]) for k in range(n)]

        NEG = (-1, ())  # infeasible state
        # dp[j][i] = (best total weight, lexicographically smallest sorted tuple
        #             of original indices) using EXACTLY j intervals among first i
        dp = [[NEG] * (n + 1) for _ in range(5)]
        for i in range(n + 1):
            dp[0][i] = (0, ())

        for i in range(1, n + 1):
            r, l, w, x = items[i - 1]
            pk = p[i - 1]
            for j in range(1, 5):
                best = dp[j][i - 1]              # skip interval i-1
                pw, pt = dp[j - 1][pk]           # take it
                if pw >= 0:
                    nw = pw + w
                    lst = list(pt)
                    lst.insert(bisect_left(lst, x), x)  # keep tuple sorted
                    nt = tuple(lst)
                    if nw > best[0] or (nw == best[0] and nt < best[1]):
                        best = (nw, nt)
                dp[j][i] = best

        best_score = -1
        best_t = ()
        for j in range(5):                       # allow "at most 4"
            w, t = dp[j][n]
            if w > best_score or (w == best_score and t < best_t):
                best_score, best_t = w, t
        return list(best_t)


def brute(intervals):
    """Oracle: enumerate all subsets of <=4 pairwise-disjoint intervals;
    pick max total weight, then lexicographically smallest index list."""
    n = len(intervals)
    best_w = -1
    best_t = ()
    for size in range(5):
        for comb in combinations(range(n), size):
            xs = sorted(comb, key=lambda i: (intervals[i][0], intervals[i][1]))
            ok = True
            for a in range(1, len(xs)):
                if intervals[xs[a - 1]][1] >= intervals[xs[a]][0]:  # strict r < l
                    ok = False
                    break
            if not ok:
                continue
            w = sum(intervals[i][2] for i in comb)
            t = tuple(sorted(comb))            # Python tuple compare == problem lex rule
            if w > best_w or (w == best_w and t < best_t):
                best_w, best_t = w, t
    return list(best_t)


def main():
    sol = Solution()

    # ---- provided samples ----
    assert sol.maximumWeight(
        [[1, 3, 2], [4, 5, 2], [1, 5, 5], [6, 9, 3], [6, 7, 1], [8, 9, 1]]
    ) == [2, 3]
    assert sol.maximumWeight(
        [[5, 8, 1], [6, 7, 7], [4, 7, 3], [9, 10, 6], [7, 8, 2], [11, 14, 3], [3, 5, 5]]
    ) == [1, 3, 5, 6]

    # ---- randomized fuzz vs brute force ----
    random.seed(20240607)
    fails = 0
    trials = 20000
    for _ in range(trials):
        n = random.randint(1, 12)
        maxc = random.choice([2, 3, 4, 5, 8])       # small range -> shared endpoints
        intervals = []
        for _ in range(n):
            l = random.randint(1, maxc)
            r = random.randint(l, maxc)
            w = random.choice([1, 1, 1, 2, 3])      # frequent equal weights
            intervals.append([l, r, w])
        got = sol.maximumWeight(intervals)
        exp = brute(intervals)
        if got != exp:
            fails += 1
            print("MISMATCH", intervals, "got", got, "exp", exp)
            if fails >= 5:
                break

    # ---- targeted edge cases: n<4, all-equal weights, duplicates,
    #      equal-weight-different-cardinality ties ----
    edge_cases = [
        [[1, 1, 5]],                                        # n = 1
        [[1, 2, 1], [3, 4, 1], [5, 6, 1]],                  # n = 3 all equal
        [[1, 2, 1], [3, 4, 1], [5, 6, 1], [7, 8, 1], [9, 10, 1]],   # 5 disjoint
        [[1, 10, 5], [2, 3, 5], [4, 5, 5], [6, 7, 5], [8, 9, 5]],   # heavy vs 4 light tie
        [[1, 2, 3], [1, 2, 3], [1, 2, 3]],                 # duplicates overlap
        [[1, 5, 4], [2, 3, 4], [4, 6, 4]],                 # boundary-sharing overlap
        [[1, 2, 2], [3, 4, 2], [5, 6, 2]],                 # sizes tie, shorter? no, all len 3
    ]
    for iv in edge_cases:
        got = sol.maximumWeight(iv)
        exp = brute(iv)
        if got != exp:
            fails += 1
            print("EDGE MISMATCH", iv, "got", got, "exp", exp)

    print("trials =", trials, "fails =", fails)


main()