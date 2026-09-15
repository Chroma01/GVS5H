class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 1_000_000_007
        transitions = n - 1

        if k < 0 or k > transitions:
            return 0

        # Compute C(transitions, k) modulo MOD.
        # Use the smaller of k and transitions-k to minimize the loop.
        r = min(k, transitions - k)
        num = 1
        den = 1

        for i in range(1, r + 1):
            num = (num * (transitions - r + i)) % MOD
            den = (den * i) % MOD

        comb = num * pow(den, MOD - 2, MOD) % MOD

        # For each valid pattern:
        # - first element: m choices
        # - each equal transition: 1 choice
        # - each unequal transition: m - 1 choices
        return comb * (m % MOD) % MOD * pow((m - 1) % MOD, transitions - k, MOD) % MOD