class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0

        bits = [1 if ch == '1' else 0 for ch in s]

        max_run = 1
        cur = 1
        for i in range(1, n):
            if bits[i] == bits[i - 1]:
                cur += 1
                if cur > max_run:
                    max_run = cur
            else:
                cur = 1

        INF = numOps + 1

        def feasible(L: int) -> bool:
            dp0 = [INF] * (L + 1)
            dp1 = [INF] * (L + 1)

            first = bits[0]
            dp0[1] = first
            dp1[1] = 1 - first

            for i in range(1, n):
                b = bits[i]

                min0 = min(dp0)
                min1 = min(dp1)
                if min0 == INF and min1 == INF:
                    return False

                c0 = b
                c1 = 1 - b

                ndp0 = [INF] * (L + 1)
                ndp1 = [INF] * (L + 1)

                if min1 < INF:
                    val = min1 + c0
                    ndp0[1] = val if val < INF else INF
                if min0 < INF:
                    val = min0 + c1
                    ndp1[1] = val if val < INF else INF

                if L > 1:
                    if c0 == 0:
                        ndp0[2:] = dp0[1:L]
                    else:
                        ndp0[2:] = [x + 1 if x < INF else INF for x in dp0[1:L]]

                    if c1 == 0:
                        ndp1[2:] = dp1[1:L]
                    else:
                        ndp1[2:] = [x + 1 if x < INF else INF for x in dp1[1:L]]

                dp0, dp1 = ndp0, ndp1

            return min(min(dp0), min(dp1)) <= numOps

        lo, hi = 1, max_run
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo


if __name__ == "__main__":
    import random

    def brute_force(s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0
        best = n
        for mask in range(1 << n):
            dist = 0
            prev = None
            cur = 0
            maxr = 0
            for i in range(n):
                ch = '1' if ((mask >> i) & 1) else '0'
                if ch != s[i]:
                    dist += 1
                    if dist > numOps:
                        break
                if ch == prev:
                    cur += 1
                else:
                    cur = 1
                if cur > maxr:
                    maxr = cur
            else:
                if dist <= numOps and maxr < best:
                    best = maxr
        return best

    sol = Solution()
    failures = []

    examples = [
        ("000001", 1, 2),
        ("0000", 2, 1),
        ("0101", 0, 1),
    ]
    for s, ops, expected in examples:
        got = sol.minLength(s, ops)
        if got != expected:
            failures.append(f"example {s} {ops}: expected {expected}, got {got}")

    edge_cases = [
        ("0", 0),
        ("1", 1),
        ("00000", 0),
        ("00000", 5),
        ("11111", 0),
        ("11111", 1),
        ("11111", 2),
        ("101010", 0),
        ("110011", 1),
        ("0000000000", 0),
        ("0000000000", 1),
        ("0101010101", 0),
    ]
    for s, ops in edge_cases:
        expected = brute_force(s, ops)
        got = sol.minLength(s, ops)
        if got != expected:
            failures.append(f"edge {s} {ops}: expected {expected}, got {got}")

    random.seed(12345)
    for _ in range(100):
        n = random.randint(1, 10)
        s = ''.join(random.choice('01') for _ in range(n))
        ops = random.randint(0, n)
        expected = brute_force(s, ops)
        got = sol.minLength(s, ops)
        if got != expected:
            failures.append(f"random {s} {ops}: expected {expected}, got {got}")

    if failures:
        print("FAIL")
        for msg in failures[:10]:
            print(msg)
    else:
        print("PASS")