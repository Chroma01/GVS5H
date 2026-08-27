from typing import List
import random
import sys


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0

        max_point = max(points)
        lo = 0
        hi = (m * max_point) // n + 1
        NEG = -10**30

        pts = points
        N = n
        M = m
        last = N - 1

        def can(x: int) -> bool:
            if x == 0:
                return True
            if M < N:
                return False

            a = [0] * N
            b = [0] * N

            for i, pt in enumerate(pts):
                r = (x + pt - 1) // pt
                if r > M:
                    return False

                if i == last:
                    a[i] = r - 1 if r > 1 else 0
                else:
                    a[i] = r - 2 if r > 2 else 0
                    b[i] = r - 1 if r > 1 else 0

            # g0[i] = maximum weight independent set on suffix i..N-1 using a weights.
            # If vertex i is taken, vertex i+1 is excluded, so use g0[i+2].
            g0 = [0] * (N + 2)
            for i in range(last, -1, -1):
                take = a[i] + g0[i + 2]
                skip = g0[i + 1]
                g0[i] = take if take > skip else skip

            # Prefix DP for b weights:
            # p0 = best prefix 0..p-1 with vertex p-1 not taken
            # p1 = best prefix 0..p-1 with vertex p-1 taken
            p0 = 0
            p1 = NEG
            base = 2 * N - 1

            for p in range(N):
                # Combine prefix 0..p-1 with suffix p..N-1.
                # If prefix last is not taken, suffix p may be taken: g0[p].
                # If prefix last is taken, suffix p must be excluded: g0[p+1].
                c = p0 + g0[p]
                alt = p1 + g0[p + 1]
                if alt > c:
                    c = alt

                if base - p + 2 * c <= M:
                    return True

                # Move vertex p into the prefix with weight b[p].
                np0 = p0 if p0 >= p1 else p1
                np1 = p0 + b[p]
                p0, p1 = np0, np1

            return False

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid

        return lo


def brute(points: List[int], m: int) -> int:
    n = len(points)
    best = 0
    scores = [0] * n

    def dfs(pos: int, depth: int) -> None:
        nonlocal best
        if depth > 0:
            mn = min(scores)
            if mn > best:
                best = mn
        if depth == m:
            return

        if pos == -1:
            scores[0] += points[0]
            dfs(0, depth + 1)
            scores[0] -= points[0]
        else:
            if pos + 1 < n:
                scores[pos + 1] += points[pos + 1]
                dfs(pos + 1, depth + 1)
                scores[pos + 1] -= points[pos + 1]
            if pos - 1 >= 0:
                scores[pos - 1] += points[pos - 1]
                dfs(pos - 1, depth + 1)
                scores[pos - 1] -= points[pos - 1]

    dfs(-1, 0)
    return best


def n2_expected(points: List[int], m: int) -> int:
    a, b = points

    def feasible(x: int) -> bool:
        if x == 0:
            return True
        r0 = (x + a - 1) // a
        r1 = (x + b - 1) // b

        # End at index 0: base moves 3, base visits [2, 1].
        moves0 = 3 + 2 * max(0, r0 - 2, r1 - 1)
        # End at index 1: base moves 2, base visits [1, 1].
        moves1 = 2 + 2 * max(0, r0 - 1, r1 - 1)

        return min(moves0, moves1) <= m

    lo = 0
    hi = (m * max(a, b)) // 2 + 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    return lo


def run_sample_tests() -> bool:
    sol = Solution()
    failures = []

    def check(desc: str, cond: bool, info: str = "") -> None:
        if not cond:
            failures.append(f"{desc}: {info}")

    # Examples.
    got = sol.maxScore([2, 4], 3)
    check("example1", got == 4, f"got {got}")

    got = sol.maxScore([1, 2, 3], 5)
    check("example2", got == 2, f"got {got}")

    # n = 2 small exhaustive: brute force and closed form.
    for a in range(1, 4):
        for b in range(1, 4):
            for m in range(1, 11):
                pts = [a, b]
                expected_brute = brute(pts, m)
                expected_n2 = n2_expected(pts, m)
                got = sol.maxScore(pts, m)
                check(
                    f"n2 small a={a} b={b} m={m}",
                    got == expected_brute == expected_n2,
                    f"got {got}, brute {expected_brute}, n2 {expected_n2}",
                )

    # m < n.
    got = sol.maxScore([1, 1], 0)
    check("m=0", got == 0, f"got {got}")

    got = sol.maxScore([1, 1, 1, 1], 2)
    check("m<n small", got == 0, f"got {got}")

    got = sol.maxScore([5, 5, 5], 1)
    check("m<n n=3", got == 0, f"got {got}")

    got = sol.maxScore([10**6] * 50000, 49999)
    check("m<n large", got == 0, f"got {got}")

    # Large n, m = n.
    pts = [10**6] * 50000
    got = sol.maxScore(pts, 50000)
    check("large n m=n all equal", got == 10**6, f"got {got}")

    pts[12345] = 1
    got = sol.maxScore(pts, 50000)
    check("large n m=n min one", got == 1, f"got {got}")

    # Large m/points on n = 2.
    large_n2_cases = [
        (10**6, 999999, 10**9),
        (1, 10**6, 10**9),
        (123456, 789012, 999999999),
        (1, 1, 10**9),
    ]
    for a, b, m in large_n2_cases:
        pts = [a, b]
        expected = n2_expected(pts, m)
        got = sol.maxScore(pts, m)
        check(
            f"large n2 a={a} b={b} m={m}",
            got == expected,
            f"got {got}, expected {expected}",
        )

    # Large n, large m sanity bounds.
    pts = [10**6] * 50000
    m = 10**9
    got = sol.maxScore(pts, m)
    ub = (m * 10**6) // 50000
    check("large n large m bounds", 0 <= got <= ub, f"got {got}, ub {ub}")
    check("large n large m lower bound", got >= 10**6, f"got {got}")

    # Random brute force small cases.
    random.seed(12345)
    for case in range(200):
        n = random.randint(2, 4)
        m = random.randint(1, 8)
        pts = [random.randint(1, 5) for _ in range(n)]
        expected = brute(pts, m)
        got = sol.maxScore(pts, m)
        check(
            f"random case {case} pts={pts} m={m}",
            got == expected,
            f"got {got}, expected {expected}",
        )

    if failures:
        for f in failures[:20]:
            print(f)
        if len(failures) > 20:
            print(f"... and {len(failures) - 20} more failures")
        print("SAMPLE TESTS FAIL")
        return False

    print("SAMPLE TESTS PASS")
    return True


if __name__ == "__main__":
    try:
        ok = run_sample_tests()
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        print("SAMPLE TESTS FAIL")
        ok = False
    sys.exit(0 if ok else 1)