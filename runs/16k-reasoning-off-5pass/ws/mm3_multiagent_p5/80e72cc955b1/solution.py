import bisect
from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4 up to > 1e9
        powers = []
        p = 1
        while p <= 10**9:
            powers.append(p)
            p *= 4
        # powers[k] = 4^k, k from 0 to len(powers)-1
        # Depth d(x) for x >= 1: smallest k such that 4^k > x, equivalently d(x) = floor(log4(x)) + 1
        # Block [4^k, 4^{k+1}-1] has depth k+1, size 3*4^k
        
        # Precompute prefix sums over full blocks:
        # full_sum[k] = sum_{i=0}^{k-1} (i+1) * 3 * 4^i, for k >= 0
        # full_sum[0] = 0
        n_levels = len(powers)  # number of powers, e.g., 16 (4^0 to 4^15)
        full_sum = [0] * (n_levels + 1)
        for k in range(n_levels):
            full_sum[k+1] = full_sum[k] + (k+1) * 3 * powers[k]
        
        def S(n):
            # Returns sum of depths d(x) for x in [1, n]. S(0) = 0.
            if n <= 0:
                return 0
            # Find largest K such that 4^K <= n
            # powers[K] <= n < powers[K+1]
            K = bisect.bisect_right(powers, n) - 1
            # Full blocks: depths 1..K, sum is full_sum[K]
            result = full_sum[K]
            # Partial block: [4^K, n], depth K+1
            result += (K + 1) * (n - powers[K] + 1)
            return result
        
        total = 0
        for l, r in queries:
            depth_sum = S(r) - S(l - 1)
            total += (depth_sum + 1) // 2
        return total


# ---- Brute-force validation for small ranges ----
import math

def brute_min_ops(l, r):
    """BFS/DP to find minimum operations for small arrays."""
    from collections import deque
    # state: sorted tuple of remaining values
    # But BFS state space is huge. Use optimal formula directly: ceil(sum(depth)/2)
    # For brute-force, simulate greedy pairing or BFS for very small arrays.
    # Since arr is [l, l+1, ..., r], we can just verify the formula.
    # For tiny ranges, we can BFS:
    if l > r:
        return 0
    arr = tuple(range(l, r+1))
    if all(x == 0 for x in arr):
        return 0
    # BFS
    visited = {arr: 0}
    queue = deque([arr])
    while queue:
        state = queue.popleft()
        d = visited[state]
        if all(x == 0 for x in state):
            return d
        n = len(state)
        for i in range(n):
            for j in range(i+1, n):
                a, b = state[i], state[j]
                if a == 0 and b == 0:
                    continue
                na = a // 4
                nb = b // 4
                new_state = list(state)
                new_state[i] = na
                new_state[j] = nb
                new_state = tuple(sorted(new_state))
                if new_state not in visited:
                    visited[new_state] = d + 1
                    if all(x == 0 for x in new_state):
                        return d + 1
                    queue.append(new_state)
    return -1

def depth_sum_brute(l, r):
    return sum(math.floor(math.log(x, 4)) + 1 for x in range(l, r+1))

def formula_min_ops(l, r):
    ds = depth_sum_brute(l, r)
    return (ds + 1) // 2

# Verify against provided examples
sol = Solution()
print("Example 1:", sol.minOperations([[1,2],[2,4]]))  # Expected: 3
print("Example 2:", sol.minOperations([[2,6]]))        # Expected: 4

# Brute-force validation for small ranges
max_val = 20
mismatches = 0
for l in range(1, max_val+1):
    for r in range(l, max_val+1):
        bf = brute_min_ops(l, r)
        fm = formula_min_ops(l, r)
        if bf != fm:
            print(f"MISMATCH l={l} r={r}: brute={bf} formula={fm}")
            mismatches += 1
print(f"Brute-force validation complete. Mismatches: {mismatches}")