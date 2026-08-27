class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        # Input validation: k must be a valid number of equal adjacencies
        if k < 0 or k > n - 1:
            return 0

        # Precompute factorials and inverse factorials up to n
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (n + 1)
        # Fermat's little theorem gives modular inverse because MOD is prime
        inv_fact[n] = pow(fact[n], MOD - 2, MOD)
        for i in range(n, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        # Binomial coefficient C(n-1, k)
        binom = fact[n - 1] * inv_fact[k] % MOD * inv_fact[n - 1 - k] % MOD

        # First run: any of the m values
        term1 = m % MOD

        # Remaining runs: each must differ from the previous one
        exp = n - k - 1
        term2 = pow((m - 1) % MOD, exp, MOD)

        # Combine everything
        answer = binom * term1 % MOD * term2 % MOD
        return answer