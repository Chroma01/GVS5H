import heapq
import random
import time
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1
        
        # Compute cost for each window of length x using two heaps with lazy deletion
        cost = [0] * m
        low = []  # max-heap (store negatives)
        high = []  # min-heap
        low_sum = 0
        total_sum = 0
        delayed = {}
        target_low = (x + 1) // 2
        
        def prune(heap, sign):
            nonlocal low_sum
            while heap:
                val = sign * heap[0]
                if val in delayed and delayed[val] > 0:
                    popped = heapq.heappop(heap)
                    actual_val = sign * popped
                    delayed[actual_val] -= 1
                    if delayed[actual_val] == 0:
                        del delayed[actual_val]
                    if sign == -1:
                        low_sum -= actual_val
                else:
                    break
        
        def balance():
            nonlocal low_sum
            # Prune tops
            prune(low, -1)
            prune(high, 1)
            # Move elements to maintain target_low size
            while len(low) > target_low:
                prune(low, -1)
                val = -heapq.heappop(low)
                low_sum -= val
                heapq.heappush(high, val)
            while len(low) < target_low:
                prune(high, 1)
                val = heapq.heappop(high)
                heapq.heappush(low, -val)
                low_sum += val
            # Ensure median is clean
            prune(low, -1)
        
        def add(num):
            nonlocal low_sum, total_sum
            if not low or num <= -low[0]:
                heapq.heappush(low, -num)
                low_sum += num
            else:
                heapq.heappush(high, num)
            total_sum += num
            balance()
        
        def remove(num):
            nonlocal total_sum
            delayed[num] = delayed.get(num, 0) + 1
            total_sum -= num
            # Try to prune if this element is at the top
            if low and -low[0] == num:
                prune(low, -1)
            if high and high[0] == num:
                prune(high, 1)
            balance()
        
        def get_cost():
            # median is top of low (already pruned)
            median = -low[0]
            len_low = target_low
            len_high = x - len_low
            return median * len_low - low_sum + (total_sum - low_sum) - median * len_high
        
        # Initialize with first window
        for i in range(x):
            add(nums[i])
        cost[0] = get_cost()
        
        # Slide the window
        for i in range(1, m):
            remove(nums[i - 1])
            add(nums[i + x - 1])
            cost[i] = get_cost()
        
        # DP: dp[t][i] = min cost to select t windows in prefix of length i
        INF = 10**18
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        for i in range(n + 1):
            dp[0][i] = 0
        
        for t in range(1, k + 1):
            for i in range(x, n + 1):
                # Option 1: don't take a window ending at i-1
                val1 = dp[t][i - 1]
                # Option 2: take a window ending at i-1 (starts at i-x)
                val2 = dp[t - 1][i - x] + cost[i - x]
                dp[t][i] = min(val1, val2)
        
        return dp[k][n]


def stress_test():
    """Stress test with large random cases to verify performance and correctness."""
    sol = Solution()
    random.seed(123)
    
    # Test with increasing sizes to check performance
    sizes = [1000, 5000, 10000, 50000, 100000]
    for n in sizes:
        x = random.randint(2, min(20, n // 2))
        k = random.randint(1, min(15, n // x))
        nums = [random.randint(-10**6, 10**6) for _ in range(n)]
        
        start = time.time()
        result = sol.minOperations(nums, x, k)
        elapsed = time.time() - start
        
        print(f"n={n:6d}, x={x:3d}, k={k:2d}: result={result:12d}, time={elapsed:.3f}s")
        
        # Basic sanity checks
        assert result >= 0, "Cost should be non-negative"
        assert result < 10**18, "Should have found a valid solution"
    
    # Edge case: k*x == n (no room to spare)
    print("\n--- Edge case: k*x == n (tight packing) ---")
    for trial in range(5):
        n = random.randint(20, 200)
        x = random.randint(2, 10)
        k = n // x
        if k < 1 or k > 15:
            continue
        nums = [random.randint(-100, 100) for _ in range(n)]
        start = time.time()
        result = sol.minOperations(nums, x, k)
        elapsed = time.time() - start
        print(f"  n={n}, x={x}, k={k}: result={result}, time={elapsed:.4f}s")
    
    # Edge case: x divides n, various k
    print("\n--- Edge case: x divides n ---")
    for trial in range(5):
        x = random.randint(2, 8)
        num_windows = random.randint(3, 15)
        n = x * num_windows
        k = random.randint(1, num_windows)
        nums = [random.randint(-50, 50) for _ in range(n)]
        start = time.time()
        result = sol.minOperations(nums, x, k)
        elapsed = time.time() - start
        print(f"  n={n}, x={x}, k={k}: result={result}, time={elapsed:.4f}s")
    
    # Edge case: k = 1 (simplest DP)
    print("\n--- Edge case: k=1 ---")
    for n in [100, 1000, 10000]:
        x = random.randint(2, min(50, n))
        k = 1
        nums = [random.randint(-10**6, 10**6) for _ in range(n)]
        start = time.time()
        result = sol.minOperations(nums, x, k)
        elapsed = time.time() - start
        # Brute force for verification on smaller case
        if n <= 50:
            # Verify by checking all windows
            min_c = min(sum(abs(v - sorted(nums[i:i+x])[x//2]) for v in nums[i:i+x]) for i in range(n - x + 1))
            assert result == min_c, f"k=1 mismatch: {result} vs {min_c}"
            print(f"  n={n}, x={x}, k=1: result={result} (verified), time={elapsed:.4f}s")
        else:
            print(f"  n={n}, x={x}, k=1: result={result}, time={elapsed:.4f}s")
    
    # Edge case: all same values (cost should be 0)
    print("\n--- Edge case: all same values ---")
    for n in [100, 10000, 100000]:
        x = random.randint(2, 10)
        k = random.randint(1, min(15, n // x))
        val = random.randint(-1000, 1000)
        nums = [val] * n
        start = time.time()
        result = sol.minOperations(nums, x, k)
        elapsed = time.time() - start
        assert result == 0, f"Expected 0 for all-same, got {result}"
        print(f"  n={n}, x={x}, k={k}: result=0 (correct), time={elapsed:.4f}s")
    
    # Edge case: strictly increasing
    print("\n--- Edge case: strictly increasing sequence ---")
    for n in [100, 10000]:
        x = random.randint(2, 10)
        k = random.randint(1, min(10, n // x))
        nums = list(range(n))
        start = time.time()
        result = sol.minOperations(nums, x, k)
        elapsed = time.time() - start
        print(f"  n={n}, x={x}, k={k}: result={result}, time={elapsed:.4f}s")
    
    # Edge case: strictly decreasing
    print("\n--- Edge case: strictly decreasing sequence ---")
    for n in [100, 10000]:
        x = random.randint(2, 10)
        k = random.randint(1, min(10, n // x))
        nums = list(range(n, 0, -1))
        start = time.time()
        result = sol.minOperations(nums, x, k)
        elapsed = time.time() - start
        print(f"  n={n}, x={x}, k={k}: result={result}, time={elapsed:.4f}s")
    
    # Worst case: large values
    print("\n--- Edge case: large values ---")
    n = 100000
    x = 10
    k = 15
    nums = [random.randint(-10**6, 10**6) for _ in range(n)]
    start = time.time()
    result = sol.minOperations(nums, x, k)
    elapsed = time.time() - start
    print(f"  n={n}, x={x}, k={k}: result={result}, time={elapsed:.3f}s")
    
    # Verify DP correctness on small cases against brute force
    print("\n--- DP verification on small cases (n<=15) ---")
    passed = 0
    total = 100
    for _ in range(total):
        n = random.randint(5, 15)
        x = random.randint(2, min(5, n // 2))
        k = random.randint(1, min(4, n // x))
        nums = [random.randint(-10, 10) for _ in range(n)]
        
        m = n - x + 1
        wc = []
        for i in range(m):
            w = nums[i:i+x]
            s = sorted(w)
            med = s[x // 2]
            wc.append(sum(abs(v - med) for v in w))
        
        # Brute force: try all combinations of k non-overlapping windows
        best = float('inf')
        def recurse(start, remaining, current):
            nonlocal best
            if remaining == 0:
                best = min(best, current)
                return
            for i in range(start, m - (remaining - 1) * x):
                if current + wc[i] >= best:
                    continue
                recurse(i + x, remaining - 1, current + wc[i])
        
        recurse(0, k, 0)
        expected = best
        
        actual = sol.minOperations(nums, x, k)
        if actual == expected:
            passed += 1
        else:
            print(f"  FAIL: nums={nums}, x={x}, k={k}, expected={expected}, actual={actual}")
    
    print(f"  DP verification: {passed}/{total} passed")
    assert passed == total, "DP verification failed!"
    
    print("\n=== All stress tests passed! ===")


if __name__ == "__main__":
    stress_test()