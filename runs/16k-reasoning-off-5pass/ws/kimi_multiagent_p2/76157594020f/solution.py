class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def flipsNeeded(L: int) -> int:
            """Minimum flips so that every run of identical chars has length <= L."""
            if L == 1:
                # Resulting string must alternate; only two possible targets.
                # Pattern A: s[i] should be '0' if i even else '1'
                # Pattern B: the opposite. Mismatches to A and B sum to n.
                mism_a = 0
                for i, ch in enumerate(s):
                    expected = '0' if i % 2 == 0 else '1'
                    if ch != expected:
                        mism_a += 1
                return min(mism_a, n - mism_a)

            # L >= 2: handle each maximal run independently.
            # A run of length `run` needs floor(run / (L+1)) flips, and for
            # L >= 2 we can always place flips away from run boundaries so the
            # flipped chars never merge with neighboring runs.
            total = 0
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                run = j - i
                total += run // (L + 1)
                i = j
            return total

        # Binary search the smallest feasible L in [1, n].
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if flipsNeeded(mid) <= numOps:
                hi = mid
            else:
                lo = mid + 1
        return lo