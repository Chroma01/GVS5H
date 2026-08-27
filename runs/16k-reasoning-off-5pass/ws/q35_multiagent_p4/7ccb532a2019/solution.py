class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        # Count frequency of each character
        freq = [0] * 26
        for char in s:
            freq[ord(char) - ord('a')] += 1
        
        # Sort frequencies in descending order
        freq.sort(reverse=True)
        
        min_ops = n  # worst case: delete all and insert nothing? or delete all and insert new string
        
        # Iterate over all possible target frequencies k
        for k in range(1, n + 1):
            # Iterate over all possible number of distinct characters m
            # m can be from 1 to 26
            for m in range(1, 27):
                # If the total length of the good string (m * k) is 0, skip
                if m * k == 0:
                    continue
                
                # Calculate the number of characters we can keep
                # We choose the top m characters with highest frequencies
                kept = 0
                for i in range(m):
                    kept += min(freq[i], k)
                
                # The cost is: n (original length) + m*k (final length) - 2 * kept
                # Explanation: 
                #   Deletions = n - kept
                #   Insertions = m*k - kept
                #   Total operations = (n - kept) + (m*k - kept) = n + m*k - 2*kept
                ops = n + m * k - 2 * kept
                if ops < min_ops:
                    min_ops = ops
        
        return min_ops