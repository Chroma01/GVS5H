from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0

        pts = points
        nn = n
        mm = m

        def check(x: int) -> bool:
            if x == 0:
                return True
            if mm < nn:
                return False

            # a[i] = req[i] - 1
            # b[i] = max(0, req[i] - 2)
            a = [0] * nn
            b = [0] * nn
            total_req = 0

            for i, pnt in enumerate(pts):
                r = (x + pnt - 1) // pnt
                total_req += r
                if total_req > mm:
                    return False

                a[i] = r - 1
                bi = r - 2
                if bi < 0:
                    bi = 0
                b[i] = bi

            # Suffix MWIS DP for c[i] = b[i] for i < n-1, c[n-1] = a[n-1].
            # suf0[i]: best on i..n-1 with vertex i not selected.
            # suf1[i]: best on i..n-1 with vertex i selected.
            suf0 = [0] * (nn + 1)
            suf1 = [0] * (nn + 1)
            last = nn - 1

            for i in range(last, -1, -1):
                w = a[i] if i == last else b[i]
                s0 = suf0[i + 1]
                s1 = suf1[i + 1]
                suf0[i] = s0 if s0 >= s1 else s1
                suf1[i] = s0 + w

            # Prefix MWIS DP for a[0..p-1].
            pref0 = 0
            pref1 = -1  # invalid selected state for empty prefix
            base = 2 * nn - 1

            for p in range(last):
                # Endpoint p < n-1:
                # weights are a[0..p-1], b[p], b[p+1..n-2], a[n-1].
                if base - p <= mm:
                    mid0 = pref0 if pref0 >= pref1 else pref1
                    mid1 = pref0 + b[p]

                    s0 = suf0[p + 1]
                    s1 = suf1[p + 1]
                    best_suf = s0 if s0 >= s1 else s1

                    val0 = mid0 + best_suf
                    val1 = mid1 + s0
                    best = val0 if val0 >= val1 else val1

                    if base - p + 2 * best <= mm:
                        return True

                # Add a[p] to prefix for the next endpoint.
                new0 = pref0 if pref0 >= pref1 else pref1
                new1 = pref0 + a[p]
                pref0, pref1 = new0, new1

            # Endpoint p = n-1:
            # weights are a[0..n-1].
            best0 = pref0 if pref0 >= pref1 else pref1
            best1 = pref0 + a[last]
            best = best0 if best0 >= best1 else best1

            if nn + 2 * best <= mm:
                return True

            return False

        lo = 0
        hi = mm * min(pts) + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if check(mid):
                lo = mid
            else:
                hi = mid

        return lo


def _brute(points: List[int], m: int) -> int:
    n = len(points)
    best = 0
    scores = [0] * n

    def dfs(pos: int, left: int) -> None:
        nonlocal best

        cur = scores[0]
        for v in scores[1:]:
            if v < cur:
                cur = v
        if cur > best:
            best = cur

        if left == 0:
            return

        if pos == -1:
            scores[0] += points[0]
            dfs(0, left - 1)
            scores[0] -= points[0]
        else:
            if pos > 0:
                np = pos - 1
                scores[np] += points[np]
                dfs(np, left - 1)
                scores[np] -= points[np]
            if pos < n - 1:
                np = pos + 1
                scores[np] += points[np]
                dfs(np, left - 1)
                scores[np] -= points[np]

    dfs(-1, m)
    return best


def _run_tests() -> None:
    sol = Solution()

    assert sol.maxScore([2, 4], 3) == 4
    assert sol.maxScore([1, 2, 3], 5) == 2
    assert sol.maxScore([1, 1], 1) == 0
    assert sol.maxScore([5, 5], 2) == 5
    assert sol.maxScore([1, 100], 3) == 2
    assert sol.maxScore([100, 1], 3) == 1

    from itertools import product

    for n in (2, 3):
        for pts in product(range(1, 4), repeat=n):
            pts_list = list(pts)
            for m in range(1, 8):
                expected = _brute(pts_list, m)
                got = sol.maxScore(pts_list, m)
                if got != expected:
                    raise AssertionError((pts_list, m, got, expected))

    import random

    rng = random.Random(12345)
    for _ in range(80):
        n = rng.randint(2, 5)
        m = rng.randint(1, 10)
        pts = [rng.randint(1, 10) for _ in range(n)]
        expected = _brute(pts, m)
        got = sol.maxScore(pts, m)
        if got != expected:
            raise AssertionError((pts, m, got, expected))


if __name__ == "__main__":
    _run_tests()