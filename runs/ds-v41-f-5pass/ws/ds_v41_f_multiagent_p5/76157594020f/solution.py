class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        bits = [1 if c == '1' else 0 for c in s]
        INF = float('inf')

        def feasible(L):
            # dp0[r] = min flips over the processed prefix so that it ends in
            # bit 0 and its trailing run of 0s has length exactly r (1 <= r <= L).
            # dp1[r] is analogous for bit 1.
            dp0 = [INF] * (L + 1)
            dp1 = [INF] * (L + 1)
            dp0[1] = 0 if bits[0] == 0 else 1
            dp1[1] = 0 if bits[0] == 1 else 1

            for i in range(1, n):
                c = bits[i]
                cost0 = c          # flips needed to place a '0' at position i
                cost1 = 1 - c      # flips needed to place a '1' at position i

                ndp0 = [INF] * (L + 1)
                ndp1 = [INF] * (L + 1)

                # switch from the opposite bit -> brand new run of length 1
                ndp0[1] = min(dp1[1:]) + cost0
                ndp1[1] = min(dp0[1:]) + cost1

                # extend the same bit -> run grows by one (stays <= L)
                # NOTE: the cost of the current character MUST be paid here too.
                ndp0[2:L + 1] = [x + cost0 for x in dp0[1:L]]
                ndp1[2:L + 1] = [x + cost1 for x in dp1[1:L]]

                dp0, dp1 = ndp0, ndp1

            return min(min(dp0[1:]), min(dp1[1:])) <= numOps

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


if __name__ == "__main__":
    from itertools import product

    sol = Solution()

    tests = [
        ("000001", 1, 2),
        ("0000", 2, 1),
        ("0101", 0, 1),
        ("100001", 2, 2),
        ("0", 0, 1),
        ("0000", 0, 4),
        ("000000", 6, 1),   # numOps = n on all-identical string
        ("111111", 1, 3),   # would be wrong with the old missing-cost extend
        ("111111", 2, 2),
        ("111111", 0, 6),
        ("0110", 1, 2),     # greedy counterexample
    ]
    allpass = True
    for s, k, exp in tests:
        got = sol.minLength(s, k)
        ok = got == exp
        allpass &= ok
        print(f"s={s!r:>10} numOps={k} expected={exp} got={got} {'PASS' if ok else 'FAIL'}")

    def brute(s, numOps):
        n = len(s)
        best = n
        for tup in product('01', repeat=n):
            if sum(a != b for a, b in zip(tup, s)) > numOps:
                continue
            mr = cur = 1
            for i in range(1, n):
                cur = cur + 1 if tup[i] == tup[i - 1] else 1
                if cur > mr:
                    mr = cur
            if mr < best:
                best = mr
        return best

    bf_pass = True
    checked = 0
    for n in range(1, 7):
        for tup in product('01', repeat=n):
            s = ''.join(tup)
            for k in range(0, n + 1):
                checked += 1
                a = sol.minLength(s, k)
                b = brute(s, k)
                if a != b:
                    bf_pass = False
                    print(f"BRUTE MISMATCH s={s} numOps={k} dp={a} brute={b}")
    print(f"brute-force cross-check ({checked} cases):", "PASS" if bf_pass else "FAIL")
    allpass &= bf_pass
    print("ALL:", "PASS" if allpass else "FAIL")