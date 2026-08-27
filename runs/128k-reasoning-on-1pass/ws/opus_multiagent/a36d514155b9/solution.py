class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7

        def T(t):
            return (t * t * t - t) // 6

        S = ((n % MOD) * (n % MOD) % MOD) * (T(m) % MOD) % MOD
        S = (S + ((m % MOD) * (m % MOD) % MOD) * (T(n) % MOD)) % MOD

        N = m * n
        size = max(N, 2)
        fact = [1] * (size + 1)
        for i in range(1, size + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (size + 1)
        inv_fact[size] = pow(fact[size], MOD - 2, MOD)
        for i in range(size, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def nCr(a, b):
            if b < 0 or a < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        return S * nCr(N - 2, k - 2) % MOD