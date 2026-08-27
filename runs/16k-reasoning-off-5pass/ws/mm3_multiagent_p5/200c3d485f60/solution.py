class Solution:
    MOD = 10**9 + 7
    _fact = None
    _inv_fact = None
    _max_n = 0

    def _precompute(self, n):
        """Precompute factorials and inverse factorials up to n."""
        if self._fact is not None and self._max_n >= n:
            return
        self._fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self._fact[i] = self._fact[i - 1] * i % self.MOD
        self._inv_fact = [1] * (n + 1)
        # Fermat's little theorem: a^(p-2) mod p
        self._inv_fact[n] = pow(self._fact[n], self.MOD - 2, self.MOD)
        for i in range(n, 0, -1):
            self._inv_fact[i - 1] = self._inv_fact[i] * i % self.MOD
        self._max_n = n

    def _comb(self, n, r):
        if r < 0 or r > n:
            return 0
        return self._fact[n] * self._inv_fact[r] % self.MOD * self._inv_fact[n - r] % self.MOD

    def _pow(self, base, exp):
        result = 1
        base %= self.MOD
        while exp > 0:
            if exp & 1:
                result = result * base % self.MOD
            base = base * base % self.MOD
            exp >>= 1
        return result

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        # Edge cases
        if k > n - 1 or k < 0:
            return 0
        # Special case m == 1
        if m == 1:
            return 1 if k == n - 1 else 0

        # Precompute up to n-1
        self._precompute(n)

        # Formula: m * C(n-1, k) * (m-1)^(n-1-k) mod MOD
        comb = self._comb(n - 1, k)
        power = self._pow(m - 1, n - 1 - k)

        return m % self.MOD * comb % self.MOD * power % self.MOD