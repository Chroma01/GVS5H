from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        def can(target: int) -> bool:
            # need[i] = minimum visits to position i to reach target score
            need = [(target + points[i] - 1) // points[i] for i in range(n)]
            
            # Greedy simulation: walk from index -1 through the array
            # cur = number of additional visits still needed at current position
            cur = 0
            total = 0
            
            for i in range(n):
                # Step into position i (1 move)
                total += 1
                
                # If we have a carried deficit from the previous position's round trip,
                # this visit satisfies one of those required returns
                if cur > 0:
                    cur -= 1
                else:
                    # No carried deficit; this visit counts toward need[i],
                    # so we still need (need[i] - 1) more visits at position i
                    cur = need[i] - 1
                
                # Handle the remaining deficit at position i
                if i < n - 1:
                    # Non-last position: round trips (go to i+1, come back)
                    # Each round trip costs 2 moves, but the first "go to i+1" 
                    # is the forward step we'll take anyway, so extra cost is 2*cur - 1
                    if cur > 0:
                        total += 2 * cur - 1
                        cur = 0
                else:
                    # Last position: each additional visit costs 2 moves 
                    # (go to n-2, back to n-1), and we end at n-1
                    if cur > 0:
                        total += 2 * cur
                        cur = 0
            
            return total <= m
        
        # Binary search on the answer
        # Upper bound: if we spent all moves on the max point, score could be up to max(points) * m
        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo