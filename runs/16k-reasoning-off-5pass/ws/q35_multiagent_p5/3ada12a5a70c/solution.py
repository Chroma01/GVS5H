class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        def manhattan_dist(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
        def get_perimeter_coord(p, side):
            x, y = p
            if y == 0:
                return x
            elif x == side:
                return side + y
            elif y == side:
                return 2 * side + (side - x)
            else:  # x == 0
                return 3 * side + (side - y)
        
        n = len(points)
        # Sort points by perimeter coordinate
        points_with_pc = []
        for i, p in enumerate(points):
            pc = get_perimeter_coord(p, side)
            points_with_pc.append((pc, i))
        points_with_pc.sort()
        sorted_indices = [idx for _, idx in points_with_pc]
        sorted_points = [points[idx] for idx in sorted_indices]
        
        # Binary search on the answer
        low, high = 0, 2 * side
        
        def can_select(mid):
            # Check if we can select k points with pairwise Manhattan distance >= mid
            # Use DFS/backtracking with pruning
            selected = []
            
            def dfs(start_idx, count):
                if count == k:
                    return True
                # Prune: if remaining points are not enough
                if count + (n - start_idx) < k:
                    return False
                
                for i in range(start_idx, n):
                    p = sorted_points[i]
                    # Check distance against all selected points
                    valid = True
                    for sel in selected:
                        if manhattan_dist(p, sel) < mid:
                            valid = False
                            break
                    if valid:
                        selected.append(p)
                        if dfs(i + 1, count + 1):
                            return True
                        selected.pop()
                return False
            
            return dfs(0, 0)
        
        # Binary search
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if can_select(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans