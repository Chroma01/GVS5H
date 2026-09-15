class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        # Factorials and inverse factorials up to N (N <= 1e5).
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a, b):
            if b < 0 or b > a or a < 0:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        inv6 = pow(6, MOD - 2, MOD)

        # T(L) = sum_{0 <= r < s < L} (s - r) = L(L-1)(L+1)/6
        def T(L):
            return L % MOD * ((L - 1) % MOD) % MOD * ((L + 1) % MOD) % MOD * inv6 % MOD

        # Every unordered pair of cells appears in exactly C(N-2, k-2) arrangements.
        ways = comb(N - 2, k - 2)

        # Vertical contribution: for each pair of distinct rows (with n^2 cell pairs),
        # sum of row differences over that row pair. Symmetric for columns.
        total = (n % MOD) * (n % MOD) % MOD * T(m) % MOD
        total = (total + (m % MOD) * (m % MOD) % MOD * T(n)) % MOD

        return ways * total % MOD