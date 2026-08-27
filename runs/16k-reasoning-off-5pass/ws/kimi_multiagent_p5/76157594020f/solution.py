class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(L: int) -> bool:
            if L == 1:
                # Final string must be perfectly alternating.
                # Count mismatches against both alternating targets.
                mism0 = 0  # target pattern starting with '0': "0101..."
                for i, ch in enumerate(s):
                    expected = '0' if i % 2 == 0 else '1'
                    if ch != expected:
                        mism0 += 1
                mism1 = n - mism0  # mismatches to the opposite pattern "1010..."
                return min(mism0, mism1) <= numOps
            # L >= 2: handle each maximal run independently.
            flips = 0
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                m = j - i
                # Place flips every (L+1) positions inside the run.
                flips += m // (L + 1)
                if flips > numOps:
                    return False
                i = j
            return flips <= numOps

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo