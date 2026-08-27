from typing import List
from collections import defaultdict
import heapq

class SlidingMedian:
    """
    Maintains median of a sliding window of fixed size using two heaps
    (max-heap for lower half, min-heap for upper half) with lazy deletions.
    Allows O(log x) updates and O(1) median queries.
    """
    def __init__(self):
        # max-heap for lower half (store as negative for min-heap behavior)
        self.low = []   # type: List[int]
        # min-heap for upper half
        self.high = []  # type: List[int]
        # lazy deletion counts
        self.delayed = defaultdict(int)
        # current sizes of the two halves
        self.low_size = 0
        self.high_size = 0
        # sum of elements in each half (needed to compute cost efficiently)
        self.low_sum = 0
        self.high_sum = 0

    def _prune(self, heap):
        """Remove the top element if it has been marked for deletion."""
        while heap and self.delayed.get(heap[0], 0) > 0:
            val = heap[0]
            self.delayed[val] -= 1
            if self.delayed[val] == 0:
                del self.delayed[val]
            heapq.heappop(heap)

    def _balance(self):
        """Ensure low and high heaps satisfy size invariant:
           low_size >= high_size and low_size - high_size <= 1."""
        # If low has too many elements (more than high+1)
        if self.low_size > self.high_size + 1:
            # move top of low to high
            # Prune first to ensure top is valid
            self._prune(self.low)
            val = -heapq.heappop(self.low)
            self.low_size -= 1
            self.low_sum -= val
            heapq.heappush(self.high, val)
            self.high_size += 1
            self.high_sum += val
        # If high has more elements (shouldn't happen normally, but handle it)
        elif self.low_size < self.high_size:
            self._prune(self.high)
            val = heapq.heappop(self.high)
            self.high_size -= 1
            self.high_sum -= val
            heapq.heappush(self.low, -val)
            self.low_size += 1
            self.low_sum += val

    def add(self, num: int):
        """Add a new number to the data structure."""
        if not self.low or num <= -self.low[0]:
            heapq.heappush(self.low, -num)
            self.low_size += 1
            self.low_sum += num
        else:
            heapq.heappush(self.high, num)
            self.high_size += 1
            self.high_sum += num
        self._balance()

    def remove(self, num: int):
        """Mark a number for removal (lazy deletion)."""
        self.delayed[num] += 1
        # Determine which half the number belongs to (based on current median)
        # This is an approximation; we'll adjust sizes optimistically and let _balance clean up.
        if self.low and num <= -self.low[0]:
            self.low_size -= 1
            self.low_sum -= num
            if self.low and -self.low[0] == num:
                self._prune(self.low)
        else:
            self.high_size -= 1
            self.high_sum -= num
            if self.high and self.high[0] == num:
                self._prune(self.high)
        self._balance()

    def median(self) -> int:
        """Return the median of the current window. For even size, returns the upper middle."""
        self._prune(self.low)
        self._prune(self.high)
        # Ensure invariant before returning
        if self.low_size > self.high_size + 1:
            self._balance()
        elif self.low_size < self.high_size:
            self._balance()
        return -self.low[0]

    def cost(self) -> int:
        """
        Compute sum of absolute differences from median for the current window.
        cost = median * low_size - low_sum + high_sum - median * high_size
        """
        med = self.median()
        left_cost = med * self.low_size - self.low_sum
        right_cost = self.high_sum - med * self.high_size
        return left_cost + right_cost


def get_costs(nums: List[int], x: int) -> List[int]:
    """
    Precompute cost for every window of size x in nums.
    cost[i] = minimum operations to make nums[i : i+x] all equal.
    """
    n = len(nums)
    sm = SlidingMedian()
    costs = []

    # Build initial window
    for i in range(x):
        sm.add(nums[i])
    costs.append(sm.cost())

    # Slide the window
    for i in range(x, n):
        sm.add(nums[i])
        sm.remove(nums[i - x])
        costs.append(sm.cost())

    return costs


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # 1. Precompute costs for every window
        costs = get_costs(nums, x)

        # 2. DP: dp[j] = min cost to place j non-overlapping windows in current prefix
        # Iterate end positions i from 1 to n
        INF = float('inf')
        # dp[j] for current i; prev_dp[j] for i-1
        # Initialize for i=0 (empty prefix)
        dp = [0] + [INF] * k  # 0 windows cost 0, others INF

        for i in range(1, n + 1):
            new_dp = dp[:]  # copy: case of not placing a window at i
            if i >= x:
                start = i - x
                window_cost = costs[start]
                # Place a window ending at i (start = i-x)
                for j in range(1, k + 1):
                    if dp[j - 1] != INF:
                        # dp[j-1] here corresponds to dp[i-x][j-1]
                        # because new window uses positions [i-x, i-1]
                        if j - 1 == 0:
                            # special case: dp[0] is the same for all i
                            prev = 0
                        else:
                            prev = dp[j - 1]  # this is dp[i-x][j-1] from previous iteration
                        candidate = prev + window_cost
                        if candidate < new_dp[j]:
                            new_dp[j] = candidate
            dp = new_dp

        return dp[k]


# ----------------------------
# Testing code
# ----------------------------
if __name__ == "__main__":
    sol = Solution()

    # Example 1
    nums1 = [5, -2, 1, 3, 7, 3, 6, 4, -1]
    x1, k1 = 3, 2
    print("Example 1:", sol.minOperations(nums1, x1, k1))  # Expected: 8

    # Example 2
    nums2 = [9, -2, -2, -2, 1, 5]
    x2, k2 = 2, 2
    print("Example 2:", sol.minOperations(nums2, x2, k2))  # Expected: 3

    # Additional small brute-force tests
    import random
    import itertools

    def brute_force(nums, x, k):
        """Brute force for very small arrays to verify correctness."""
        n = len(nums)
        best = float('inf')
        # Generate all ways to choose k non-overlapping windows of size x
        # We can think of selecting k start positions s1 < s2 < ... < sk such that s_{i+1} >= s_i + x
        starts = []
        for i in range(n - x + 1):
            starts.append(i)
        # All combinations of k starts
        for combo in itertools.combinations(starts, k):
            valid = True
            for i in range(1, k):
                if combo[i] < combo[i - 1] + x:
                    valid = False
                    break
            if not valid:
                continue
            total_cost = 0
            for s in combo:
                window = nums[s:s + x]
                # minimum cost is sum of abs differences to median
                sorted_w = sorted(window)
                med = sorted_w[x // 2] if x % 2 == 1 else sorted_w[x // 2]
                cost = sum(abs(v - med) for v in window)
                total_cost += cost
            if total_cost < best:
                best = total_cost
        return best if best != float('inf') else 0

    # Test with small random arrays
    random.seed(42)
    for _ in range(100):
        n = random.randint(2, 8)
        nums = [random.randint(-5, 5) for _ in range(n)]
        x = random.randint(2, n)
        max_k = n // x
        k = random.randint(1, max_k)
        expected = brute_force(nums, x, k)
        result = sol.minOperations(nums[:], x, k)
        if expected != result:
            print(f"MISMATCH: nums={nums}, x={x}, k={k}, expected={expected}, got={result}")
            break
    else:
        print("All random brute-force tests passed!")