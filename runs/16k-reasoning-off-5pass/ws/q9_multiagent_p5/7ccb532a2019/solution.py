from collections import Counter

class Solution:
    def makeStringGood(self, s: str) -> int:
        # Count the frequency of each character in the string
        char_counts = Counter(s)
        
        # Count how many characters have a specific frequency
        # For example, if s = "aaabc", char_counts = {'a':3, 'b':1, 'c':1}
        # freq_of_freq will be {3: 1, 1: 2}
        freq_of_freq = Counter(char_counts.values())
        
        # Get unique frequencies present in the string and sort them
        unique_freqs = sorted(freq_of_freq.keys())
        
        # Initialize the minimum operations with the cost of deleting all characters
        # This covers the case where the optimal strategy is to remove everything (k=0 effectively)
        min_ops = len(s)
        
        # Iterate through each unique frequency present in the string as a candidate target k
        for k in unique_freqs:
            current_ops = 0
            for c, count in freq_of_freq.items():
                # For each character type with frequency c:
                # Option 1: Keep the character type and adjust its count to k.
                #           Cost is |c - k|.
                # Option 2: Drop the character type entirely (delete all occurrences).
                #           Cost is c.
                # We choose the minimum of these two options.
                cost_per_char = min(abs(c - k), c)
                current_ops += count * cost_per_char
            
            # Update the global minimum operations found so far
            if current_ops < min_ops:
                min_ops = current_ops
                
        return min_ops