import random


class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        max_run = 1
        cur = 1
        for i in range(1, n):
            if s[i] == s[i - 1]:
                cur += 1
                if cur > max_run:
                    max_run = cur
            else:
                cur = 1

        if max_run == 1:
            return 1
        if numOps == 0:
            return max_run

        arr = [1 if c == '1' else 0 for c in s]
        budget = numOps
        INF = budget + 1

        def feasible(L: int) -> bool:
            dp0 = [INF] * (L + 1)
            dp1 = [INF] * (L + 1)

            first = arr[0]
            dp0[1] = 0 if first == 0 else 1
            dp1[1] = 0 if first == 1 else 1

            if n == 1:
                return min(dp0[1], dp1[1]) <= budget

            for i in range(1, n):
                ch = arr[i]
                ndp0 = [INF] * (L + 1)
                ndp1 = [INF] * (L + 1)

                cost0 = 0 if ch == 0 else 1
                cost1 = 1 - cost0

                min0 = INF
                min1 = INF
                best0 = INF
                best1 = INF

                d0 = dp0
                d1 = dp1
                n0 = ndp0
                n1 = ndp1

                max_r = min(i, L)
                for r in range(1, max_r + 1):
                    v0 = d0[r]
                    if v0 < min0:
                        min0 = v0

                    v1 = d1[r]
                    if v1 < min1:
                        min1 = v1

                    if r < L:
                        if v0 <= budget:
                            nv = v0 + cost0
                            if nv < n0[r + 1]:
                                n0[r + 1] = nv
                                if nv < best0:
                                    best0 = nv

                        if v1 <= budget:
                            nv = v1 + cost1
                            if nv < n1[r + 1]:
                                n1[r + 1] = nv
                                if nv < best1:
                                    best1 = nv

                if min1 <= budget:
                    nv = min1 + cost0
                    if nv < n0[1]:
                        n0[1] = nv
                        if nv < best0:
                            best0 = nv

                if min0 <= budget:
                    nv = min0 + cost1
                    if nv < n1[1]:
                        n1[1] = nv
                        if nv < best1:
                            best1 = nv

                if best0 > budget and best1 > budget:
                    return False

                dp0, dp1 = ndp0, ndp1

            return best0 <= budget or best1 <= budget

        lo, hi = 1, max_run
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo


def brute_force(s: str, numOps: int) -> int:
    n = len(s)
    base = 0
    for i, c in enumerate(s):
        if c == '1':
            base |= 1 << i

    best = n
    for mask in range(1 << n):
        if bin(mask).count('1') > numOps:
            continue

        val = base ^ mask
        ans = 1
        cur = 1

        for i in range(1, n):
            if ((val >> i) & 1) == ((val >> (i - 1)) & 1):
                cur += 1
                if cur > ans:
                    ans = cur
            else:
                cur = 1

        if ans < best:
            best = ans
            if best == 1:
                break

    return best


def run_tests() -> None:
    sol = Solution()

    fixed_cases = [
        ("000001", 1, 2),
        ("0000", 2, 1),
        ("0101", 0, 1),
        ("0", 0, 1),
        ("1", 1, 1),
        ("00", 0, 2),
        ("00", 1, 1),
        ("000", 0, 3),
        ("000", 1, 1),
        ("00000", 0, 5),
        ("00000", 1, 2),
        ("00000", 2, 1),
        ("11111", 3, 1),
        ("000000", 3, 1),
        ("111111", 3, 1),
        ("0000000", 2, 2),
        ("0000000", 3, 1),
        ("1111111", 2, 2),
        ("1111111", 3, 1),
        ("00000000", 3, 2),
        ("00111100", 0, 4),
        ("01010", 5, 1),
    ]

    for s, ops, expected in fixed_cases:
        got = sol.minLength(s, ops)
        if got != expected:
            print(f"FAIL fixed case s={s} ops={ops} expected={expected} got={got}")
            raise RuntimeError("fixed case failed")

    # Exhaustive cross-check for all strings up to length 6.
    for n in range(1, 7):
        for mask in range(1 << n):
            s = ''.join('1' if (mask >> i) & 1 else '0' for i in range(n))
            for ops in range(n + 1):
                expected = brute_force(s, ops)
                got = sol.minLength(s, ops)
                if expected != got:
                    print(f"FAIL exhaustive s={s} ops={ops} expected={expected} got={got}")
                    raise RuntimeError("exhaustive test failed")

    # Random cross-check for slightly larger small strings.
    random.seed(20240527)
    for _ in range(200):
        n = random.randint(1, 10)
        s = ''.join(random.choice('01') for _ in range(n))
        ops = random.randint(0, n)
        expected = brute_force(s, ops)
        got = sol.minLength(s, ops)
        if expected != got:
            print(f"FAIL random s={s} ops={ops} expected={expected} got={got}")
            raise RuntimeError("random test failed")

    print("All tests passed")


if __name__ == "__main__":
    run_tests()