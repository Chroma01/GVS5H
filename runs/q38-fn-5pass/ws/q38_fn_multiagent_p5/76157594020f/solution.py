class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n <= 1:
            return n

        max_run = self._max_run(s)
        if numOps == 0 or max_run == 1:
            return max_run

        lo, hi = 1, max_run
        while lo < hi:
            mid = (lo + hi) // 2
            if self._min_flips(s, mid, numOps) <= numOps:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def _max_run(self, s: str) -> int:
        best = 1
        cur = 1
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                cur += 1
            else:
                cur = 1
            if cur > best:
                best = cur
        return best

    def _min_flips(self, s: str, limit: int, cap: int) -> int:
        n = len(s)
        INF = cap + 1

        dp0 = [INF] * (limit + 1)
        dp1 = [INF] * (limit + 1)

        first = 1 if s[0] == '1' else 0
        if first == 0:
            dp0[1] = 0
            if cap >= 1:
                dp1[1] = 1
        else:
            dp1[1] = 0
            if cap >= 1:
                dp0[1] = 1

        for i in range(1, n):
            cost0 = 0 if s[i] == '0' else 1
            cost1 = 1 - cost0

            ndp0 = [INF] * (limit + 1)
            ndp1 = [INF] * (limit + 1)

            best0 = min(dp0)
            if best0 != INF:
                nv = best0 + cost1
                if nv <= cap and nv < ndp1[1]:
                    ndp1[1] = nv

            best1 = min(dp1)
            if best1 != INF:
                nv = best1 + cost0
                if nv <= cap and nv < ndp0[1]:
                    ndp0[1] = nv

            for r in range(1, limit):
                v = dp0[r]
                if v != INF:
                    nv = v + cost0
                    if nv <= cap and nv < ndp0[r + 1]:
                        ndp0[r + 1] = nv

                v = dp1[r]
                if v != INF:
                    nv = v + cost1
                    if nv <= cap and nv < ndp1[r + 1]:
                        ndp1[r + 1] = nv

            dp0, dp1 = ndp0, ndp1

        return min(min(dp0), min(dp1))

    def _min_flips_brute(self, s: str, limit: int) -> int:
        n = len(s)
        target = [1 if ch == '1' else 0 for ch in s]
        best = n + 1

        for mask in range(1 << n):
            dist = 0
            run = 0
            prev = -1
            max_run = 0

            for i in range(n):
                bit = (mask >> i) & 1
                if bit != target[i]:
                    dist += 1
                    if dist >= best:
                        break

                if bit == prev:
                    run += 1
                else:
                    run = 1
                    prev = bit

                if run > max_run:
                    max_run = run
                    if max_run > limit:
                        break
            else:
                if dist < best:
                    best = dist

        return best

    def _verify_small(self, max_n: int = 8) -> bool:
        for n in range(1, max_n + 1):
            for mask in range(1 << n):
                s = ''.join('1' if (mask >> i) & 1 else '0' for i in range(n))
                for limit in range(1, n + 1):
                    dp = self._min_flips(s, limit, n)
                    brute = self._min_flips_brute(s, limit)
                    if dp != brute:
                        return False
        return True


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("000001", 1, 2),
        ("0000", 2, 1),
        ("0101", 0, 1),
    ]

    all_pass = True
    for s, numOps, expected in tests:
        got = sol.minLength(s, numOps)
        if got != expected:
            all_pass = False
            print(f"FAIL: s={s!r}, numOps={numOps}, expected={expected}, got={got}")

    if all_pass:
        print("SAMPLE TESTS PASS")
    else:
        print("SAMPLE TESTS FAIL")