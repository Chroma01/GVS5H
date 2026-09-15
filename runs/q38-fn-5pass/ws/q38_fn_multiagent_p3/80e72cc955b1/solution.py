from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        max_r = 0
        for _, r in queries:
            if r > max_r:
                max_r = r

        # powers[i] = 4^i. Ensure there is a power strictly greater than max_r.
        powers = [1]
        while powers[-1] <= max_r:
            powers.append(powers[-1] * 4)

        def prefix(n: int) -> int:
            """Return sum_{x=1}^n f(x), where f(x) is divisions by 4 needed to reach 0."""
            if n <= 0:
                return 0

            total = 0
            # For block i (0-based), f(x) = i + 1 on [4^i, 4^(i+1) - 1].
            for i in range(len(powers) - 1):
                start = powers[i]
                if start > n:
                    break

                end = powers[i + 1] - 1
                if end > n:
                    end = n

                total += (i + 1) * (end - start + 1)

            return total

        ans = 0
        for l, r in queries:
            steps = prefix(r) - prefix(l - 1)
            ans += (steps + 1) // 2

        return ans