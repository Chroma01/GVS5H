from itertools import combinations

MOD = 10**9 + 7


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        total = m * n

        def comb(N: int, r: int) -> int:
            if r < 0 or r > N:
                return 0
            r = min(r, N - r)
            num = 1
            den = 1
            for i in range(1, r + 1):
                num = num * (N - r + i) % MOD
                den = den * i % MOD
            return num * pow(den, MOD - 2, MOD) % MOD

        c = comb(total - 2, k - 2)
        m2 = m * m % MOD
        n2 = n * n % MOD
        # Sum of Manhattan distances over all unordered pairs of distinct cells:
        #   row part: n^2 * m(m^2 - 1) / 6
        #   col part: m^2 * n(n^2 - 1) / 6
        S = (n2 * (m * (m2 - 1) % MOD) + m2 * (n * (n2 - 1) % MOD)) % MOD
        inv6 = pow(6, MOD - 2, MOD)
        return c * S % MOD * inv6 % MOD


# ---------------- verification (not part of submission) ----------------
def brute(m: int, n: int, k: int) -> int:
    cells = [(i, j) for i in range(m) for j in range(n)]
    total = 0
    for combo in combinations(range(len(cells)), k):
        pts = [cells[idx] for idx in combo]
        for a in range(len(pts)):
            for b in range(a + 1, len(pts)):
                total += abs(pts[a][0] - pts[b][0]) + abs(pts[a][1] - pts[b][1])
    return total


if __name__ == "__main__":
    sol = Solution()
    assert sol.distanceSum(2, 2, 2) == 8, sol.distanceSum(2, 2, 2)
    assert sol.distanceSum(1, 4, 3) == 20, sol.distanceSum(1, 4, 3)
    for m in range(1, 9):
        for n in range(1, 9):
            if m * n > 8:
                continue
            for k in range(2, m * n + 1):
                got = sol.distanceSum(m, n, k)
                exp = brute(m, n, k) % MOD
                assert got == exp, (m, n, k, got, exp)
    print("all tests passed")