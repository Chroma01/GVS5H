class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(limit: int) -> bool:
            inf = n + 1
            first = int(s[0])

            dp = [[inf] * (limit + 1) for _ in range(2)]
            dp[first][1] = 0
            dp[1 - first][1] = 1

            for ch in s[1:]:
                target = int(ch)
                ndp = [[inf] * (limit + 1) for _ in range(2)]

                best0 = min(dp[0])
                best1 = min(dp[1])

                for bit in (0, 1):
                    cost = 0 if bit == target else 1
                    opposite_best = best1 if bit == 0 else best0

                    # Start a new run with the opposite character.
                    ndp[bit][1] = opposite_best + cost

                    # Extend an existing run of the same character.
                    for length in range(1, limit):
                        ndp[bit][length + 1] = dp[bit][length] + cost

                dp = ndp

            return min(min(dp[0]), min(dp[1])) <= numOps

        low, high = 1, n
        while low < high:
            mid = (low + high) // 2
            if feasible(mid):
                high = mid
            else:
                low = mid + 1

        return low