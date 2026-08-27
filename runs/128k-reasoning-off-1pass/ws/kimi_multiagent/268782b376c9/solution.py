from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        def check(x: int) -> bool:
            if x == 0:
                return True
            req = [(x + p - 1) // p for p in points]
            moves = 0
            visits = [0] * n
            curr = -1
            
            for i in range(n):
                if visits[i] >= req[i]:
                    continue
                
                # Move to index i
                while curr < i:
                    curr += 1
                    moves += 1
                    visits[curr] += 1
                    if moves > m:
                        return False
                
                # Bounce to satisfy req[i]
                if visits[i] < req[i]:
                    k = req[i] - visits[i]
                    moves += 2 * k
                    visits[i] += k
                    if i < n - 1:
                        visits[i+1] += k
                    else:
                        visits[i-1] += k
                    if moves > m:
                        return False
            
            return moves <= m

        low, high = 0, 10**18
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans