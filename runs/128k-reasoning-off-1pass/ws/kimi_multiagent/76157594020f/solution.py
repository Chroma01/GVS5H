class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        # Precompute maximal run lengths
        runs = []
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            runs.append(j - i)
            i = j

        def flips_for_alternating(start: int) -> int:
            # cost to make s alternate starting with bit `start`
            cost = 0
            for idx, ch in enumerate(s):
                expected = (start + idx) & 1
                if (ord(ch) - 48) != expected:
                    cost += 1
            return cost

        def check(L: int) -> bool:
            if L == 1:
                # string must be alternating; only two possible patterns
                return min(flips_for_alternating(0), flips_for_alternating(1)) <= numOps
            total = 0
            for ln in runs:
                total += ln // (L + 1)
                if total > numOps:
                    return False
            return total <= numOps

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if check(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo