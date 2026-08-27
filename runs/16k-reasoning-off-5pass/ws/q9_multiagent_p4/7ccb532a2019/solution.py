class Solution:
    def makeStringGood(self, s: str) -> int:
        from collections import Counter
        
        # Step 1: Count frequencies of each character
        counts = Counter(s)
        # Get distinct counts present in the string
        distinct_counts = sorted(counts.values())
        
        # We also consider k=1 if it's not present, as it might be optimal
        if 1 not in distinct_counts:
            distinct_counts.append(1)
        
        min_ops = float('inf')
        n = len(s)
        
        # Map char index (0-25) to its count
        char_counts = [0] * 26
        for char, count in counts.items():
            char_counts[ord(char) - ord('a')] = count
            
        for k in distinct_counts:
            # DP: dp[balance] = min_cost
            # balance can be positive or negative. We use a dict.
            # Initial state: balance 0, cost 0
            dp = {0: 0}
            
            for i in range(26):
                c = char_counts[i]
                if c == 0:
                    continue
                
                # Determine possible nets for this character
                # If c > k: must keep -> net = c - k (surplus)
                # If c == k: net = 0 (neutral)
                # If c < k: choice -> net1 = c - k (deficit), net2 = c (surplus)
                
                if c > k:
                    nets = [c - k]
                elif c == k:
                    nets = [0]
                else:
                    nets = [c - k, c]
                
                new_dp = {}
                for b, cost in dp.items():
                    for net in nets:
                        # Calculate potential moves between current balance and current net
                        # A move saves 1 operation (change vs delete+insert)
                        moves = 0
                        if b > 0 and net < 0:
                            moves = min(b, -net)
                        elif b < 0 and net > 0:
                            moves = min(-b, net)
                        
                        # Cost contribution: |net| (base cost) - moves (savings)
                        new_cost = cost + abs(net) - moves
                        new_balance = b + net - moves
                        
                        if new_balance not in new_dp or new_dp[new_balance] > new_cost:
                            new_dp[new_balance] = new_cost
                dp = new_dp
            
            # After processing all chars, any remaining balance must be resolved by deletions/insertions
            if dp:
                final_cost = min(abs(b) + cost for b, cost in dp.items())
                if final_cost < min_ops:
                    min_ops = final_cost
        
        return min_ops