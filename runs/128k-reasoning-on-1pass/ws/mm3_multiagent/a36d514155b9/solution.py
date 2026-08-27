import sys

MOD = 10**9 + 7
INV6 = pow(6, MOD - 2, MOD)          # modular inverse of 6

class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        N = m * n                     # total number of cells ( ≤ 10^5 )

        # ---------- pre‑compute factorials ----------
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        # ---------- binomial coefficient C(N‑2, k‑2) ----------
        # Constraints guarantee 0 ≤ k‑2 ≤ N‑2
        comb = (fact[N - 2] *
                inv_fact[k - 2] % MOD *
                inv_fact[N - k]) % MOD

        # ---------- compute T (sum of distances over all cell pairs) ----------
        m_mod = m % MOD
        n_mod = n % MOD

        # row term: n^2 * m * (m-1) * (m+1) / 6
        term1 = n_mod * n_mod % MOD
        term1 = term1 * m_mod % MOD
        term1 = term1 * ((m_mod - 1) % MOD) % MOD
        term1 = term1 * ((m_mod + 1) % MOD) % MOD
        term1 = term1 * INV6 % MOD

        # column term: m^2 * n * (n-1) * (n+1) / 6
        term2 = m_mod * m_mod % MOD
        term2 = term2 * n_mod % MOD
        term2 = term2 * ((n_mod - 1) % MOD) % MOD
        term2 = term2 * ((n_mod + 1) % MOD) % MOD
        term2 = term2 * INV6 % MOD

        T = (term1 + term2) % MOD

        # ---------- final answer ----------
        return T * comb % MOD