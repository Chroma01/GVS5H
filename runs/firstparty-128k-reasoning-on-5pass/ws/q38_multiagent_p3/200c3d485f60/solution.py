class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        # There are n - 1 adjacent pairs. If k is outside the valid range,
        # no array can satisfy the condition.
        if k < 0 or k > n - 1:
            return 0

        # Precompute factorials and inverse factorials up to n - 1.
        max_fact = n - 1
        fact = [1] * (max_fact + 1)
        for i in range(1, max_fact + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (max_fact + 1)
        inv_fact[max_fact] = pow(fact[max_fact], MOD - 2, MOD)
        for i in range(max_fact, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Choose which k of the n - 1 adjacent pairs are equal.
        ans = comb(n - 1, k)

        # The chosen equal pairs split the array into n - k runs.
        # The first run can be any of m values, and each later run must
        # differ from the previous run, giving m - 1 choices.
        ans = ans * (m % MOD) % MOD
        ans = ans * pow((m - 1) % MOD, n - k - 1, MOD) % MOD

        return ans