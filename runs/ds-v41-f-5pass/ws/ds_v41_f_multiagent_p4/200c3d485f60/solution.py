class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        if k < 0 or k > n - 1:
            return 0

        # Precompute factorials and inverse factorials up to n.
        N = n
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Choose which k of the n-1 adjacent pairs are equal.
        # Remaining n-1-k adjacencies are changes => n-k runs.
        # First run: m choices; each of the other n-1-k runs: (m-1) choices.
        return comb(n - 1, k) * m % MOD * pow(m - 1, n - 1 - k, MOD) % MOD