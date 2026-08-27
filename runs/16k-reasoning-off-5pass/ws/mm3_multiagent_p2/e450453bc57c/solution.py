from typing import List
import heapq
from collections import defaultdict

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        INF = float('inf')
        # cost[i] = min ops to equalize window ending at i (0-indexed),
        # i.e., subarray nums[i-x+1 .. i]. For i < x-1, INF.
        cost = [INF] * n
        
        # Two-heap sliding median with lazy deletion
        # low: max-heap (store as negatives) for elements <= median
        # high: min-heap for elements > median
        # Invariant: len(low) == len(high) or len(low) == len(high) + 1
        low = []   # max-heap (negated values)
        high = []  # min-heap
        sum_low = 0
        sum_high = 0
        delayed = defaultdict(int)  # lazy deletion counts
        
        def prune(heap):
            while heap:
                if heap is low:
                    num = -heap[0]
                else:
                    num = heap[0]
                if delayed[num] > 0:
                    delayed[num] -= 1
                    if delayed[num] == 0:
                        del delayed[num]
                    heapq.heappop(heap)
                else:
                    break
        
        def rebalance():
            nonlocal sum_low, sum_high
            # Ensure len(low) == len(high) or len(low) == len(high) + 1
            if len(low) > len(high) + 1:
                num = -heapq.heappop(low)
                sum_low -= num
                sum_high += num
                heapq.heappush(high, num)
            elif len(low) < len(high):
                num = heapq.heappop(high)
                sum_high -= num
                sum_low += num
                heapq.heappush(low, -num)
        
        def add(num):
            nonlocal sum_low, sum_high
            if not low or num <= -low[0]:
                heapq.heappush(low, -num)
                sum_low += num
            else:
                heapq.heappush(high, num)
                sum_high += num
        
        def remove(num):
            nonlocal sum_low, sum_high
            delayed[num] += 1
            if low and num <= -low[0]:
                sum_low -= num
            else:
                sum_high -= num
        
        def get_cost():
            median = -low[0]
            lc = len(low)
            hc = len(high)
            return (median * lc - sum_low) + (sum_high - median * hc)
        
        # Build first window [0 .. x-1]
        for i in range(x):
            add(nums[i])
        rebalance()
        prune(low)
        prune(high)
        cost[x - 1] = get_cost()
        
        # Slide window
        for i in range(x, n):
            add(nums[i])
            remove(nums[i - x])
            prune(low)
            prune(high)
            rebalance()
            prune(low)
            prune(high)
            cost[i] = get_cost()
        
        # DP: dp[c][i] = min cost to select c non-overlapping windows
        # among windows ending at positions <= i.
        dp = [[INF] * n for _ in range(k + 1)]
        for i in range(n):
            dp[0][i] = 0
        
        for c in range(1, k + 1):
            for i in range(n):
                if i > 0:
                    dp[c][i] = dp[c][i - 1]
                if i >= x - 1 and cost[i] != INF:
                    if i - x >= 0:
                        cand = dp[c - 1][i - x] + cost[i]
                    else:
                        cand = cost[i]
                    if cand < dp[c][i]:
                        dp[c][i] = cand
        
        return dp[k][n - 1]


# ---------------- TESTING ----------------
def brute_force(nums, x, k):
    """Brute force: try all ways to pick k non-overlapping windows of length x."""
    from itertools import combinations
    n = len(nums)
    windows = [(i, i + x - 1) for i in range(n - x + 1)]
    
    def window_cost(l, r):
        sub = nums[l:r + 1]
        srt = sorted(sub)
        m = srt[len(srt) // 2]
        return sum(abs(v - m) for v in sub)
    
    best = float('inf')
    # Try all combinations of k windows
    for combo in combinations(windows, k):
        # Check non-overlapping
        combo_sorted = sorted(combo)
        ok = True
        for j in range(len(combo_sorted) - 1):
            if combo_sorted[j][1] >= combo_sorted[j + 1][0]:
                ok = False
                break
        if not ok:
            continue
        total = sum(window_cost(l, r) for l, r in combo)
        if total < best:
            best = total
    return best


if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    nums1 = [5, -2, 1, 3, 7, 3, 6, 4, -1]
    x1, k1 = 3, 2
    result1 = sol.minOperations(nums1, x1, k1)
    print(f"Example 1: {result1} (expected 8) - {'PASS' if result1 == 8 else 'FAIL'}")
    
    # Example 2
    nums2 = [9, -2, -2, -2, 1, 5]
    x2, k2 = 2, 2
    result2 = sol.minOperations(nums2, x2, k2)
    print(f"Example 2: {result2} (expected 3) - {'PASS' if result2 == 3 else 'FAIL'}")
    
    # Brute force verification on small random cases
    import random
    random.seed(42)
    all_pass = True
    for trial in range(200):
        n = random.randint(2, 10)
        x = random.randint(2, n)
        k = random.randint(1, min(5, n // x))
        if k * x > n:
            continue
        nums = [random.randint(-5, 5) for _ in range(n)]
        sol_result = sol.minOperations(nums, x, k)
        bf_result = brute_force(nums, x, k)
        if sol_result != bf_result:
            print(f"FAIL on trial {trial}: nums={nums}, x={x}, k={k}")
            print(f"  Solution returned: {sol_result}, Brute force: {bf_result}")
            all_pass = False
    if all_pass:
        print("All 200 random brute-force tests PASSED!")