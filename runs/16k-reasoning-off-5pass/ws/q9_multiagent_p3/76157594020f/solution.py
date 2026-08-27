class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        # Helper function to extract run lengths
        def get_runs(string):
            if not string:
                return []
            runs = []
            current_char = string[0]
            count = 1
            for char in string[1:]:
                if char == current_char:
                    count += 1
                else:
                    runs.append(count)
                    current_char = char
                    count = 1
            runs.append(count)
            return runs
        
        # Get initial run lengths
        runs = get_runs(s)
        n = len(s)
        
        # Binary search for the minimum possible max length k
        # Range of k is [1, n]
        left, right = 1, n
        
        while left < right:
            mid = (left + right) // 2
            k = mid
            
            # Calculate total operations needed to ensure all runs have length <= k
            ops_needed = 0
            for length in runs:
                if length > k:
                    # Derived formula: m = length // (k + 1)
                    # Explanation:
                    # We want to split a run of length L into segments of size at most k.
                    # Each operation flips one character, removing it from the run and acting as a separator.
                    # With m operations, we have m+1 segments and L-m characters remaining.
                    # We need (m+1) * k >= L - m  =>  m(k+1) >= L - k  =>  m >= (L - k) / (k + 1)
                    # Using integer arithmetic, ceil((L - k) / (k + 1)) simplifies to L // (k + 1).
                    ops_needed += length // (k + 1)
            
            if ops_needed <= numOps:
                right = mid
            else:
                left = mid + 1
                
        return left