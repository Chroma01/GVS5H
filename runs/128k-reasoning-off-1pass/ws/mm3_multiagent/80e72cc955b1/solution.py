from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4: 4^0, 4^1, ..., 4^15 (since 4^15 = 2^30 ≈ 1e9, 4^16 > 1e9)
        powers = [1]
        while powers[-1] <= 10**9:
            powers.append(powers[-1] * 4)
        # powers[k] = 4^k, powers has size such that powers[K-1] <= n < powers[K]

        def sum_levels(n: int) -> int:
            """
            Return total sum of level(x) for x in [1, n].
            level(x) = floor(log4(x)) + 1, i.e., the number of times to floor-divide by 4 to reach 0.
            For x = 0, level(0) = 0.
            """
            if n <= 0:
                return 0

            # Find K such that 4^(K-1) <= n < 4^K, with K >= 1
            # Equivalently, K = floor(log4(n)) + 1
            # We use the precomputed powers list.
            K = 0
            while K + 1 < len(powers) and powers[K + 1] <= n:
                K += 1
            # Now powers[K-1] <= n < powers[K]  (with powers[0]=1, so K >= 1)
            # Actually after the loop, K is the smallest index such that powers[K] > n,
            # meaning n < powers[K] and n >= powers[K-1] (for K>=1).
            # So K = floor(log4(n)) + 1.

            # Full blocks for k = 0, 1, ..., K-2
            # A block of size 4^k has level distribution:
            #   - 1 number with level 1 (the first number, value 4^k? Wait, let's re-derive.)
            #
            # The range [4^k, 4^{k+1} - 1] contains 4^k numbers.
            # Among them, those divisible by 4 (but not 4^2) have level k+2? Let's think carefully.
            #
            # Actually, level(x) is 1 + floor(log4(x)) for x >= 1.
            # For x in [4^k, 4^{k+1} - 1], floor(log4(x)) = k, so level(x) = k+1.
            # There are 4^{k+1} - 4^k = 3 * 4^k numbers in this range.
            # But x = 0 has level 0; x in [1, 3] has level 1 (3 numbers);
            # x in [4, 15] has level 2 (12 numbers);
            # x in [16, 63] has level 3 (48 numbers);
            # So the count of numbers with level (k+1) is 3 * 4^k for k >= 0.
            # Sum of levels for level-(k+1) numbers: (k+1) * 3 * 4^k.
            #
            # For n, we sum over full levels and then a partial top level.
            #
            # Full levels covered: levels 1, 2, ..., K-1, each with 3*4^(k-1) numbers (where k = level-1).
            # The remaining numbers are in [4^(K-1), n], all having level K.
            # Count of remaining: n - 4^(K-1) + 1.
            # Sum from full levels: sum_{k=0}^{K-2} (k+1) * 3 * 4^k
            # Plus: K * (n - powers[K-1] + 1)

            total = 0
            # Sum for full levels 1 to K-1
            for k in range(K - 1):  # k = 0, 1, ..., K-2  =>  level = k+1 ranges 1 to K-1
                total += (k + 1) * 3 * powers[k]

            # Partial top level
            total += K * (n - powers[K - 1] + 1)

            return total

        result = 0
        for l, r in queries:
            total_levels = sum_levels(r) - sum_levels(l - 1)
            result += (total_levels + 1) // 2

        return result