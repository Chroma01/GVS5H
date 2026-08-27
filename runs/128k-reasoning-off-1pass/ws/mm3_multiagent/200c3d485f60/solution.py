class Solution:
    MOD = 10**9 + 7

    def _pow(self, base: int, exp: int, mod: int) -> int:
        """Fast modular exponentiation."""
        result = 1
        base %= mod
        while exp > 0:
            if exp & 1:
                result = (result * base) % mod
            base = (base * base) % mod
            exp >>= 1
        return result

    def _precompute_factorials(self, max_n: int):
        """Precompute factorials and inverse factorials up to max_n."""
        fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            fact[i] = (fact[i - 1] * i) % self.MOD
        inv_fact = [1] * (max_n + 1)
        # Fermat's little theorem for modular inverse since MOD is prime
        inv_fact[max_n] = self._pow(fact[max_n], self.MOD - 2, self.MOD)
        for i in range(max_n, 0, -1):
            inv_fact[i - 1] = (inv_fact[i] * i) % self.MOD
        return fact, inv_fact

    def _nCr(self, n: int, r: int, fact, inv_fact) -> int:
        """Compute binomial coefficient C(n, r) modulo MOD."""
        if r < 0 or r > n:
            return 0
        return (fact[n] * inv_fact[r] % self.MOD) * inv_fact[n - r] % self.MOD

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        # Edge cases
        if n == 1:
            # Only one element, no adjacent pairs, so k must be 0
            return m % self.MOD if k == 0 else 0

        # If k > n-1, impossible
        if k > n - 1:
            return 0

        # If m == 1, all elements must be 1, so only array is [1,1,...,1]
        # This has k = n-1 equal adjacent pairs
        if m == 1:
            return 1 if k == n - 1 else 0

        # General formula: C(n-1, k) * m * (m-1)^(n-k-1) mod MOD
        max_n = n
        fact, inv_fact = self._precompute_factorials(max_n)

        comb = self._nCr(n - 1, k, fact, inv_fact)
        power_exp = n - k - 1
        power_val = self._pow(m - 1, power_exp, self.MOD)

        result = (comb * m) % self.MOD
        result = (result * power_val) % self.MOD
        return result