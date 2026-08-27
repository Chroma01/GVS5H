import random

class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0

        max_run = 1
        cur = 1
        for i in range(1, n):
            if s[i] == s[i - 1]:
                cur += 1
            else:
                cur = 1
            if cur > max_run:
                max_run = cur

        if max_run == 1 or numOps == 0:
            return max_run

        def feasible(L: int) -> bool:
            INF = numOps + 1
            dp0 = [INF] * (L + 1)
            dp1 = [INF] * (L + 1)

            dp0[1] = 0 if s[0] == '0' else 1
            dp1[1] = 1 if s[0] == '0' else 0

            for ch in s[1:]:
                ndp0 = [INF] * (L + 1)
                ndp1 = [INF] * (L + 1)
                add0 = 0 if ch == '0' else 1
                add1 = 1 - add0
                active = False

                for r in range(1, L + 1):
                    cost0 = dp0[r]
                    if cost0 < INF:
                        nc = cost0 + add1
                        if nc < INF and nc < ndp1[1]:
                            ndp1[1] = nc
                            active = True

                        if r < L:
                            nc = cost0 + add0
                            if nc < INF and nc < ndp0[r + 1]:
                                ndp0[r + 1] = nc
                                active = True

                    cost1 = dp1[r]
                    if cost1 < INF:
                        nc = cost1 + add0
                        if nc < INF and nc < ndp0[1]:
                            ndp0[1] = nc
                            active = True

                        if r < L:
                            nc = cost1 + add1
                            if nc < INF and nc < ndp1[r + 1]:
                                ndp1[r + 1] = nc
                                active = True

                if not active:
                    return False

                dp0, dp1 = ndp0, ndp1

            return min(min(dp0), min(dp1)) < INF

        lo, hi = 1, max_run
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo


_BRUTE_CACHE = {}


def _max_runs_for_n(n: int):
    if n not in _BRUTE_CACHE:
        arr = [0] * (1 << n)
        for mask in range(1 << n):
            if n == 0:
                arr[mask] = 0
            else:
                prev = mask & 1
                cur = 1
                best = 1
                for i in range(1, n):
                    bit = (mask >> i) & 1
                    if bit == prev:
                        cur += 1
                    else:
                        cur = 1
                        prev = bit
                    if cur > best:
                        best = cur
                arr[mask] = best
        _BRUTE_CACHE[n] = arr
    return _BRUTE_CACHE[n]


def _popcount(x: int) -> int:
    c = 0
    while x:
        c += x & 1
        x >>= 1
    return c


def brute_force(s: str, numOps: int) -> int:
    n = len(s)
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n > 10:
        raise ValueError("brute_force is only for small n")

    s_int = 0
    for i, ch in enumerate(s):
        if ch == '1':
            s_int |= 1 << i

    max_runs = _max_runs_for_n(n)
    best = n

    for mask in range(1 << n):
        if _popcount(mask ^ s_int) <= numOps:
            mr = max_runs[mask]
            if mr < best:
                best = mr
                if best == 1:
                    break

    return best


def _check(actual, expected, msg: str = "") -> None:
    if actual != expected:
        raise AssertionError(f"{msg} expected={expected} actual={actual}")


def _run_tests() -> None:
    sol = Solution()

    _check(sol.minLength("000001", 1), 2, "sample1")
    _check(sol.minLength("0000", 2), 1, "sample2")
    _check(sol.minLength("0101", 0), 1, "sample3")

    for s in ("0", "1"):
        for ops in (0, 1):
            _check(sol.minLength(s, ops), 1, f"n=1 s={s} ops={ops}")

    for n in (1, 2, 3, 4, 5, 6, 8, 10):
        strings = {
            "0" * n,
            "1" * n,
            "01" * (n // 2) + ("0" if n % 2 else ""),
            "10" * (n // 2) + ("1" if n % 2 else ""),
        }
        for s in strings:
            for ops in range(n + 1):
                _check(
                    sol.minLength(s, ops),
                    brute_force(s, ops),
                    f"edge s={s} ops={ops}",
                )

    random.seed(2024)
    for _ in range(200):
        n = random.randint(1, 8)
        s = ''.join(random.choice("01") for _ in range(n))
        for ops in range(n + 1):
            _check(
                sol.minLength(s, ops),
                brute_force(s, ops),
                f"random s={s} ops={ops}",
            )

    _check(sol.minLength("0" * 1000, 0), 1000, "large all zeros ops=0")
    _check(sol.minLength("0" * 1000, 1000), 1, "large all zeros ops=n")
    _check(sol.minLength("01" * 500, 0), 1, "large alternating ops=0")

    print("All tests passed")


if __name__ == "__main__":
    _run_tests()