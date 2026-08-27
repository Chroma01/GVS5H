class Solution:
    MOD = 10**9 + 7

    def _comb(self, N: int, R: int) -> int:
        if R < 0 or R > N:
            return 0

        MOD = self.MOD
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        invfact = [1] * (N + 1)
        invfact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD

        return fact[N] * invfact[R] % MOD * invfact[N - R] % MOD

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        if n <= 0:
            return 0
        if k < 0 or k > n - 1:
            return 0
        if m <= 0:
            return 0

        if m == 1:
            return 1 if k == n - 1 else 0

        MOD = self.MOD
        ways_to_choose_equal_edges = self._comb(n - 1, k)
        ways_to_color_runs = (m % MOD) * pow((m - 1) % MOD, n - k - 1, MOD) % MOD

        return ways_to_choose_equal_edges * ways_to_color_runs % MOD