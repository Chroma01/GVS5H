from typing import List
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Sort intervals by right endpoint, keeping original indices.
        order = sorted(range(n), key=lambda i: (intervals[i][1], intervals[i][0], i))
        rights = [intervals[i][1] for i in order]

        # prev[j] = number of intervals (in sorted order, indices < j) whose
        # right endpoint is strictly less than order[j]'s left endpoint.
        # Touching boundaries count as overlapping, so we need r < l (strict).
        prev = [0] * n
        for j in range(n):
            l = intervals[order[j]][0]
            prev[j] = bisect_left(rights, l, 0, j)

        K = 4
        NEG = (-1, None)  # sentinel: weight -1, no path

        def better(a, b):
            # a, b are (weight, tuple_of_original_indices_sorted)
            # Returns the better candidate: higher weight; tie -> lexicographically
            # smaller index tuple (shorter prefix tuple is smaller, matching spec).
            if b[1] is None:
                return a
            if a[1] is None:
                return b
            if a[0] != b[0]:
                return a if a[0] > b[0] else b
            return a if a[1] <= b[1] else b

        # dp[j][k] = best (weight, sorted tuple of original indices) considering
        # the first j sorted intervals, choosing exactly k of them.
        dp = [[NEG] * (K + 1) for _ in range(n + 1)]
        for k in range(K + 1):
            dp[0][k] = (0, ()) if k == 0 else NEG

        for j in range(1, n + 1):
            idx = order[j - 1]
            w = intervals[idx][2]
            pj = prev[j - 1]
            for k in range(K + 1):
                # Option 1: skip interval j-1
                best = dp[j - 1][k]
                # Option 2: take interval j-1
                if k >= 1:
                    pw, pt = dp[pj][k - 1]
                    if pt is not None:
                        cand = (pw + w, tuple(sorted(pt + (idx,))))
                        best = better(best, cand)
                dp[j][k] = best

        # "Up to 4": take the best among all counts. Weights are positive, but
        # ties across cardinalities are resolved by the lexicographic rule.
        ans = dp[n][0]
        for k in range(1, K + 1):
            ans = better(ans, dp[n][k])
        return list(ans[1])


# ------------------------- tests -------------------------
def brute_force(intervals):
    """Exhaustive check: max weight over subsets of size <=4 of non-overlapping
    intervals; tie -> lexicographically smallest sorted index list."""
    from itertools import combinations
    n = len(intervals)
    best_w = -1
    best_list = None
    for k in range(0, min(4, n) + 1):
        for comb in combinations(range(n), k):
            ok = True
            for a in range(k):
                for b in range(a + 1, k):
                    i, j = comb[a], comb[b]
                    l1, r1, _ = intervals[i]
                    l2, r2, _ = intervals[j]
                    # overlap if they share any point (inclusive boundaries)
                    if max(l1, l2) <= min(r1, r2):
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue
            w = sum(intervals[i][2] for i in comb)
            lst = sorted(comb)
            if w > best_w or (w == best_w and (best_list is None or lst < best_list)):
                best_w = w
                best_list = lst
    return best_list if best_list is not None else []


def check(intervals, expected=None, label=""):
    got = Solution().maximumWeight([list(x) for x in intervals])
    bf = brute_force(intervals)
    assert got == bf, f"{label}: mismatch got={got} brute={bf}"
    if expected is not None:
        assert got == expected, f"{label}: got={got} expected={expected}"
    print(f"PASS {label}: {got}")


if __name__ == "__main__":
    # Provided examples
    check([[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]], [2,3], "example1")
    check([[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]],
          [1,3,5,6], "example2")

    # Single interval
    check([[2,5,7]], [0], "single")

    # All mutually overlapping, equal weights -> smallest index alone
    check([[1,10,5],[2,9,5],[3,8,5],[4,7,5]], [0], "all-overlap-equal")

    # Equal total weight, different cardinality:
    # interval 3 alone weight 5 vs intervals 0 (w2) + 4 (w3) -> total 5.
    # Compare (3,) vs (0,4): 0 < 3 -> [0,4].
    check([[1,2,2],[5,6,1],[7,8,1],[1,9,5],[3,4,3]], [0,4], "cross-cardinality-tie")

    # Chain of exactly 4 disjoint intervals, all needed
    check([[1,2,1],[3,4,1],[5,6,1],[7,8,1]], [0,1,2,3], "chain-of-4")

    # Chain of 5 disjoint -> only best 4 by weight, lexicographic tie-break
    check([[1,2,1],[3,4,2],[5,6,3],[7,8,4],[9,10,5]], [1,2,3,4], "chain-of-5")

    # Boundary touching counts as overlapping: [1,3] and [3,5] share point 3
    # so they cannot combine; best single is index 1 (weight 5).
    check([[1,3,4],[3,5,5],[6,7,1]], [1], "boundary-touch")

    # Boundary non-touch: r=3 < l=4 allowed
    check([[1,3,4],[4,5,5]], [0,1], "boundary-strict-ok")

    # Random fuzz against brute force
    import random
    random.seed(12345)
    for t in range(300):
        m = random.randint(1, 9)
        iv = []
        for _ in range(m):
            l = random.randint(1, 12)
            r = random.randint(l, l + random.randint(0, 5))
            w = random.randint(1, 9)
            iv.append([l, r, w])
        check(iv, None, f"fuzz{t}")
    print("ALL TESTS PASSED")