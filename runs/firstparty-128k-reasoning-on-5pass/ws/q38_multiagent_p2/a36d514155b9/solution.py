MOD = 1_000_000_007
INV6 = pow(6, MOD - 2, MOD)


class Solution:
    MOD = MOD
    _fact = None
    _invfact = None

    @classmethod
    def _ensure_factorials(cls, limit: int) -> None:
        if cls._fact is None:
            limit = max(limit, 100000)

        if cls._fact is None or len(cls._fact) <= limit:
            fact = [1] * (limit + 1)
            for i in range(1, limit + 1):
                fact[i] = fact[i - 1] * i % cls.MOD

            invfact = [1] * (limit + 1)
            invfact[limit] = pow(fact[limit], cls.MOD - 2, cls.MOD)
            for i in range(limit, 0, -1):
                invfact[i - 1] = invfact[i] * i % cls.MOD

            cls._fact = fact
            cls._invfact = invfact

    @classmethod
    def _comb(cls, n: int, r: int) -> int:
        if r < 0 or r > n:
            return 0
        cls._ensure_factorials(n)
        return cls._fact[n] * cls._invfact[r] % cls.MOD * cls._invfact[n - r] % cls.MOD

    def distanceSum(self, m: int, n: int, k: int) -> int:
        cells = m * n
        ways = self._comb(cells - 2, k - 2)

        m_mod = m % self.MOD
        n_mod = n % self.MOD

        row_sum = m_mod * ((m_mod * m_mod - 1) % self.MOD) % self.MOD
        row_sum = row_sum * INV6 % self.MOD

        col_sum = n_mod * ((n_mod * n_mod - 1) % self.MOD) % self.MOD
        col_sum = col_sum * INV6 % self.MOD

        pair_distance_sum = (
            n_mod * n_mod % self.MOD * row_sum
            + m_mod * m_mod % self.MOD * col_sum
        ) % self.MOD

        return ways * pair_distance_sum % self.MOD


def _brute_force(m: int, n: int, k: int) -> int:
    from itertools import combinations

    cells = [(i, j) for i in range(m) for j in range(n)]
    total = 0

    for chosen in combinations(cells, k):
        for a in range(k):
            xa, ya = chosen[a]
            for b in range(a + 1, k):
                xb, yb = chosen[b]
                total += abs(xa - xb) + abs(ya - yb)

    return total % MOD


if __name__ == "__main__":
    sol = Solution()

    assert sol.distanceSum(2, 2, 2) == 8
    assert sol.distanceSum(1, 4, 3) == 20
    assert sol.distanceSum(1, 2, 2) == 1
    assert sol.distanceSum(2, 1, 2) == 1
    assert sol.distanceSum(3, 3, 9) == 72

    for m in range(1, 4):
        for n in range(1, 4):
            total_cells = m * n
            if total_cells < 2:
                continue
            for k in range(2, total_cells + 1):
                assert sol.distanceSum(m, n, k) == _brute_force(m, n, k)