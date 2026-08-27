class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        # Check function for binary search
        def check(x):
            if x == 0:
                return True
            
            # Calculate required visits for each index
            req = []
            total_visits = 0
            for p in points:
                # ceil(x / p)
                visits = (x + p - 1) // p
                req.append(visits)
                total_visits += visits
            
            # If total visits exceed m, it's impossible (since each visit takes at least 1 move, and path constraints add more)
            if total_visits > m:
                return False
            
            # Find the leftmost and rightmost indices that need visits
            L = 0
            while L < n and req[L] == 0:
                L += 1
            
            R = n - 1
            while R >= 0 and req[R] == 0:
                R -= 1
            
            # If no index needs visits, x=0 which is already handled
            if L > R:
                return True
            
            # Minimal moves = total_visits + min(L, n - 1 - R)
            moves = total_visits + min(L, n - 1 - R)
            
            return moves <= m
        
        # Binary search for the maximum x
        low, high = 0, 10**15
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans