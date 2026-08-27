class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        def check(x):
            total = 0
            for p in points:
                total += (x + p - 1) // p
                if total > m:
                    return False
            return True
            
        low, high = 0, m * max(points)
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans