class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Precompute Manhattan distances between all pairs? No, too expensive for n=15000.
        # Instead, in the feasibility check, we'll compute on the fly.
        
        # We'll use binary search on the answer (min_dist)
        # The range of possible min_dist is [0, 2*side]
        
        n = len(points)
        
        # Helper function to check if we can select k points with min Manhattan distance >= min_dist
        def can_select(min_dist: int) -> bool:
            # We need to select k points from points such that every pair has Manhattan distance >= min_dist.
            # Since k is small (<=25), we can use backtracking with pruning.
            # To optimize, we sort points by a heuristic (e.g., x+y or perimeter coordinate) to help pruning.
            # But actually, for Manhattan distance, sorting by x+y might not be perfect.
            # However, a common trick is to sort by one coordinate. Let's sort by x then y.
            
            # Create a list of indices sorted by x, then y
            indices = list(range(n))
            indices.sort(key=lambda i: (points[i][0], points[i][1]))
            
            # Precompute the points for easier access
            pts = [points[i] for i in indices]
            
            # Backtracking function
            # We'll try to select points one by one.
            # state: current count of selected points, last selected point index in sorted list, and the list of selected points' indices (to check against all previously selected)
            # But checking against all previously selected is O(k) per candidate, and k is small, so it's acceptable.
            
            # To prune: we can keep track of the minimum distance from the last selected point to any candidate. But actually, we need to check against ALL selected points.
            
            # We'll use a recursive backtracking with memoization? Not really, because the state is the set of selected points, which is too large.
            # Instead, we rely on pruning: if the remaining points are not enough to complete k, return False.
            
            # Let's implement backtracking without memoization, but with pruning.
            
            selected = []  # list of indices in the sorted list (pts) that are selected
            
            def backtrack(start_idx: int, count: int) -> bool:
                # If we have selected k points, return True
                if count == k:
                    return True
                # If not enough points left to complete k, return False
                if n - start_idx < k - count:
                    return False
                
                # Try to select a point from start_idx onwards
                for i in range(start_idx, n):
                    # Check if pts[i] is at least min_dist away from all selected points
                    valid = True
                    for j in range(len(selected)):
                        # Compute Manhattan distance between pts[i] and pts[selected[j]]
                        x1, y1 = pts[i]
                        x2, y2 = pts[selected[j]]
                        dist = abs(x1 - x2) + abs(y1 - y2)
                        if dist < min_dist:
                            valid = False
                            break
                    if valid:
                        selected.append(i)
                        # Recurse: next candidate must be after i
                        if backtrack(i + 1, count + 1):
                            return True
                        selected.pop()
                return False
            
            return backtrack(0, 0)
        
        # Binary search for the maximum min_dist
        low, high = 0, 2 * side
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if can_select(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans