class Solution:
    MOD = 10**9 + 7

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = self.MOD
        # factorials and inverse factorials up to n-1
        fact = [1] * n
        for i in range(1, n):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * n
        if n > 1:
            inv_fact[n - 1] = pow(fact[n - 1], MOD - 2, MOD)
            for i in range(n - 2, -1, -1):
                inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # choose which k of the n-1 boundaries are equal,
        # first element: m choices, each "different" boundary: (m-1) choices
        return comb(n - 1, k) * m % MOD * pow(m - 1, n - 1 - k, MOD) % MOD