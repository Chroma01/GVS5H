class Solution:
    MOD = 10**9 + 7
    _fact = {}
    _inv_fact = {}

    def _precompute(self, N):
        if N in self._fact:
            return
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i-1] * i % self.MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], self.MOD - 2, self.MOD)
        for i in range(N, 0, -1):
            inv_fact[i-1] = inv_fact[i] * i % self.MOD
        self._fact[N] = fact
        self._inv_fact[N] = inv_fact

    def _C(self, N, a, b):
        if b < 0 or b > a:
            return 0
        self._precompute(N)
        return self._fact[N][a] * self._inv_fact[N][b] % self.MOD * self._inv_fact[N][a-b] % self.MOD

    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = self.MOD
        total = m * n
        binom = self._C(total, total - 2, k - 2)
        inv6 = pow(6, MOD - 2, MOD)
        U = total % MOD * (m + n) % MOD * (total - 1) % MOD * inv6 % MOD
        return binom * U % MOD