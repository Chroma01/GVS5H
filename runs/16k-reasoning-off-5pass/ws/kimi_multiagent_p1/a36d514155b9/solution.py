class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        # Factorials and inverse factorials up to N for computing C(N-2, k-2)
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        c = comb(N - 2, k - 2)

        # Sum of |r1 - r2| over unordered row pairs = (m^3 - m) / 6
        # Row contribution: n^2 * (m^3 - m) / 6
        # Column contribution: m^2 * (n^3 - n) / 6
        inv6 = pow(6, MOD - 2, MOD)
        row_part = (n % MOD) * (n % MOD) % MOD * ((pow(m, 3, MOD) - m) % MOD) % MOD
        col_part = (m % MOD) * (m % MOD) % MOD * ((pow(n, 3, MOD) - n) % MOD) % MOD

        return c * ((row_part + col_part) % MOD) % MOD * inv6 % MOD