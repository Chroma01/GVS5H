class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        # Collect maximal run lengths of the original string.
        runs = []
        cur = 1
        for i in range(1, n):
            if s[i] == s[i - 1]:
                cur += 1
            else:
                runs.append(cur)
                cur = 1
        runs.append(cur)

        max_run = max(runs)
        if max_run == 1:
            return 1  # already alternating (also covers n == 1)

        # Min flips to reach a fully alternating string = min Hamming distance
        # to "0101..." and to its complement "1010...".
        d0 = 0
        for i, ch in enumerate(s):
            cbit = 1 if ch == '1' else 0
            if cbit != (i & 1):     # pattern P0 has bit == i % 2
                d0 += 1
        min_alt = min(d0, n - d0)

        def can(L: int) -> bool:
            if L == 1:
                return min_alt <= numOps
            total = 0
            for r in runs:
                total += r // (L + 1)   # flips needed to break this run
                if total > numOps:
                    return False
            return True

        lo, hi = 1, max_run
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo