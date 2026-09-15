class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        def modpow(a, e):
            r = 1
            a %= MOD
            while e:
                if e & 1:
                    r = r * a % MOD
                a = a * a % MOD
                e >>= 1
            return r

        # Precompute factorials / inverse factorials up to N.
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = modpow(fact[N], MOD - 2)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Each valid arrangement is a k-subset; a fixed cell pair appears in
        # C(N-2, k-2) arrangements.
        binom = comb(N - 2, k - 2)

        inv6 = modpow(6, MOD - 2)

        # Sum of |i-j| over unordered row pairs = m(m^2-1)/6; same for columns.
        row_pairs = (m % MOD) * ((m * m - 1) % MOD) % MOD * inv6 % MOD
        col_pairs = (n % MOD) * ((n * n - 1) % MOD) % MOD * inv6 % MOD

        # Row contribution weighted by n^2 column choices; column by m^2.
        S = (n % MOD) * (n % MOD) % MOD * row_pairs % MOD
        S = (S + (m % MOD) * (m % MOD) % MOD * col_pairs) % MOD

        return binom * S % MOD