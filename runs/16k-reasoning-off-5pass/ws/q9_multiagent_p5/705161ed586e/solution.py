class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # Convert characters to integers 0-25
        s = [ord(c) - ord('a') for c in caption]
        
        # Precompute prefix_cost[26][n+1] and suffix_cost[26][n+1]
        # prefix_cost[c][i] = sum(|s[0...i-1] - c|)
        # suffix_cost[c][i] = sum(|s[i...n-1] - c|)
        prefix_cost = [[0] * (n + 1) for _ in range(26)]
        suffix_cost = [[0] * (n + 1) for _ in range(26)]
        
        for c in range(26):
            current = 0
            for i in range(n):
                current += abs(s[i] - c)
                prefix_cost[c][i+1] = current
            current = 0
            for i in range(n-1, -1, -1):
                current += abs(s[i] - c)
                suffix_cost[c][i] = current
        
        best_cost = float('inf')
        best_string = ""
        
        # Helper to update best solution
        def update_best(cost, cand_str):
            nonlocal best_cost, best_string
            if best_string == "" or cost < best_cost or (cost == best_cost and cand_str < best_string):
                best_cost = cost
                best_string = cand_str

        # Single block candidates: convert entire string to character c
        for c in range(26):
            cost = prefix_cost[c][n]
            update_best(cost, chr(c + ord('a')) * n)
        
        # Two block candidates: split at k, first part [0, k), second part [k, n)
        # Valid splits require both parts to have length >= 3
        for k in range(3, n - 2):
            # Find best c1 for first part
            min_cost1 = float('inf')
            for c in range(26):
                if prefix_cost[c][k] < min_cost1:
                    min_cost1 = prefix_cost[c][k]
            
            # Find smallest c1 that achieves min_cost1
            c1_opt = 26
            for c in range(26):
                if prefix_cost[c][k] == min_cost1:
                    c1_opt = c
                    break
            
            # Find best c2 for second part
            min_cost2 = float('inf')
            for c in range(26):
                if suffix_cost[c][k] < min_cost2:
                    min_cost2 = suffix_cost[c][k]
            
            # Find smallest c2 that achieves min_cost2
            c2_opt = 26
            for c in range(26):
                if suffix_cost[c][k] == min_cost2:
                    c2_opt = c
                    break
            
            total_cost = min_cost1 + min_cost2
            candidate = chr(c1_opt + ord('a')) * k + chr(c2_opt + ord('a')) * (n - k)
            update_best(total_cost, candidate)
            
        return best_string