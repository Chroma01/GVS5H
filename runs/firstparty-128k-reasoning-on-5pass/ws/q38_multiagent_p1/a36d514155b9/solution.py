class Solution:
    MOD = 10**9 + 7
    INV6 = pow(6, MOD - 2, MOD)
    MAXN = 100000
    _fact = None
    _invfact = None
    _max = -1

    def _ensure_fact(self, limit: int) -> None:
        if Solution._max >= limit:
            return
        old = Solution._max
        if old < 0:
            limit = max(limit, Solution.MAXN)
            fact = [1] * (limit + 1)
            for i in range(1, limit + 1):
                fact[i] = fact[i - 1] * i % Solution.MOD
            invfact = [1] * (limit + 1)
            invfact[limit] = pow(fact[limit], Solution.MOD - 2, Solution.MOD)
            for i in range(limit, 0, -1):
                invfact[i - 1] = invfact[i] * i % Solution.MOD
            Solution._fact = fact
            Solution._invfact = invfact
            Solution._max = limit
        else:
            fact = Solution._fact
            invfact = Solution._invfact
            fact.extend([1] * (limit - old))
            for i in range(old + 1, limit + 1):
                fact[i] = fact[i - 1] * i % Solution.MOD
            invfact.extend([1] * (limit - old))
            invfact[limit] = pow(fact[limit], Solution.MOD - 2, Solution.MOD)
            for i in range(limit, old, -1):
                invfact[i - 1] = invfact[i] * i % Solution.MOD
            Solution._max = limit

    def _comb(self, N: int, R: int) -> int:
        if N < 0 or R < 0 or R > N:
            return 0
        self._ensure_fact(N)
        fact = Solution._fact
        invfact = Solution._invfact
        return fact[N] * invfact[R] % Solution.MOD * invfact[N - R] % Solution.MOD

    def distanceSum(self, m: int, n: int, k: int) -> int:
        N = m * n
        arrangements_factor = self._comb(N - 2, k - 2)

        m_mod = m % Solution.MOD
        n_mod = n % Solution.MOD

        row_pair_sum = m_mod * ((m_mod * m_mod - 1) % Solution.MOD) % Solution.MOD
        row_pair_sum = row_pair_sum * Solution.INV6 % Solution.MOD

        col_pair_sum = n_mod * ((n_mod * n_mod - 1) % Solution.MOD) % Solution.MOD
        col_pair_sum = col_pair_sum * Solution.INV6 % Solution.MOD

        total_pair_distance = (
            (n_mod * n_mod % Solution.MOD) * row_pair_sum
            + (m_mod * m_mod % Solution.MOD) * col_pair_sum
        ) % Solution.MOD

        return arrangements_factor * total_pair_distance % Solution.MOD