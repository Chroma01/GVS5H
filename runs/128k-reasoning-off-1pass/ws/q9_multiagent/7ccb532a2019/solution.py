class Solution:
    def makeStringGood(self, s: str) -> int:
        from collections import Counter
        
        # Count frequency of each character
        freq_map = Counter(s)
        
        # Get all non-zero frequencies
        frequencies = [count for count in freq_map.values() if count > 0]
        
        # If the string is empty (though constraints say length >= 3), return 0
        if not frequencies:
            return 0
            
        # Get unique frequencies and sort them
        unique_freqs = sorted(list(set(frequencies)))
        
        min_ops = float('inf')
        
        # Iterate through each unique frequency as a candidate target
        for target in unique_freqs:
            current_ops = 0
            for count in frequencies:
                if count > target:
                    current_ops += (count - target)
                elif count < target:
                    current_ops += (target - count)
            
            if current_ops < min_ops:
                min_ops = current_ops
        
        return min_ops

# Test cases
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    s1 = "acab"
    print(f"Example 1: {sol.makeStringGood(s1)}") # Expected: 1
    
    # Example 2
    s2 = "wddw"
    print(f"Example 2: {sol.makeStringGood(s2)}") # Expected: 0
    
    # Example 3
    s3 = "aaabc"
    print(f"Example 3: {sol.makeStringGood(s3)}") # Expected: 2
    
    # Edge Case 1: All same characters
    s4 = "aaaaa"
    print(f"Edge Case 1 (All same): {sol.makeStringGood(s4)}") # Expected: 0
    
    # Edge Case 2: All different characters
    s5 = "abcdef"
    print(f"Edge Case 2 (All different): {sol.makeStringGood(s5)}") # Expected: 0
    
    # Edge Case 3: Large input (performance check)
    import time
    s6 = "a" * 20000
    start = time.time()
    print(f"Edge Case 3 (Large input): {sol.makeStringGood(s6)}")
    print(f"Time taken: {time.time() - start:.4f}s")
    
    # Edge Case 4: Mixed frequencies
    s7 = "aabbccddeeffg" # a:2, b:2, c:2, d:2, e:2, f:2, g:1
    print(f"Edge Case 4 (Mixed): {sol.makeStringGood(s7)}") # Expected: 1 (change g to one of a-f or delete one of a-f)
    
    # Edge Case 5: Two distinct frequencies
    s8 = "aaabbbccc" # a:3, b:3, c:3 -> 0
    s9 = "aaabbbcc"  # a:3, b:3, c:2 -> Target 3: 0+0+1=1, Target 2: 1+1+0=2. Min 1.
    print(f"Edge Case 5a (Equal): {sol.makeStringGood(s8)}") # Expected: 0
    print(f"Edge Case 5b (Two freqs): {sol.makeStringGood(s9)}") # Expected: 1