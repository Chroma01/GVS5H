class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        # Precompute factorials and inverse factorials up to n - 1
        # (size at least 1 to handle n = 1)
        size = max(n, 1)
        fact = [1] * size
        for i in range(1, size):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * size
        inv_fact[size - 1] = pow(fact[size - 1], MOD - 2, MOD)
        for i in range(size - 2, -1, -1):
            inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

        # C(n - 1, k)
        comb = fact[n - 1] * inv_fact[k] % MOD * inv_fact[n - 1 - k] % MOD

        # m choices for first run, (m - 1) for each of the remaining n - k - 1 runs.
        # pow(0, 0, MOD) == 1 handles m = 1, k = n - 1 correctly.
        return comb * m % MOD * pow(m - 1, n - k - 1, MOD) % MOD