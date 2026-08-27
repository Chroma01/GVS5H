from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        def check(x: int) -> bool:
            moves = 0
            # visits represents the number of times the current index i has been 
            # visited due to bounces from the previous index i-1.
            visits = 0 
            
            for i in range(n):
                # If we are at the last index and it's already satisfied by 
                # bounces from n-2, we don't need to move further.
                if i == n - 1 and visits * points[i] >= x:
                    break
                
                # Move from i-1 to i (or from -1 to 0)
                moves += 1
                visits += 1
                
                # Calculate required visits for index i to reach target x
                needed = (x + points[i] - 1) // points[i]
                
                if visits < needed:
                    extra = needed - visits
                    # We bounce between i and i+1 (or i-1 if i is the last index).
                    # Each bounce (i -> i+1 -> i) costs 2 moves and adds 1 visit to i.
                    moves += 2 * extra
                    # These bounces also visit i+1 'extra' times, which carries over.
                    visits = extra 
                else:
                    # No bounces needed, next index starts with 0 carried visits.
                    visits = 0
                
                if moves > m:
                    return False
            
            return True

        # Binary search on the answer
        # Upper bound: a safe estimate is bouncing at the first index.
        low = 0
        high = (m // 2 + 1) * points[0] 
        # A safer global upper bound:
        high = max(high, (m // n + 1) * max(points))
        
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans