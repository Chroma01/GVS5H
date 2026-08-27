class Solution:
    MOD = 1_000_000_007
    _fact = [1]
    _invfact = [1]
    _max = 0

    @classmethod
    def _ensure_factorials(cls, limit: int) -> None:
        if limit <= cls._max:
            return

        old = cls._max
        cls._fact.extend([1] * (limit - old))
        for i in range(old + 1, limit + 1):
            cls._fact[i] = (cls._fact[i - 1] * i) % cls.MOD

        cls._invfact.extend([1] * (limit - old))
        cls._invfact[limit] = pow(cls._fact[limit], cls.MOD - 2, cls.MOD)
        for i in range(limit, old, -1):
            cls._invfact[i - 1] = (cls._invfact[i] * i) % cls.MOD

        cls._max = limit

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        gaps = n - 1
        if k < 0 or k > gaps:
            return 0

        if m == 1:
            return 1 if k == gaps else 0

        self._ensure_factorials(gaps)

        comb = self._fact[gaps]
        comb = (comb * self._invfact[k]) % self.MOD
        comb = (comb * self._invfact[gaps - k]) % self.MOD

        ans = (comb * (m % self.MOD)) % self.MOD
        ans = (ans * pow((m - 1) % self.MOD, gaps - k, self.MOD)) % self.MOD
        return ans


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ((3, 2, 1), 4),
        ((4, 2, 2), 6),
        ((5, 2, 0), 2),
        ((1, 1, 0), 1),
        ((1, 5, 0), 5),
        ((2, 1, 0), 0),
        ((2, 1, 1), 1),
        ((3, 1, 2), 1),
        ((3, 1, 1), 0),
        ((2, 3, 0), 6),
        ((2, 3, 1), 3),
        ((3, 3, 1), 12),
        ((100000, 1, 99999), 1),
        ((100000, 1, 0), 0),
        ((100000, 100000, 99999), 100000),
    ]

    for args, expected in cases:
        got = sol.countGoodArrays(*args)
        assert got == expected, (args, got, expected)

    print("All tests passed")