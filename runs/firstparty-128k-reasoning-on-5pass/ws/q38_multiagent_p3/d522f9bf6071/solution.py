from typing import List
from bisect import bisect_left

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        arr = sorted(((r, l, w, i) for i, (l, r, w) in enumerate(intervals)),
                     key=lambda x: (x[0], x[1], x[3]))
        ends = [x[0] for x in arr]

        W = [[-1] * (n + 1) for _ in range(5)]
        T = [[None] * (n + 1) for _ in range(5)]
        W[0] = [0] * (n + 1)
        T[0] = [()] * (n + 1)

        def insert(t, x):
            for i, v in enumerate(t):
                if x < v:
                    return t[:i] + (x,) + t[i:]
            return t + (x,)

        for j, (r, l, w, idx) in enumerate(arr, 1):
            for k in range(1, 5):
                W[k][j] = W[k][j - 1]
                T[k][j] = T[k][j - 1]

            p = bisect_left(ends, l)
            for k in range(1, 5):
                prev_w = W[k - 1][p]
                if prev_w != -1:
                    tw = prev_w + w
                    tt = insert(T[k - 1][p], idx)
                    cur_w = W[k][j]
                    if tw > cur_w or (tw == cur_w and (T[k][j] is None or tt < T[k][j])):
                        W[k][j] = tw
                        T[k][j] = tt

        best_w = -1
        best_t = None
        for k in range(1, 5):
            w = W[k][n]
            if w == -1:
                continue
            t = T[k][n]
            if w > best_w or (w == best_w and (best_t is None or t < best_t)):
                best_w = w
                best_t = t

        return list(best_t) if best_t is not None else []

if __name__ == "__main__":
    import random
    from itertools import combinations

    def brute(intervals):
        n = len(intervals)
        best_w = -1
        best = None
        for k in range(1, min(4, n) + 1):
            for comb in combinations(range(n), k):
                ok = True
                for a in range(k):
                    for b in range(a + 1, k):
                        i, j = comb[a], comb[b]
                        l1, r1, _ = intervals[i]
                        l2, r2, _ = intervals[j]
                        if not (r1 < l2 or r2 < l1):
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    continue
                w = 0
                for i in comb:
                    w += intervals[i][2]
                lst = list(comb)
                if w > best_w or (w == best_w and (best is None or lst < best)):
                    best_w = w
                    best = lst
        return best if best is not None else []

    sol = Solution()
    cases = [
        ([[1, 3, 2], [4, 5, 2], [1, 5, 5], [6, 9, 3], [6, 7, 1], [8, 9, 1]], [2, 3]),
        ([[5, 8, 1], [6, 7, 7], [4, 7, 3], [9, 10, 6], [7, 8, 2], [11, 14, 3], [3, 5, 5]], [1, 3, 5, 6]),
        ([[1, 1, 7]], [0]),
        ([[1, 5, 1], [2, 6, 2], [3, 7, 3]], [2]),
        ([[1, 2, 1], [2, 3, 1], [3, 4, 1]], [0, 2]),
        ([[1, 5, 1], [2, 5, 1], [6, 7, 1]], [0, 2]),
        ([[1, 10, 5], [2, 3, 2], [4, 5, 3]], [0]),
        ([[1, 2, 5], [3, 4, 5], [1, 20, 10]], [0, 1]),
        ([[1, 2, 1], [3, 4, 1], [5, 6, 1], [7, 8, 1], [9, 10, 1]], [0, 1, 2, 3]),
    ]
    ok = True
    for intervals, expected in cases:
        got = sol.maximumWeight(intervals)
        if got != expected:
            ok = False
            print(f"FAIL: got {got}, expected {expected}")

    rng = random.Random(12345)
    for _ in range(2000):
        n = rng.randint(1, 8)
        style = rng.random()
        if style < 0.1:
            l = rng.randint(1, 5)
            r = rng.randint(l, l + 2)
            intervals = [[l, r, rng.randint(1, 3)]]
        elif style < 0.2:
            c = rng.randint(1, 5)
            intervals = []
            for _ in range(n):
                l = rng.randint(1, c)
                r = rng.randint(c, c + 2)
                intervals.append([l, r, rng.randint(1, 3)])
        elif style < 0.3:
            w = rng.randint(1, 3)
            intervals = []
            for _ in range(n):
                l = rng.randint(1, 6)
                r = rng.randint(l, min(8, l + 2))
                intervals.append([l, r, w])
        else:
            intervals = []
            for _ in range(n):
                l = rng.randint(1, 6)
                r = rng.randint(l, min(8, l + 2))
                intervals.append([l, r, rng.randint(1, 3)])

        got = sol.maximumWeight(intervals)
        exp = brute(intervals)
        if got != exp:
            ok = False
            print(f"FAIL: intervals={intervals} got={got} expected={exp}")
            break

    if ok:
        print("PASS")