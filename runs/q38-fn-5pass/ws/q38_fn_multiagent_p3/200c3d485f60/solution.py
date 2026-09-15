class Solution:
    MOD = 10**9 + 7
    _fact = [1]
    _invfact = [1]

    def _ensure_factorials(self, n: int) -> None:
        fact = Solution._fact
        invfact = Solution._invfact
        mod = Solution.MOD

        current = len(fact) - 1
        if n <= current:
            return

        fact.extend([1] * (n - current))
        invfact.extend([1] * (n - current))

        for i in range(current + 1, n + 1):
            fact[i] = fact[i - 1] * i % mod

        invfact[n] = pow(fact[n], mod - 2, mod)
        for i in range(n, current, -1):
            invfact[i - 1] = invfact[i] * i % mod

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        if k < 0 or k > n - 1:
            return 0

        mod = Solution.MOD
        transitions = n - 1

        self._ensure_factorials(transitions)

        fact = Solution._fact
        invfact = Solution._invfact

        comb = fact[transitions] * invfact[k] % mod
        comb = comb * invfact[transitions - k] % mod

        return (m % mod) * comb % mod * pow(m - 1, transitions - k, mod) % mod