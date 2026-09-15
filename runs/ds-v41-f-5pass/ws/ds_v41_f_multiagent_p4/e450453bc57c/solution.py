from typing import List
import random


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        vals = sorted(set(nums))
        m = len(vals)
        rmap = {v: i + 1 for i, v in enumerate(vals)}
        rnums = [rmap[v] for v in nums]

        cnt_tree = [0] * (m + 1)
        sum_tree = [0] * (m + 1)
        top = 1 << (m.bit_length() - 1)
        M = m

        # build initial window [0, x)
        win_sum = 0
        for t in range(x):
            v = nums[t]
            win_sum += v
            i = rnums[t]
            while i <= M:
                cnt_tree[i] += 1
                sum_tree[i] += v
                i += i & (-i)

        nwin = n - x + 1
        costs = [0] * nwin
        kk = (x + 1) // 2  # rank (1-indexed) of the lower median

        for s in range(nwin):
            if s:
                # remove nums[s-1]
                v = nums[s - 1]
                i = rnums[s - 1]
                while i <= M:
                    cnt_tree[i] -= 1
                    sum_tree[i] -= v
                    i += i & (-i)
                win_sum -= v
                # add nums[s+x-1]
                v = nums[s + x - 1]
                win_sum += v
                i = rnums[s + x - 1]
                while i <= M:
                    cnt_tree[i] += 1
                    sum_tree[i] += v
                    i += i & (-i)

            # find the kk-th smallest value; accumulate prefix count & sum
            target = kk
            idx = 0
            bit = top
            sum_less = 0
            while bit:
                nxt = idx + bit
                if nxt <= M and cnt_tree[nxt] < target:
                    idx = nxt
                    target -= cnt_tree[nxt]
                    sum_less += sum_tree[nxt]
                bit >>= 1
            med = vals[idx]           # median value
            cnt_less = kk - target    # number of elements strictly below med
            # cost = sum |a - med|
            costs[s] = win_sum - 2 * sum_less + 2 * med * cnt_less - med * x

        # DP over positions and number of chosen non-overlapping windows
        INF = float('inf')
        dp_prev = [0] * (n + 1)  # j = 0
        for j in range(1, k + 1):
            dp_cur = [INF] * (n + 1)
            for i in range(j * x, n + 1):
                best = dp_cur[i - 1]                      # skip position i-1
                cand = dp_prev[i - x] + costs[i - x]      # window ends at i-1
                if cand < best:
                    best = cand
                dp_cur[i] = best
            dp_prev = dp_cur

        return dp_prev[n]


# ----------------- test harness -----------------
def brute(nums, x, k):
    n = len(nums)

    def wcost(s):
        w = nums[s:s + x]
        med = sorted(w)[(x - 1) // 2]
        return sum(abs(a - med) for a in w)

    best = [float('inf')]

    def rec(start, cnt, acc):
        if acc >= best[0]:
            return
        if cnt == k:
            best[0] = min(best[0], acc)
            return
        remaining = k - cnt
        for s in range(start, n - x + 1):
            if n - s < remaining * x:
                break
            rec(s + x, cnt + 1, acc + wcost(s))

    rec(0, 0, 0)
    return best[0]


if __name__ == "__main__":
    sol = Solution()

    r1 = sol.minOperations([5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2)
    print("Sample 1:", "PASS" if r1 == 8 else "FAIL (got %r, exp 8)" % r1)

    r2 = sol.minOperations([9, -2, -2, -2, 1, 5], 2, 2)
    print("Sample 2:", "PASS" if r2 == 3 else "FAIL (got %r, exp 3)" % r2)

    random.seed(20240607)
    fails = 0
    tested = 0
    for _ in range(20000):
        n = random.randint(2, 9)
        x = random.randint(2, n)
        maxk = n // x
        k = random.randint(1, maxk)
        # bias toward duplicates / negatives
        style = random.random()
        if style < 0.4:
            nums = [random.choice([-3, -3, 0, 0, 4, 4]) for _ in range(n)]
        else:
            nums = [random.randint(-6, 6) for _ in range(n)]
        a = sol.minOperations(nums, x, k)
        b = brute(nums, x, k)
        tested += 1
        if a != b:
            fails += 1
            print("MISMATCH nums=%r x=%d k=%d got=%r exp=%r" % (nums, x, k, a, b))
            if fails > 5:
                break

    # explicit boundary: k*x == n (must tile the whole array)
    for _ in range(3000):
        x = random.randint(2, 4)
        k = random.randint(1, 15)
        n = x * k
        if n < 2:
            continue
        nums = [random.randint(-4, 4) for _ in range(n)]
        a = sol.minOperations(nums, x, k)
        b = brute(nums, x, k)
        tested += 1
        if a != b:
            fails += 1
            print("MISMATCH(full) nums=%r x=%d k=%d got=%r exp=%r" % (nums, x, k, a, b))
            if fails > 5:
                break

    print("Random tests (%d cases):" % tested, "PASS" if fails == 0 else "FAIL (%d)" % fails)