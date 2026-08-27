class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 1:
            return 1

        bits = [ord(c) - 48 for c in s]

        # Original maximum run length. Zero flips always achieves this.
        max_run = 1
        cur = 1
        for i in range(1, n):
            if bits[i] == bits[i - 1]:
                cur += 1
            else:
                cur = 1
            if cur > max_run:
                max_run = cur

        if numOps == 0:
            return max_run

        # Minimum flips to make the string strictly alternating.
        # Pattern 0101... has mismatches mism0; pattern 1010... has n - mism0.
        mism0 = 0
        for i, b in enumerate(bits):
            if b != (i & 1):
                mism0 += 1
        if min(mism0, n - mism0) <= numOps:
            return 1

        limit = numOps
        INF = limit + 1

        def feasible(L: int) -> bool:
            # The original string already has max run <= L.
            if L >= max_run:
                return True

            # Max run 1 means strictly alternating.
            if L == 1:
                return min(mism0, n - mism0) <= limit

            # dp0[r] = min flips for processed prefix ending in bit 0
            #          with current run length r.
            # dp1[r] = same for ending in bit 1.
            dp0 = [INF] * (L + 1)
            dp1 = [INF] * (L + 1)

            first = bits[0]
            if first == 0:
                dp0[1] = 0
                if limit >= 1:
                    dp1[1] = 1
            else:
                dp1[1] = 0
                if limit >= 1:
                    dp0[1] = 1

            for i in range(1, n):
                bit = bits[i]
                ndp0 = [INF] * (L + 1)
                ndp1 = [INF] * (L + 1)

                if bit == 0:
                    # Original bit is 0.
                    # From last 0: keep 0 costs 0, switch to 1 costs 1.
                    # From last 1: keep 1 costs 1, switch to 0 costs 0.
                    for r in range(1, L + 1):
                        c0 = dp0[r]
                        if c0 <= limit:
                            if r < L and c0 < ndp0[r + 1]:
                                ndp0[r + 1] = c0
                            nc = c0 + 1
                            if nc <= limit and nc < ndp1[1]:
                                ndp1[1] = nc

                        c1 = dp1[r]
                        if c1 <= limit:
                            if r < L:
                                nc = c1 + 1
                                if nc <= limit and nc < ndp1[r + 1]:
                                    ndp1[r + 1] = nc
                            if c1 < ndp0[1]:
                                ndp0[1] = c1
                else:
                    # Original bit is 1.
                    # From last 0: keep 0 costs 1, switch to 1 costs 0.
                    # From last 1: keep 1 costs 0, switch to 0 costs 1.
                    for r in range(1, L + 1):
                        c0 = dp0[r]
                        if c0 <= limit:
                            if r < L:
                                nc = c0 + 1
                                if nc <= limit and nc < ndp0[r + 1]:
                                    ndp0[r + 1] = nc
                            if c0 < ndp1[1]:
                                ndp1[1] = c0

                        c1 = dp1[r]
                        if c1 <= limit:
                            if r < L and c1 < ndp1[r + 1]:
                                ndp1[r + 1] = c1
                            nc = c1 + 1
                            if nc <= limit and nc < ndp0[1]:
                                ndp0[1] = nc

                dp0, dp1 = ndp0, ndp1

            for r in range(1, L + 1):
                if dp0[r] <= limit or dp1[r] <= limit:
                    return True
            return False

        lo, hi = 1, max_run
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


def _brute_all(s: str):
    n = len(s)
    bits = [ord(c) - 48 for c in s]
    size = 1 << n

    pop = [0] * size
    for m in range(1, size):
        pop[m] = pop[m >> 1] + (m & 1)

    best_exact = [n] * size
    for mask in range(size):
        cost = pop[mask]
        prev = -1
        cur = 0
        local = 0

        for i in range(n):
            b = bits[i] ^ ((mask >> i) & 1)
            if b == prev:
                cur += 1
            else:
                prev = b
                cur = 1
            if cur > local:
                local = cur

        if local < best_exact[cost]:
            best_exact[cost] = local

    res = []
    best = n
    for k in range(n + 1):
        if best_exact[k] < best:
            best = best_exact[k]
        res.append(best)
    return res


def _run_tests():
    sol = Solution()

    examples = [
        ("000001", 1, 2),
        ("0000", 2, 1),
        ("0101", 0, 1),
    ]
    for s, k, expected in examples:
        got = sol.minLength(s, k)
        assert got == expected, f"example failed: s={s}, numOps={k}, got={got}, expected={expected}"

    # Large sanity checks.
    assert sol.minLength("0" * 1000, 0) == 1000
    assert sol.minLength("0" * 1000, 1000) == 1
    assert sol.minLength("0" * 1000, 500) == 1
    assert sol.minLength("0" * 1000, 499) == 2
    assert sol.minLength("0" * 999, 499) == 1

    # Exhaustive brute-force validation for small lengths.
    for n in range(1, 9):
        for mask in range(1 << n):
            s = "".join("1" if (mask >> i) & 1 else "0" for i in range(n))
            expected = _brute_all(s)
            for k in range(n + 1):
                got = sol.minLength(s, k)
                if got != expected[k]:
                    raise AssertionError(
                        f"brute mismatch: n={n}, s={s}, numOps={k}, got={got}, expected={expected[k]}"
                    )


if __name__ == "__main__":
    _run_tests()