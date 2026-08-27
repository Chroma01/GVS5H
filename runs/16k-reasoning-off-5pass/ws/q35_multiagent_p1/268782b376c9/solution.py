class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        # Helper function to check if a minimum score 'mid' is achievable
        def is_feasible(mid: int) -> bool:
            if mid == 0:
                return True
            
            total_visits = 0
            for p in points:
                # visits needed for this index = ceil(mid / p)
                # Using integer arithmetic: (mid + p - 1) // p
                visits = (mid + p - 1) // p
                total_visits += visits
                # Early exit if already exceeds m
                if total_visits > m:
                    return False
            return total_visits <= m

        # Binary search for the maximum feasible mid
        low = 0
        # Upper bound: m * max(points) is a safe upper bound.
        # Since m <= 10^9 and points[i] <= 10^6, max possible score is 10^15.
        high = m * max(points)
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if is_feasible(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans