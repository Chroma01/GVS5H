from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        max_p = max(points)

        def feasible(X: int) -> bool:
            if X == 0:
                return True
            # required minimum number of landings at index i
            r = [(X + p - 1) // p for p in points]

            # Right suffix MWIS: weights R'_i = r_i - 2 for i<=n-2, r_{n-1}-1
            right0 = [0] * (n + 1)   # index i NOT selected
            right1 = [0] * (n + 1)   # index i selected
            for i in range(n - 1, -1, -1):
                w = r[i] - (1 if i == n - 1 else 2)
                if w < 0:
                    w = 0
                a = right0[i + 1]
                b = right1[i + 1]
                right0[i] = a if a > b else b
                right1[i] = a + w

            # e == 0 : all edges even, base 2
            MWIS0 = right0[0] if right0[0] > right1[0] else right1[0]
            Lmin = 1 + 2 * (n - 1) + 2 * MWIS0

            # Left prefix MWIS: weights R'_i = r_i - 1  (i <= n-2)
            left0 = [0] * n
            left1 = [0] * n
            for i in range(n - 1):
                a = r[i] - 1
                if a < 0:
                    a = 0
                if i == 0:
                    left0[i] = 0
                    left1[i] = a
                else:
                    p0 = left0[i - 1]
                    p1 = left1[i - 1]
                    left0[i] = p0 if p0 > p1 else p1
                    left1[i] = p0 + a

            for e in range(1, n):
                l0 = left0[e - 1]
                l1 = left1[e - 1]
                r0 = right0[e]
                r1 = right1[e]
                # forbid selecting both e-1 and e
                m1 = l0 + (r0 if r0 > r1 else r1)
                m2 = l1 + r0
                mwis = m1 if m1 > m2 else m2
                L = 1 + 2 * (n - 1) - e + 2 * mwis
                if L < Lmin:
                    Lmin = L

            return Lmin <= m

        low = 0
        high = max_p * m
        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1
        return low


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ([2, 4], 3, 4, "example1"),
        ([1, 2, 3], 5, 2, "example2"),
        ([2, 4], 2, 2, "n=2 m=2 -> min(points)"),
        ([5, 7], 1, 0, "n=2 m=1 -> impossible"),
        ([1, 2, 3, 4], 3, 0, "m<n -> 0"),
        ([1, 1], 1, 0, "single move unreachable peer"),
        ([1, 1], 10**9, 5 * 10**8, "large m balanced"),
        ([1000000, 1], 3, 1, "huge/small mismatch"),
        ([10**6] * 50000, 10**9, 2 * 10**10, "large scale n=5e4"),
    ]
    for pts, mm, exp, name in cases:
        got = sol.maxScore(list(pts), mm)
        status = "OK" if got == exp else "FAIL"
        print(f"{name}: len={len(pts)}, m={mm} -> got={got}, expected={exp} [{status}]")