class Solution:
    def makeStringGood(self, s: str) -> int:
        from collections import Counter
        
        freq = [0] * 26
        for c in s:
            freq[ord(c) - ord('a')] += 1
        
        n = len(s)
        min_ops = n  # Upper bound: delete all and insert nothing (or other trivial bounds)
        
        # Iterate over target frequency k
        # k can range from 1 to n
        for k in range(1, n + 1):
            # Iterate over number of distinct characters m
            # m can range from 1 to 26
            for m in range(1, 27):
                # If the minimum possible length (m * k) is already greater than n + some buffer,
                # the cost will likely be high, but we must check because we can insert.
                # However, if m * k is very large, the insertion cost alone will be high.
                # We can prune if m * k > n + min_ops, but min_ops decreases, so it's tricky.
                # Given constraints, we can just run the loops.
                
                # Iterate over start character
                # The block of m characters starts at 'start'
                for start in range(27 - m):
                    current_cost = 0
                    
                    # Cost for characters before the target block: must be deleted
                    for i in range(start):
                        current_cost += freq[i]
                    
                    # Cost for characters in the target block [start, start + m - 1]
                    carry = 0
                    for i in range(start, start + m):
                        avail = freq[i] + carry
                        if avail > k:
                            excess = avail - k
                            carry = excess
                            current_cost += excess  # Cost to increment excess characters to next
                        elif avail < k:
                            needed = k - avail
                            carry = 0
                            current_cost += needed  # Cost to insert missing characters
                        else:
                            carry = 0
                    
                    # Cost for characters after the target block: must be deleted
                    for i in range(start + m, 26):
                        current_cost += freq[i]
                    
                    if current_cost < min_ops:
                        min_ops = current_cost
                        
        return min_ops