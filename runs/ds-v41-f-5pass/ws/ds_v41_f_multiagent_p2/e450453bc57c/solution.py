from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # Coordinate compression: value -> rank 1..V
        vals = sorted(set(nums))
        V = len(vals)
        rank = {v: i + 1 for i, v in enumerate(vals)}
        comp = [rank[v] for v in nums]

        # Fenwick trees over counts and sums (1-indexed by rank)
        cnt = [0] * (V + 1)
        sm = [0] * (V + 1)

        topbit = 1 << V.bit_length()
        m = (x + 1) >> 1          # target for lower median
        W = n - x + 1             # number of window starts

        # Initialize first window [0, x)
        total = 0
        for i in range(x):
            v = nums[i]
            total += v
            j = comp[i]
            while j <= V:
                cnt[j] += 1
                sm[j] += v
                j += j & (-j)

        costs = [0] * W
        for p in range(W):
            if p:
                # remove nums[p-1]
                v = nums[p - 1]
                j = comp[p - 1]
                while j <= V:
                    cnt[j] -= 1
                    sm[j] -= v
                    j += j & (-j)
                # add nums[p-1+x]
                v2 = nums[p - 1 + x]
                j = comp[p - 1 + x]
                while j <= V:
                    cnt[j] += 1
                    sm[j] += v2
                    j += j & (-j)
                total += v2 - v

            # find rank of the lower median via binary lifting
            kk = m
            idx = 0
            b = topbit
            while b:
                nxt = idx + b
                if nxt <= V and cnt[nxt] < kk:
                    idx = nxt
                    kk -= cnt[nxt]
                b >>= 1
            med_idx = idx + 1
            med = vals[med_idx - 1]

            # prefix count / sum up to and including median rank
            j = med_idx
            cle = 0
            sle = 0
            while j > 0:
                cle += cnt[j]
                sle += sm[j]
                j -= j & (-j)

            cgt = x - cle
            sgt = total - sle
            costs[p] = med * cle - sle + sgt - med * cgt

        # DP over window-start positions
        INF = 1 << 60
        prev = [0] * (W + 1)          # dp_0[idx] = 0
        for _ in range(k):
            cur = [INF] * (W + 1)     # dp_j[0] = INF for j >= 1
            for idx in range(1, W + 1):
                best = cur[idx - 1]
                pidx = idx - x
                if pidx < 0:
                    pidx = 0
                t = prev[pidx] + costs[idx - 1]
                if t < best:
                    best = t
                cur[idx] = best
            prev = cur

        return prev[W]


if __name__ == "__main__":
    import random
    from itertools import combinations

    sol = Solution()

    def brute(nums, x, k):
        n = len(nums)
        W = n - x + 1
        costs = []
        for s in range(W):
            w = sorted(nums[s:s + x])
            med = w[(x - 1) // 2]
            costs.append(sum(abs(v - med) for v in w))
        best = float("inf")
        for combo in combinations(range(W), k):
            if all(b >= a + x for a, b in zip(combo, combo[1:])):
                best = min(best, sum(costs[i] for i in combo))
        return best

    # Provided samples
    assert sol.minOperations([5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2) == 8
    assert sol.minOperations([9, -2, -2, -2, 1, 5], 2, 2) == 3

    # Edge cases
    assert sol.minOperations([1, 10], 2, 1) == 9            # x == len(nums), k = 1
    assert sol.minOperations([5, 5, 5, 5], 2, 2) == 0       # all equal
    assert sol.minOperations([1, 2, 3, 4, 5, 6], 3, 2) == 4  # k*x == n
    assert sol.minOperations([1, 2, 3, 4], 2, 1) == 1        # k = 1, min window

    # Random brute-force cross-check
    random.seed(12345)
    for _ in range(3000):
        n = random.randint(2, 9)
        x = random.randint(2, n)
        maxk = n // x
        if maxk < 1:
            continue
        k = random.randint(1, maxk)
        nums = [random.randint(-6, 6) for _ in range(n)]
        exp = brute(nums, x, k)
        got = sol.minOperations(nums, x, k)
        if exp != got:
            print("MISMATCH", nums, x, k, "expected", exp, "got", got)
            raise SystemExit(1)

    print("ALL PASS")