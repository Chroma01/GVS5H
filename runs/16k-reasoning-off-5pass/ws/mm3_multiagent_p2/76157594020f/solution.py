class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        # Convert string to list of ints for speed
        a = [int(c) for c in s]
        
        # Binary search on L (1 to n)
        lo, hi = 1, n
        ans = n
        
        def feasible(L: int) -> bool:
            # dp[c][len] = min flips to reach state where last char is c and current run of c has length len
            INF = float('inf')
            # Initialize for first character
            dp0 = [INF] * (L + 1)  # dp for last char = 0
            dp1 = [INF] * (L + 1)  # dp for last char = 1
            
            # First character
            orig = a[0]
            # Keep it
            if orig == 0:
                dp0[1] = 0
            else:
                dp1[1] = 0
            # Flip it
            flipped = 1 - orig
            if flipped == 0:
                dp1[1] = min(dp1[1], 1)
            else:
                dp0[1] = min(dp0[1], 1)
            
            # Process remaining characters
            for i in range(1, n):
                orig = a[i]
                new_dp0 = [INF] * (L + 1)
                new_dp1 = [INF] * (L + 1)
                
                for c, dp in [(0, dp0), (1, dp1)]:
                    for length in range(1, L + 1):
                        cost = dp[length]
                        if cost == INF:
                            continue
                        # Option 1: don't flip
                        new_c = orig
                        if new_c == c:
                            new_length = length + 1
                            if new_length <= L:
                                if c == 0:
                                    if cost < new_dp0[new_length]:
                                        new_dp0[new_length] = cost
                                else:
                                    if cost < new_dp1[new_length]:
                                        new_dp1[new_length] = cost
                        else:
                            new_length = 1
                            if new_c == 0:
                                if cost < new_dp0[new_length]:
                                    new_dp0[new_length] = cost
                            else:
                                if cost < new_dp1[new_length]:
                                    new_dp1[new_length] = cost
                        
                        # Option 2: flip
                        new_c = 1 - orig
                        if new_c == c:
                            new_length = length + 1
                            if new_length <= L:
                                if c == 0:
                                    if cost + 1 < new_dp0[new_length]:
                                        new_dp0[new_length] = cost + 1
                                else:
                                    if cost + 1 < new_dp1[new_length]:
                                        new_dp1[new_length] = cost + 1
                        else:
                            new_length = 1
                            if new_c == 0:
                                if cost + 1 < new_dp0[new_length]:
                                    new_dp0[new_length] = cost + 1
                            else:
                                if cost + 1 < new_dp1[new_length]:
                                    new_dp1[new_length] = cost + 1
                
                dp0 = new_dp0
                dp1 = new_dp1
            
            # Find minimum cost in final states
            min_cost = INF
            for length in range(1, L + 1):
                if dp0[length] < min_cost:
                    min_cost = dp0[length]
                if dp1[length] < min_cost:
                    min_cost = dp1[length]
            return min_cost <= numOps
        
        # Binary search for smallest L
        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        
        return ans