class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n <= 1:
            return 1

        bits = [1 if ch == '1' else 0 for ch in s]
        INF = 10**9

        def feasible(limit: int) -> bool:
            """
            Returns True iff we can make every final run length <= limit
            using at most numOps flips.
            """
            if limit >= n:
                return True

            # dp0[r] = minimum flips for processed prefix ending with '0'
            #          and current run length r.
            # dp1[r] = same, ending with '1'.
            # Index 0 is unused and kept as INF.
            dp0 = [INF] * (limit + 1)
            dp1 = [INF] * (limit + 1)

            if bits[0] == 0:
                dp0[1] = 0
                dp1[1] = 1
            else:
                dp0[1] = 1
                dp1[1] = 0

            for i in range(1, n):
                min0 = min(dp0)
                min1 = min(dp1)

                # Costs never decrease, so if both are already too expensive,
                # this prefix can never lead to a feasible full string.
                if min0 > numOps and min1 > numOps:
                    return False

                x = bits[i]

                # Cost to write final bit 0 or 1 at this position.
                cost0 = x          # original 1 -> final 0 costs 1
                cost1 = 1 - x      # original 0 -> final 1 costs 1

                # Switch to the opposite character: run length resets to 1.
                switch0 = min1 + cost0
                switch1 = min0 + cost1

                if limit == 1:
                    # Cannot extend any run; must alternate.
                    dp0 = [INF, switch0]
                    dp1 = [INF, switch1]
                else:
                    # Extend existing runs of length 1..limit-1 by one.
                    # Runs of length limit cannot be extended.
                    dp0 = [INF, switch0] + [v + cost0 for v in dp0[1:limit]]
                    dp1 = [INF, switch1] + [v + cost1 for v in dp1[1:limit]]

            return min(min(dp0), min(dp1)) <= numOps

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo