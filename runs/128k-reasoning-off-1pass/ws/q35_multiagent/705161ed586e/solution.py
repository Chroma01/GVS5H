class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        INF = float('inf')
        
        # Precompute prefix sums for each character
        # P[c][i] = sum of abs(ord(caption[j]) - ord(c)) for j in 0..i-1
        P = [[0] * (n + 1) for _ in range(26)]
        for c in range(26):
            char_c = chr(ord('a') + c)
            for i in range(n):
                P[c][i + 1] = P[c][i] + abs(ord(caption[i]) - ord(char_c))
        
        # dp[i][c] = min cost to make prefix of length i valid, ending with character c
        dp = [[INF] * 26 for _ in range(n + 1)]
        # parent[i][c] = (l, c_prev) that achieved the minimum, where l is start index of current group
        parent = [[None] * 26 for _ in range(n + 1)]
        
        # Base case: dp[0][c] = 0 for all c
        for c in range(26):
            dp[0][c] = 0
        
        # min1[i], char1[i], min2[i] for each position i
        min1 = [INF] * (n + 1)
        char1 = [-1] * (n + 1)
        min2 = [INF] * (n + 1)
        
        # Initialize for i=0
        min1[0] = 0
        char1[0] = 0  # arbitrary
        min2[0] = INF
        
        # running_min[c] stores min over l from 0 to current_l of (min_prev(l, c) - P[c][l])
        # where min_prev(l, c) = min1[l] if char1[l] != c else min2[l]
        running_min = [INF] * 26
        
        for i in range(1, n + 1):
            # Update running_min with l = i-3 (if valid)
            if i >= 3:
                l = i - 3
                for c in range(26):
                    # min_prev for character c at position l
                    if char1[l] != c:
                        min_prev = min1[l]
                    else:
                        min_prev = min2[l]
                    if min_prev != INF:
                        val = min_prev - P[c][l]
                        if val < running_min[c]:
                            running_min[c] = val
            
            # Compute dp[i][c] for each c
            for c in range(26):
                if running_min[c] != INF:
                    cost = running_min[c] + P[c][i]
                    if cost < dp[i][c]:
                        dp[i][c] = cost
                        # We need to find the l that achieved running_min[c]
                        # But running_min is a running min, so we don't know l directly.
                        # Instead, we iterate l from i-3 down to 0 to find the best l for reconstruction.
                        # This is O(n) per state, making total O(n^2 * 26) which is too slow.
                        # Instead, we store the best l separately.
                        pass
        
        # The above approach with running_min loses the specific l. 
        # Let's use a different approach: store best_l[i][c] explicitly.
        # We'll recompute without running_min optimization for correctness, but optimize the inner loop.
        
        # Reset
        dp = [[INF] * 26 for _ in range(n + 1)]
        parent = [[None] * 26 for _ in range(n + 1)]
        for c in range(26):
            dp[0][c] = 0
        
        min1 = [INF] * (n + 1)
        char1 = [-1] * (n + 1)
        min2 = [INF] * (n + 1)
        min1[0] = 0
        char1[0] = 0
        min2[0] = INF
        
        # best_l[i][c] stores the start index l of the last group for state (i, c)
        best_l = [[-1] * 26 for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            # For each character c, try all possible group lengths L >= 3
            # l = i - L, so l from i-3 down to 0
            for c in range(26):
                best_cost = INF
                best_l_val = -1
                best_c_prev = -1
                
                # We need min_{c' != c} dp[l][c'] for l from 0 to i-3
                # Instead of iterating all l, we can use the min1/min2 arrays, but we need the specific l.
                # So we iterate l from i-3 down to 0.
                for l in range(i - 3, -1, -1):
                    # Get min cost at l for character != c
                    if char1[l] != c:
                        prev_cost = min1[l]
                        prev_c = char1[l]
                    else:
                        prev_cost = min2[l]
                        # Find the character for min2[l]
                        # We need to store char2 as well
                        pass
                
                # This is O(n) per state, total O(n^2 * 26) which is 50,000^2 * 26 = 65 billion, too slow.
        
        # Given the complexity, I'll implement the O(n*26*26) solution with explicit iteration over previous characters.
        # For each i and c, iterate over all possible previous characters c' != c, and for each c', find the best l.
        # But finding the best l for fixed c' and c is still O(n).
        
        # Alternative: For each i, and for each c, the cost for a group from l to i-1 with character c is P[c][i] - P[c][l].
        # dp[i][c] = min_{l=0}^{i-3} [ min_{c' != c} dp[l][c'] + P[c][i] - P[c][l] ]
        #          = P[c][i] + min_{l=0}^{i-3} [ min_{c' != c} dp[l][c'] - P[c][l] ]
        
        # Let f(l, c) = min_{c' != c} dp[l][c'] - P[c][l]
        # Then dp[i][c] = P[c][i] + min_{l=0}^{i-3} f(l, c)
        
        # We can maintain for each c, a running minimum of f(l, c) as l increases.
        # But f(l, c) depends on c, so we need 26 running minima.
        
        # Let's do that, and also store the l that achieved the minimum for each c at each i.
        # We'll store best_l_for_running_min[c] = the l that achieved the current running_min[c]
        
        dp = [[INF] * 26 for _ in range(n + 1)]
        parent = [[None] * 26 for _ in range(n + 1)]  # parent[i][c] = (l, c_prev)
        best_l_dp = [[-1] * 26 for _ in range(n + 1)]  # best_l_dp[i][c] = l that achieved dp[i][c]
        
        for c in range(26):
            dp[0][c] = 0
        
        min1 = [INF] * (n + 1)
        char1 = [-1] * (n + 1)
        min2 = [INF] * (n + 1)
        char2 = [-1] * (n + 1)
        min1[0] = 0
        char1[0] = 0
        min2[0] = INF
        char2[0] = -1
        
        # running_min[c] and best_l_running[c]
        running_min = [INF] * 26
        best_l_running = [-1] * 26
        
        for i in range(1, n + 1):
            # Update running_min with l = i-3
            if i >= 3:
                l = i - 3
                for c in range(26):
                    if char1[l] != c:
                        min_prev = min1[l]
                    else:
                        min_prev = min2[l]
                    if min_prev != INF:
                        val = min_prev - P[c][l]
                        if val < running_min[c]:
                            running_min[c] = val
                            best_l_running[c] = l
            
            for c in range(26):
                if running_min[c] != INF:
                    cost = running_min[c] + P[c][i]
                    if cost < dp[i][c]:
                        dp[i][c] = cost
                        best_l_dp[i][c] = best_l_running[c]
                        # Find c_prev
                        l = best_l_running[c]
                        if char1[l] != c:
                            c_prev = char1[l]
                        else:
                            c_prev = char2[l]
                        parent[i][c] = (l, c_prev)
            
            # Update min1, min2, char1, char2 for position i
            # Find two smallest values in dp[i]
            first_min = INF
            first_char = -1
            second_min = INF
            second_char = -1
            
            for c in range(26):
                if dp[i][c] < first_min:
                    second_min = first_min
                    second_char = first_char
                    first_min = dp[i][c]
                    first_char = c
                elif dp[i][c] < second_min:
                    second_min = dp[i][c]
                    second_char = c
            
            min1[i] = first_min
            char1[i] = first_char
            min2[i] = second_min
            char2[i] = second_char
        
        # Find the minimum cost at position n
        min_cost = INF
        last_char = -1
        for c in range(26):
            if dp[n][c] < min_cost:
                min_cost = dp[n][c]
                last_char = c
            elif dp[n][c] == min_cost and c < last_char:
                last_char = c
        
        if min_cost == INF:
            return ""
        
        # Reconstruct the string
        res = [''] * n
        i = n
        while i > 0:
            c = last_char
            l, c_prev = parent[i][c]
            # The group from l to i-1 is character c
            char_c = chr(ord('a') + c)
            for j in range(l, i):
                res[j] = char_c
            last_char = c_prev
            i = l
        
        return ''.join(res)