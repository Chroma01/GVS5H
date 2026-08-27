class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        # Factorials and inverse factorials up to N for binomial coefficients
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        invfact = [1] * (N + 1)
        invfact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

        inv6 = pow(6, MOD - 2, MOD)

        # f(L) = sum_{0 <= i < j < L} (j - i) = L * (L^2 - 1) / 6  (mod MOD)
        def f(L: int) -> int:
            return L % MOD * ((L * L - 1) % MOD) % MOD * inv6 % MOD

        # Sum of Manhattan distances over all unordered pairs of cells:
        # row part: n^2 * f(m), column part: m^2 * f(n)
        S = (n * n % MOD * f(m) + m * m % MOD * f(n)) % MOD

        # Each pair of cells co-occurs in C(N-2, k-2) arrangements
        return comb(N - 2, k - 2) * S % MOD