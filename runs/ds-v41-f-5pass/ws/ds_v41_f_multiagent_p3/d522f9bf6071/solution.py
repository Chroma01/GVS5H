from typing import List
import bisect


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        order = sorted(range(n), key=lambda i: (intervals[i][1], intervals[i][0], i))
        rs = [intervals[i][1] for i in order]
        ls = [intervals[i][0] for i in order]
        ws = [intervals[i][2] for i in order]

        NEG = -1
        dp_w = [[NEG] * 5 for _ in range(n + 1)]
        dp_t = [[None] * 5 for _ in range(n + 1)]
        dp_w[0][0] = 0
        dp_t[0][0] = ()

        for i in range(1, n + 1):
            orig = order[i - 1]
            l = ls[i - 1]
            w = ws[i - 1]
            p = bisect.bisect_left(rs, l)

            prev_w = dp_w[i - 1]
            prev_t = dp_t[i - 1]
            cur_w = dp_w[i]
            cur_t = dp_t[i]
            for k in range(5):
                cur_w[k] = prev_w[k]
                cur_t[k] = prev_t[k]

            for k in range(1, 5):
                if dp_w[p][k - 1] >= 0:
                    cw = dp_w[p][k - 1] + w
                    tt = list(dp_t[p][k - 1])
                    bisect.insort(tt, orig)
                    ct = tuple(tt)
                    if cur_w[k] < 0 or cw > cur_w[k] or (cw == cur_w[k] and ct < cur_t[k]):
                        cur_w[k] = cw
                        cur_t[k] = ct

        best_w = -1
        best_t = None
        for k in range(5):
            if dp_w[n][k] >= 0:
                if (best_t is None or dp_w[n][k] > best_w
                        or (dp_w[n][k] == best_w and dp_t[n][k] < best_t)):
                    best_w = dp_w[n][k]
                    best_t = dp_t[n][k]

        return list(best_t)


if __name__ == "__main__":
    import itertools, random, time

    sol = Solution()

    # ---- (a) Provided examples ----
    ex1 = [[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]
    ex2 = [[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]
    r1 = sol.maximumWeight(ex1)
    r2 = sol.maximumWeight(ex2)
    print("Example 1:", r1, "expected [2,3]", "PASS" if r1 == [2,3] else "FAIL")
    print("Example 2:", r2, "expected [1,3,5,6]", "PASS" if r2 == [1,3,5,6] else "FAIL")

    # ---- (b) Brute force over all subsets of size 0..4 ----
    def nonoverlap(sub, intervals):
        # strict: need each pair to satisfy r < l' or r' < l
        pts = sorted((intervals[i][0], intervals[i][1]) for i in sub)
        for (l1, r1_), (l2, r2_) in zip(pts, pts[1:]):
            if not (r1_ < l2):   # sharing/overlap => invalid
                return False
        return True

    def brute(intervals):
        n = len(intervals)
        best_w = -1
        best_t = None
        idxs = range(n)
        for k in range(5):
            for sub in itertools.combinations(idxs, k):
                if not nonoverlap(sub, intervals):
                    continue
                w = sum(intervals[i][2] for i in sub)
                t = tuple(sorted(sub))
                if w > best_w or (w == best_w and (best_t is None or t < best_t)):
                    best_w = w
                    best_t = t
        return list(best_t) if best_t is not None else []

    random.seed(12345)
    mismatches = 0
    trials = 0
    touching = 0
    for _ in range(20000):
        n = random.randint(1, 10)
        intervals = []
        for _ in range(n):
            l = random.randint(1, 8)
            r = random.randint(l, 8)
            w = random.randint(1, 10)
            intervals.append([l, r, w])
        # ensure some touching endpoints exist often
        got = sol.maximumWeight([row[:] for row in intervals])
        exp = brute(intervals)
        trials += 1
        if got != exp:
            mismatches += 1
            if mismatches <= 5:
                print("MISMATCH input:", intervals, "got:", got, "exp:", exp)
        # track that touching-endpoint cases were exercised in brute validation
        if any(intervals[i][1] == intervals[j][0] for i in range(n) for j in range(n) if i != j):
            touching += 1

    print(f"Brute-force random trials: {trials}, mismatches: {mismatches}")
    print(f"Trials containing touching endpoints: {touching}")

    # ---- (c) Timing at n = 5*10^4 ----
    n = 50000
    random.seed(7)
    big = []
    for _ in range(n):
        l = random.randint(1, 10**9)
        r = random.randint(l, 10**9)
        w = random.randint(1, 10**9)
        big.append([l, r, w])
    t0 = time.time()
    res = sol.maximumWeight(big)
    t1 = time.time()
    print(f"n={n} runtime: {t1 - t0:.3f}s, result len={len(res)}")