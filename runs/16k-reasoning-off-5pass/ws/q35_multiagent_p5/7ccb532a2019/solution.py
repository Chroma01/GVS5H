class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        # Count frequency of each character
        freq = [0] * 26
        for char in s:
            freq[ord(char) - ord('a')] += 1
        
        # Sort frequencies in descending order to easily pick top m
        freq.sort(reverse=True)
        
        min_ops = n  # worst case: delete all and insert nothing (or similar)
        
        # Iterate over all possible target frequencies k
        # k can range from 1 to n
        for k in range(1, n + 1):
            # The number of distinct characters we can keep is m
            # Each kept character has frequency k, so total length is m * k <= n
            # Also, m cannot exceed 26 (number of lowercase letters)
            m = min(26, n // k)
            
            # We choose the top m characters with highest frequencies to keep
            # Calculate insertions and deletions
            
            insertions = 0
            deletions = 0
            
            # For the top m characters (kept)
            for i in range(m):
                f = freq[i]
                if f < k:
                    insertions += (k - f)
                elif f > k:
                    deletions += (f - k)
            
            # For the remaining characters (not kept), we must delete all their occurrences
            for i in range(m, 26):
                deletions += freq[i]
            
            # The cost is max(insertions, deletions) because change operations
            # can cover one deletion and one insertion at cost 1.
            # Unpaired deletions or insertions cost 1 each.
            ops = max(insertions, deletions)
            
            if ops < min_ops:
                min_ops = ops
                
        return min_ops