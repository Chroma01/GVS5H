class Solution:
    def makeStringGood(self, s: str) -> int:
        from collections import Counter
        
        freq = Counter(s)
        n = len(s)
        # Get sorted frequencies in descending order
        freqs = sorted(freq.values(), reverse=True)
        
        ans = n  # Initialize with maximum possible operations (delete all)
        
        # Iterate over all possible target frequencies k
        for k in range(1, n + 1):
            # Iterate over all possible number of distinct characters m
            for m in range(1, 27):
                # If the total length required exceeds n, break
                if m * k > n:
                    break
                
                cost = 0
                # Calculate cost for the top m characters
                for i in range(m):
                    cost += abs(freqs[i] - k)
                
                # Add the cost for characters not in the top m (they must be deleted/removed)
                # The term (n - m * k) accounts for the net deletion needed to reach length m*k
                # combined with the fact that abs(freqs[i]-k) already accounts for adjustments in chosen chars.
                # Specifically: 
                # cost = sum(|freq[i] - k| for i in chosen) + (n - m * k)
                # This formula is standard for this problem.
                cost += n - m * k
                
                ans = min(ans, cost)
                
        return ans