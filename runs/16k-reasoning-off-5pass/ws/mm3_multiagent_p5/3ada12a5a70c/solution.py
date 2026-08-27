from typing import List
import bisect
import sys
sys.setrecursionlimit(10000)

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        n = len(points)
        # Precompute perimeter coordinate s for each point
        s_list = []
        for x, y in points:
            if y == 0:
                s = x
            elif x == side:
                s = side + y
            elif y == side:
                s = 2 * side + (side - x)
            else:
                s = 3 * side + (side - y)
            s_list.append(s)
        
        # Sort points by perimeter coordinate s
        indexed = list(range(n))
        indexed.sort(key=lambda i: s_list[i])
        sorted_points = [points[i] for i in indexed]
        sorted_s = [s_list[i] for i in indexed]
        
        perimeter = 4 * side
        
        # Precompute for binary search bounds
        low, high = 0, 2 * side
        
        # Helper: compute Manhattan distance between two points
        def manhattan(i, j):
            x1, y1 = sorted_points[i]
            x2, y2 = sorted_points[j]
            return abs(x1 - x2) + abs(y1 - y2)
        
        # Feasibility check: can we select k points with pairwise distance >= D?
        def can_form(D):
            # Compute conflict count based on perimeter distance < D for each point
            # This is a lower bound on actual conflicts, used for ordering
            conf_perim = [0] * n
            # For each point, count points with perimeter distance < D
            for i in range(n):
                # Backward arc: s in [s_i - D, s_i)
                left = bisect.bisect_left(sorted_s, sorted_s[i] - D, 0, i)
                back_count = i - left
                # Forward arc: s in (s_i, s_i + D]
                right = bisect.bisect_right(sorted_s, sorted_s[i] + D, i + 1, n)
                forward_count = right - (i + 1)
                conf_perim[i] = back_count + forward_count
            
            # Sort candidates by conf_perim descending (most conflicted first)
            order = sorted(range(n), key=lambda i: -conf_perim[i])
            
            selected = []
            
            def dfs(start, candidates):
                if len(selected) == k:
                    return True
                needed = k - len(selected)
                if len(candidates) - start < needed:
                    return False
                
                for idx in range(start, len(candidates)):
                    i = candidates[idx]
                    # Check if i is compatible with all selected
                    ok = True
                    for j in selected:
                        if manhattan(i, j) < D:
                            ok = False
                            break
                    if not ok:
                        continue
                    # Choose i
                    selected.append(i)
                    if dfs(idx + 1, candidates):
                        return True
                    selected.pop()
                return False
            
            return dfs(0, order)
        
        # Binary search
        while low < high:
            mid = (low + high + 1) // 2
            if can_form(mid):
                low = mid
            else:
                high = mid - 1
        
        return low