class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        n = len(points)
        
        # Helper function to check if we can select k points with min distance d
        def can_select(d: int) -> bool:
            # If d is 0, always possible
            if d == 0:
                return True
            
            # We'll use backtracking to try to select k points
            # selected: list of indices of selected points
            selected = []
            
            # To optimize, we can sort points? Actually, order doesn't matter for correctness,
            # but for pruning, we can iterate in order.
            # We'll use a recursive backtracking function
            
            # Precompute nothing to save time, just check on the fly
            
            # Backtracking function
            # idx: current index in points we are considering
            # count: number of points selected so far
            def backtrack(idx: int, count: int) -> bool:
                # If we have selected k points, return True
                if count == k:
                    return True
                
                # If not enough points left to fill k slots, return False
                if idx + (n - idx) < k:  # This is always n - idx + count >= k? 
                    # Actually, remaining points = n - idx
                    # We need k - count more points
                    if n - idx < k - count:
                        return False
                
                # Try to pick points from idx to n-1
                for i in range(idx, n):
                    # Check if point i is at least distance d from all selected points
                    valid = True
                    for j in selected:
                        # Manhattan distance
                        dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                        if dist < d:
                            valid = False
                            break
                    
                    if valid:
                        selected.append(i)
                        if backtrack(i + 1, count + 1):
                            return True
                        selected.pop()
                
                return False
            
            return backtrack(0, 0)
        
        # Binary search for the maximum d
        low = 0
        high = 2 * side  # Maximum possible Manhattan distance on the boundary
        
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if can_select(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans