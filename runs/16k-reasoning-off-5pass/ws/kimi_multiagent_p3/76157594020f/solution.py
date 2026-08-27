class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        def canAchieve(k: int) -> bool:
            flips_needed = 0
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                run_length = j - i
                flips_needed += run_length // (k + 1)
                if flips_needed > numOps:
                    return False
                i = j
            return flips_needed <= numOps
        
        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if canAchieve(mid):
                right = mid
            else:
                left = mid + 1
        return left