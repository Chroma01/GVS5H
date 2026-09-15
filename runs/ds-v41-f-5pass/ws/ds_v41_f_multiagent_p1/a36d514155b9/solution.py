class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        # S(L) = sum over unordered pairs of 1D positions {i,j} of |i-j|
        #      = sum_{d=1}^{L-1} d*(L-d) = L(L-1)(L+1)/6, exact integer.
        def S(L):
            return L * (L - 1) * (L + 1) // 6

        # Total Manhattan distance over all unordered cell pairs.
        # Row contribution: pick two rows (n^2 column assignments), weighted by S(m).
        # Column contribution: pick two columns (m^2 row assignments), weighted by S(n).
        D = (pow(n, 2, MOD) * (S(m) % MOD) + pow(m, 2, MOD) * (S(n) % MOD)) % MOD

        # Each fixed unordered pair of cells appears together in C(N-2, k-2) arrangements.
        top = N - 2
        r = k - 2
        if r < 0 or r > top:
            return 0

        fact = [1] * (top + 1)
        for i in range(1, top + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (top + 1)
        inv_fact[top] = pow(fact[top], MOD - 2, MOD)
        for i in range(top, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        c = fact[top] * inv_fact[r] % MOD * inv_fact[top - r] % MOD
        return c * D % MOD