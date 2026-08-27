class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 1_000_000_007

        factorial = [1] * n
        for i in range(1, n):
            factorial[i] = factorial[i - 1] * i % MOD

        inverse_factorial = [1] * n
        inverse_factorial[n - 1] = pow(factorial[n - 1], MOD - 2, MOD)
        for i in range(n - 1, 0, -1):
            inverse_factorial[i - 1] = inverse_factorial[i] * i % MOD

        combinations = (
            factorial[n - 1]
            * inverse_factorial[k]
            % MOD
            * inverse_factorial[n - 1 - k]
            % MOD
        )

        unequal_transitions = n - 1 - k
        return (
            m
            * combinations
            % MOD
            * pow(m - 1, unequal_transitions, MOD)
            % MOD
        )