class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(limit: int) -> bool:
            inf = n + numOps + 1

            # dp[bit][run] = minimum flips after processing the prefix,
            # ending with `bit` repeated `run` times.
            dp = [[inf] * (limit + 1) for _ in range(2)]

            first = int(s[0])
            dp[first][1] = 0
            dp[1 - first][1] = 1

            for i in range(1, n):
                current = int(s[i])
                ndp = [[inf] * (limit + 1) for _ in range(2)]

                best0 = min(dp[0])
                best1 = min(dp[1])

                cost0 = 0 if current == 0 else 1
                cost1 = 0 if current == 1 else 1

                # Start a new run with the opposite bit.
                ndp[0][1] = min(ndp[0][1], best1 + cost0)
                ndp[1][1] = min(ndp[1][1], best0 + cost1)

                # Extend the current run.
                for bit, cost in ((0, cost0), (1, cost1)):
                    for run in range(1, limit):
                        if dp[bit][run] != inf:
                            ndp[bit][run + 1] = min(
                                ndp[bit][run + 1],
                                dp[bit][run] + cost
                            )

                dp = ndp

            return min(min(dp[0]), min(dp[1])) <= numOps

        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if feasible(mid):
                right = mid
            else:
                left = mid + 1

        return left