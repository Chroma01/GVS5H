class Solution:
    MOD = 1_000_000_007
    INV6 = 166666668
    _fact = [1]
    _invfact = [1]

    @classmethod
    def _ensure_factorials(cls, limit: int) -> None:
        current = len(cls._fact) - 1
        if limit <= current:
            return

        cls._fact.extend([1] * (limit - current))
        for i in range(current + 1, limit + 1):
            cls._fact[i] = (cls._fact[i - 1] * i) % cls.MOD

        cls._invfact = [1] * (limit + 1)
        cls._invfact[limit] = pow(cls._fact[limit], cls.MOD - 2, cls.MOD)
        for i in range(limit, 0, -1):
            cls._invfact[i - 1] = (cls._invfact[i] * i) % cls.MOD

    def distanceSum(self, m: int, n: int, k: int) -> int:
        if k < 2:
            return 0

        mod = self.MOD
        N = m * n
        self._ensure_factorials(N)

        fact = self._fact
        invfact = self._invfact

        def one_dim_sum(length: int) -> int:
            x = length % mod
            return (
                x
                * ((length - 1) % mod)
                % mod
                * ((length + 1) % mod)
                % mod
                * self.INV6
                % mod
            )

        row_part = ((n % mod) * (n % mod) % mod) * one_dim_sum(m) % mod
        col_part = ((m % mod) * (m % mod) % mod) * one_dim_sum(n) % mod
        total_cell_pairs = (row_part + col_part) % mod

        a = N - 2
        b = k - 2
        if b < 0 or b > a:
            ways = 0
        else:
            ways = fact[a] * invfact[b] % mod * invfact[a - b] % mod

        return total_cell_pairs * ways % mod


if __name__ == "__main__":
    sol = Solution()
    assert sol.distanceSum(2, 2, 2) == 8
    assert sol.distanceSum(1, 4, 3) == 20
    assert sol.distanceSum(1, 2, 2) == 1
    assert sol.distanceSum(2, 3, 6) == 25
    assert sol.distanceSum(3, 3, 2) == 72
    expected = (100000 * 99999 * 100001 // 6) % Solution.MOD
    assert sol.distanceSum(1, 100000, 100000) == expected