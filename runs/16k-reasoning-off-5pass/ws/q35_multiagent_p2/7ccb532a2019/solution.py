class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        # Count frequency of each character
        freq = [0] * 26
        for char in s:
            freq[ord(char) - ord('a')] += 1
        
        min_ops = n  # Worst case: delete all characters (k=0)
        
        # Iterate over all possible target frequencies k from 1 to n
        for k in range(1, n + 1):
            ops = 0
            pushed = 0  # Number of characters pushed from previous character
            
            for i in range(26):
                current_count = freq[i] + pushed
                if current_count > k:
                    # Excess characters: change to next char (push) or delete
                    # Cost is current_count - k (each excess char costs 1 op)
                    ops += current_count - k
                    # Push excess to next character
                    pushed = current_count - k
                else:
                    # Deficient characters: insert to reach k
                    # Cost is k - current_count
                    ops += k - current_count
                    # No excess to push
                    pushed = 0
            
            min_ops = min(min_ops, ops)
            
        return min_ops