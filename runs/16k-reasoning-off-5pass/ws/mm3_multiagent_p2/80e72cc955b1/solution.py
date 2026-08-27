from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4 and prefix sums of f(i) for i up to 10^9.
        # f(i) = number of base-4 digits of i, i.e., floor(log4(i)) + 1 for i >= 1.
        # S(x) = sum_{i=1}^{x} f(i) for x >= 0 (with S(0) = 0).
        # We use the closed form:
        # Let K = floor(log4(x)) + 1 (the number of base-4 digits of x).
        # Then S(x) = sum_{k=1}^{K-1} k * (4^k - 4^{k-1}) + K * (x - 4^{K-1} + 1).
        # The sum part can be precomputed once for all K up to 16 (since 4^15 > 10^9).

        # Maximum exponent we need: 4^15 = 1073741824 > 1e9, so up to 4^15.
        # We store powers[0] = 1, powers[1] = 4, ..., powers[15] = 4^15.
        powers = [1]
        for _ in range(15):
            powers.append(powers[-1] * 4)

        # Precompute pref[k] = sum_{j=1}^{k} j * (4^j - 4^{j-1}) for k = 0..15.
        # Note: pref[0] = 0 (empty sum).
        pref = [0]  # pref[0] = 0
        for k in range(1, 16):
            # contribution for this k:
            contrib = k * (powers[k] - powers[k-1])
            pref.append(pref[-1] + contrib)

        def S(x: int) -> int:
            """Return sum_{i=1}^{x} f(i) where f(i) is number of base-4 digits of i.
            For x == 0, returns 0.
            """
            if x <= 0:
                return 0
            # Find K = number of base-4 digits of x = floor(log4(x)) + 1.
            # We find the largest k such that 4^{k-1} <= x, i.e., k-1 <= log4(x).
            # Using precomputed powers: 4^{k-1} <= x < 4^k.
            # We can binary search or just linear scan since K <= 16.
            # Linear scan is fast enough.
            K = 1
            while K < 16 and powers[K] <= x:
                K += 1
            # After loop, powers[K-1] <= x < powers[K], so K is correct.
            # S(x) = pref[K-1] + K * (x - powers[K-1] + 1)
            return pref[K-1] + K * (x - powers[K-1] + 1)

        total = 0
        for l, r in queries:
            # sum_{i=l}^{r} f(i) = S(r) - S(l-1)
            T = S(r) - S(l - 1)
            # Minimum operations = ceil(T / 2) = (T + 1) // 2
            total += (T + 1) // 2

        return total