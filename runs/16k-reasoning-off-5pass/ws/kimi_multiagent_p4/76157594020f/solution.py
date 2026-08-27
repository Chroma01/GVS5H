class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def min_flips(L: int) -> int:
            if L == 1:
                # Final string must be alternating; try both patterns.
                # Pattern starting with '0': position i should be '0' if i even else '1'.
                mismatches0 = 0
                for i, ch in enumerate(s):
                    expected = '0' if i % 2 == 0 else '1'
                    if ch != expected:
                        mismatches0 += 1
                # The other pattern needs exactly n - mismatches0 flips.
                return min(mismatches0, n - mismatches0)
            # L >= 2: each maximal run of length `run` needs run // (L + 1) flips.
            flips = 0
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                run = j - i
                flips += run // (L + 1)
                i = j
            return flips

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if min_flips(mid) <= numOps:
                hi = mid
            else:
                lo = mid + 1
        return lo