class Solution:
    MOD = 10**9 + 7
    _fact = [1]
    _invfact = [1]

    def _ensure_factorials(self, n: int) -> None:
        fact = Solution._fact
        invfact = Solution._invfact
        current = len(fact)

        if current > n:
            return

        fact.extend([1] * (n + 1 - current))
        for i in range(current, n + 1):
            fact[i] = fact[i - 1] * i % Solution.MOD

        invfact.extend([1] * (n + 1 - len(invfact)))
        invfact[n] = pow(fact[n], Solution.MOD - 2, Solution.MOD)

        for i in range(n, current - 1, -1):
            invfact[i - 1] = invfact[i] * i % Solution.MOD

    def _comb(self, n: int, r: int) -> int:
        if n < 0 or r < 0 or r > n:
            return 0

        self._ensure_factorials(n)
        mod = Solution.MOD

        return (
            Solution._fact[n]
            * Solution._invfact[r]
            % mod
            * Solution._invfact[n - r]
            % mod
        )

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        if k < 0 or k > n - 1:
            return 0

        mod = Solution.MOD

        ans = self._comb(n - 1, k)
        ans = ans * (m % mod) % mod
        ans = ans * pow((m - 1) % mod, n - 1 - k, mod) % mod

        return ans