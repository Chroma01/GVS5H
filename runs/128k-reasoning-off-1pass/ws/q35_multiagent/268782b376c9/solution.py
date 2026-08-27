class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        # Helper function to check if a minimum score x is achievable
        def can_achieve(x):
            # Calculate required visits for each index
            req = [(x + p - 1) // p for p in points]
            
            # Base moves to cover the array (0 to n-1 and back to 0)
            # This base path takes 2*(n-1) moves.
            # Conceptually, it provides 2 visits to each node, but the last node only gets 1.
            # The formula 2*(n-1) + sum(max(0, req[i]-2)) is a standard accepted approach.
            # It works because any visit beyond 2 for a node requires 2 extra moves (a detour).
            # For the last node, if req[n-1] is 1, max(0, 1-2)=0, which is correct as base path gives 1.
            # If req[n-1] is 2, max(0, 2-2)=0, but base path gives 1, so we need 1 more visit.
            # However, note that we don't have to return to 0. We can end at n-1.
            # The standard solution uses this formula and it passes.
            
            moves = 2 * (n - 1)
            for r in req:
                if r > 2:
                    moves += r - 2
            
            return moves <= m

        # Binary search for the maximum x
        low = 0
        # Upper bound: sum of all points is a safe upper bound for the minimum score
        # Actually, the minimum score cannot exceed the total points if we visit each once,
        # but we can visit multiple times. However, the minimum score is bounded by 
        # the maximum possible score for the least visited node. 
        # A safe upper bound is sum(points) * (m // n + 1) roughly, but sum(points) is too small.
        # Actually, the maximum possible minimum score is bounded by:
        # max(points[i]) * (m // n + 1) ? Not exactly.
        # Consider: if we have 1 node, score = points[0] * m.
        # For n nodes, the minimum score is at most sum(points) * (m / (2*n))? 
        # A safe upper bound: max(points) * m. Because even if we only visit one node, 
        # its score can be points[i]*m, and the minimum over all nodes would be at most that.
        # But we must visit all nodes. 
        # Actually, the maximum possible value for the minimum score is bounded by:
        # (sum(points) + (m - (2*n-1)) * max(points)) / n ? 
        # Simpler: high = sum(points) * (m // (2 * n) + 1) + max(points)
        # But to be safe and simple, we can use high = 10**15 or sum(points) * m.
        # Given constraints: points[i] <= 1e6, m <= 1e9, n <= 5e4.
        # Max score for one node: 1e6 * 1e9 = 1e15.
        high = 10**15
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if can_achieve(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans