from typing import List
import bisect
import random
import time
from itertools import combinations

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []
        # Attach original index before sorting
        indexed = [(l, r, w, i) for i, (l, r, w) in enumerate(intervals)]
        # Sort by start, then by end
        indexed.sort(key=lambda x: (x[0], x[1]))
        
        # Extract arrays for binary search
        starts = [item[0] for item in indexed]
        ends = [item[1] for item in indexed]
        weights = [item[2] for item in indexed]
        orig_idx = [item[3] for item in indexed]
        
        # Precompute nextIdx[i]: smallest j such that start_j > end_i
        next_idx = [0] * n
        for i in range(n):
            # bisect_right finds insertion point for end_i; we need first start > end_i
            j = bisect.bisect_right(starts, ends[i], lo=i+1)
            next_idx[i] = j
        
        # dp[k][i] represents the best (weight, tuple_of_indices) using at most k intervals from i..n-1
        # Initialize with base case: dp[k][n] = (0, ()) for all k
        dp = [[(0, ())] * (n + 1) for _ in range(5)]
        
        # Fill from i = n-1 down to 0
        for i in range(n - 1, -1, -1):
            for k in range(1, 5):
                # Option 1: skip current interval
                best = dp[k][i + 1]
                
                # Option 2: take current interval
                w_take = weights[i]
                nxt = next_idx[i]
                inner = dp[k - 1][nxt]
                total_w = w_take + inner[0]
                # Combine indices: current orig_idx[i] + inner[1]
                combined = list(inner[1])
                combined.append(orig_idx[i])
                combined.sort()
                cand = (total_w, tuple(combined))
                
                # Compare best and cand
                if cand[0] > best[0]:
                    best = cand
                elif cand[0] == best[0]:
                    if cand[1] < best[1]:
                        best = cand
                
                dp[k][i] = best
        
        # Final answer: best among dp[1][0], dp[2][0], dp[3][0], dp[4][0]
        final = dp[1][0]
        for k in range(2, 5):
            cand = dp[k][0]
            if cand[0] > final[0]:
                final = cand
            elif cand[0] == final[0]:
                if cand[1] < final[1]:
                    final = cand
        
        return list(final[1])


def brute_force(intervals: List[List[int]]) -> List[int]:
    """Exhaustive search for up to 4 non-overlapping intervals maximizing weight,
    returning lexicographically smallest index list among optimal solutions."""
    n = len(intervals)
    best_weight = -1
    best_indices = None
    # Try all subsets of size 0..4
    for k in range(0, 5):
        for combo in combinations(range(n), k):
            # Check non-overlap
            # sort by start to easily check
            sorted_combo = sorted(combo, key=lambda idx: intervals[idx][0])
            ok = True
            for i in range(len(sorted_combo) - 1):
                a = intervals[sorted_combo[i]]
                b = intervals[sorted_combo[i+1]]
                # a ends, b starts; need b[0] > a[1] (strict)
                if not (b[0] > a[1]):
                    ok = False
                    break
            if not ok:
                continue
            w = sum(intervals[idx][2] for idx in combo)
            if w > best_weight:
                best_weight = w
                best_indices = list(combo)
            elif w == best_weight:
                # lexicographic comparison on sorted list
                cand_sorted = sorted(combo)
                if cand_sorted < best_indices:
                    best_indices = cand_sorted
    if best_indices is None:
        return []
    return best_indices


def test_small_random():
    sol = Solution()
    for _ in range(500):
        n = random.randint(1, 8)  # small for brute force
        ivs = []
        for _ in range(n):
            l = random.randint(1, 10)
            r = random.randint(l, 10)
            w = random.randint(1, 10)
            ivs.append([l, r, w])
        expected = brute_force(ivs)
        got = sol.maximumWeight(ivs)
        if sorted(got) != sorted(expected):
            print("FAIL small")
            print("intervals:", ivs)
            print("expected:", expected)
            print("got:", got)
            return False
    print("All 500 small random tests passed.")
    return True


def generate_patterns(n):
    """Generate a list of intervals with various overlap patterns for stress testing."""
    patterns = []
    # 1. All overlapping (same range)
    patterns.append([[1, 5, random.randint(1, 100)] for _ in range(n)])
    # 2. All non-overlapping (staggered)
    ivs = []
    for i in range(n):
        l = i * 10 + 1
        r = l + 5
        ivs.append([l, r, random.randint(1, 100)])
    patterns.append(ivs)
    # 3. Random with large n
    ivs = []
    for _ in range(n):
        l = random.randint(1, 10**9)
        r = random.randint(l, l + 1000)
        w = random.randint(1, 10**9)
        ivs.append([l, r, w])
    patterns.append(ivs)
    # 4. Chain where each overlaps next
    ivs = []
    for i in range(n):
        l = i * 5
        r = l + 10
        ivs.append([l, r, random.randint(1, 100)])
    patterns.append(ivs)
    # 5. Every interval touches the next at boundary
    ivs = []
    for i in range(n):
        l = i * 10
        r = l + 9
        ivs.append([l, r, random.randint(1, 100)])
    patterns.append(ivs)
    return patterns


def test_medium_stress():
    sol = Solution()
    n = 200
    patterns = generate_patterns(n)
    for idx, ivs in enumerate(patterns):
        start = time.time()
        res = sol.maximumWeight(ivs)
        elapsed = time.time() - start
        # Just ensure it returns a list and does not crash; brute force is too slow here.
        assert isinstance(res, list), f"Pattern {idx} did not return a list"
        assert all(0 <= x < len(ivs) for x in res), f"Pattern {idx} returned invalid indices"
        assert len(res) <= 4, f"Pattern {idx} returned more than 4 indices"
        print(f"Pattern {idx} (n={n}) solved in {elapsed:.4f}s, returned {sorted(res)}")
    print("All medium stress patterns executed successfully.")


def test_large_performance():
    sol = Solution()
    n = 50000
    # Random large n
    ivs = []
    for _ in range(n):
        l = random.randint(1, 10**9)
        r = random.randint(l, l + 100)
        w = random.randint(1, 10**9)
        ivs.append([l, r, w])
    start = time.time()
    res = sol.maximumWeight(ivs)
    elapsed = time.time() - start
    assert isinstance(res, list)
    assert all(0 <= x < n for x in res)
    assert len(res) <= 4
    print(f"Large n={n} performance test solved in {elapsed:.4f}s, returned {sorted(res)}")
    # Time limit: should be well under a few seconds
    if elapsed > 5.0:
        print("WARNING: performance slower than expected.")
    else:
        print("Performance is acceptable.")


if __name__ == "__main__":
    random.seed(42)  # reproducibility
    test_small_random()
    test_medium_stress()
    test_large_performance()