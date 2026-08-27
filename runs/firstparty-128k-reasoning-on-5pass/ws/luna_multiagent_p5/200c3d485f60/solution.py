class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        transitions = n - 1
        different = transitions - k

        factorial = [1] * (transitions + 1)
        for i in range(1, transitions + 1):
            factorial[i] = factorial[i - 1] * i % MOD

        inverse_factorial = [1] * (transitions + 1)
        inverse_factorial[transitions] = pow(
            factorial[transitions], MOD - 2, MOD
        )
        for i in range(transitions, 0, -1):
            inverse_factorial[i - 1] = inverse_factorial[i] * i % MOD

        combinations = (
            factorial[transitions]
            * inverse_factorial[k]
            % MOD
            * inverse_factorial[transitions - k]
            % MOD
        )

        return (
            m
            % MOD
            * combinations
            % MOD
            * pow((m - 1) % MOD, different, MOD)
            % MOD
        )