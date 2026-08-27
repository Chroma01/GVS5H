class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        # Special case m = 1
        if m == 1:
            # Only one possible array: all 1's
            # It has n-1 equal adjacent pairs, so k must be n-1
            return 1 if k == n - 1 else 0

        # Precompute factorials up to n (we need up to n-1 for combinations)
        size = n
        fact = [1] * (size + 1)
        for i in range(1, size + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (size + 1)
        inv_fact[size] = pow(fact[size], MOD - 2, MOD)
        for i in range(size, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(N, R):
            if R < 0 or R > N:
                return 0
            return fact[N] * inv_fact[R] % MOD * inv_fact[N - R] % MOD

        # Number of ways to choose the k "equal" positions among n-1 gaps
        choose = comb(n - 1, k)

        # First block: m choices, each subsequent block: m-1 choices (k of them)
        ways = m * pow(m - 1, k, MOD) % MOD
        result = choose * ways % MOD
        return result