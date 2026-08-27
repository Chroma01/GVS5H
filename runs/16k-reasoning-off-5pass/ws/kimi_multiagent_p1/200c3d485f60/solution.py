class Solution:
    MOD = 10**9 + 7
    MAX = 10**5
    _fact = None
    _inv_fact = None

    @classmethod
    def _precompute(cls):
        if cls._fact is None:
            fact = [1] * (cls.MAX + 1)
            for i in range(1, cls.MAX + 1):
                fact[i] = fact[i - 1] * i % cls.MOD
            inv_fact = [1] * (cls.MAX + 1)
            inv_fact[cls.MAX] = pow(fact[cls.MAX], cls.MOD - 2, cls.MOD)
            for i in range(cls.MAX, 0, -1):
                inv_fact[i - 1] = inv_fact[i] * i % cls.MOD
            cls._fact = fact
            cls._inv_fact = inv_fact

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = self.MOD
        self._precompute()
        fact = self._fact
        inv_fact = self._inv_fact

        # C(n-1, k)
        a = n - 1
        comb = fact[a] * inv_fact[k] % MOD * inv_fact[a - k] % MOD

        # m * C(n-1, k) * (m-1)^(n-1-k)
        return m % MOD * comb % MOD * pow(m - 1, n - 1 - k, MOD) % MOD