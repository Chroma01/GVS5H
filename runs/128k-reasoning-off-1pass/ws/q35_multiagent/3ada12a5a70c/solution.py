class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        n = len(points)
        
        # Sort points to help with pruning in backtracking
        # Sorting by x then y is a simple heuristic
        points_sorted = sorted(points)
        n_sorted = len(points_sorted)
        
        # Precompute Manhattan distance matrix for sorted points
        dist_sorted = [[0] * n_sorted for _ in range(n_sorted)]
        for i in range(n_sorted):
            for j in range(i + 1, n_sorted):
                d = abs(points_sorted[i][0] - points_sorted[j][0]) + abs(points_sorted[i][1] - points_sorted[j][1])
                dist_sorted[i][j] = d
                dist_sorted[j][i] = d
        
        # Backtracking function to check if we can select k points with min distance >= d
        def can_select(d: int) -> bool:
            # selected: list of indices in points_sorted that are selected
            selected = []
            
            # Recursive function with pruning
            def backtrack(start_idx: int) -> bool:
                if len(selected) == k:
                    return True
                
                # Pruning: if remaining points are not enough
                if n_sorted - start_idx < k - len(selected):
                    return False
                
                # Try to pick the next point from start_idx onwards
                for i in range(start_idx, n_sorted):
                    # Check if point i is at least distance d from all selected points
                    valid = True
                    for s in selected:
                        if dist_sorted[i][s] < d:
                            valid = False
                            break
                    if valid:
                        selected.append(i)
                        if backtrack(i + 1):
                            return True
                        selected.pop()
                
                return False
            
            return backtrack(0)
        
        # Binary search for the maximum minimum distance
        low = 0
        high = 4 * side  # Maximum possible Manhattan distance on boundary
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if can_select(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans