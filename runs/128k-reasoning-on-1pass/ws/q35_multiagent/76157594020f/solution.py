class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        blocks = []
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            blocks.append(j - i)
            i = j
            
        def check(k: int) -> bool:
            return sum(b // (k + 1) for b in blocks) <= numOps

        left, right = 1, n
        ans = n
        while left <= right:
            mid = (left + right) // 2
            if check(mid):
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
        return ans