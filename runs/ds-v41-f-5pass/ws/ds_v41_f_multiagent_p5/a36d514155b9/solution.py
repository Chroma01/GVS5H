class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        # Precompute factorials and inverse factorials up to N
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

        # Each fixed unordered pair of cells is contained in C(N-2, k-2) arrangements
        pair_count = comb(N - 2, k - 2)

        # A(L) = sum over unordered index pairs of |i-j| = L(L-1)(L+1)/6
        inv6 = pow(6, MOD - 2, MOD)

        def A(L):
            return (L % MOD) * ((L - 1) % MOD) % MOD * ((L + 1) % MOD) % MOD * inv6 % MOD

        # Row differences: n*n cell pairs per row-index pair
        # Column differences: m*m cell pairs per column-index pair
        S = (n * n % MOD) * A(m) % MOD
        S = (S + (m * m % MOD) * A(n)) % MOD

        return S * pair_count % MOD