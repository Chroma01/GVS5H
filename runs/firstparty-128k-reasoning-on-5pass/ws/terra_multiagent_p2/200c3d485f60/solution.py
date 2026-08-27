class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 1_000_000_007

        # Choose which k of the n - 1 transitions are equal.
        total_transitions = n - 1

        factorial = [1] * (total_transitions + 1)
        for i in range(1, total_transitions + 1):
            factorial[i] = factorial[i - 1] * i % MOD

        inv_factorial = [1] * (total_transitions + 1)
        inv_factorial[total_transitions] = pow(
            factorial[total_transitions], MOD - 2, MOD
        )
        for i in range(total_transitions, 0, -1):
            inv_factorial[i - 1] = inv_factorial[i] * i % MOD

        combinations = (
            factorial[total_transitions]
            * inv_factorial[k]
            % MOD
            * inv_factorial[total_transitions - k]
            % MOD
        )

        differing_transitions = total_transitions - k
        return (
            m
            * combinations
            % MOD
            * pow(m - 1, differing_transitions, MOD)
            % MOD
        )