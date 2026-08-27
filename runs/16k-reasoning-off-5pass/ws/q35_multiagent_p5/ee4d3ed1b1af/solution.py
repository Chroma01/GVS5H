class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split the pattern into prefix, middle, and suffix
        parts = p.split('*', 2)
        prefix = parts[0]
        middle = parts[1]
        suffix = parts[2]
        
        n = len(s)
        len_prefix = len(prefix)
        len_middle = len(middle)
        len_suffix = len(suffix)
        
        # Case: p is "**"
        if len_prefix == 0 and len_middle == 0 and len_suffix == 0:
            return 0
        
        # Precompute next_suffix: next_suffix[i] is the smallest k >= i such that s[k:k+len_suffix] == suffix
        # If no such k exists, set to infinity
        next_suffix = [float('inf')] * (n + 1)
        # We'll compute from right to left
        # For i from n-1 down to 0
        for i in range(n - 1, -1, -1):
            if i + len_suffix <= n:
                if s[i:i+len_suffix] == suffix:
                    next_suffix[i] = i
                else:
                    next_suffix[i] = next_suffix[i+1]
            else:
                next_suffix[i] = next_suffix[i+1]
        
        min_len = float('inf')
        
        # Iterate over all possible start positions for the prefix
        # We can use string find to get all occurrences of prefix
        start = 0
        while start <= n - len_prefix:
            idx = s.find(prefix, start)
            if idx == -1:
                break
            # prefix matches at s[idx:idx+len_prefix]
            end_prefix = idx + len_prefix
            # Check if middle part exists and matches
            if end_prefix + len_middle <= n:
                if s[end_prefix:end_prefix+len_middle] == middle:
                    start_suffix = end_prefix + len_middle
                    # Find the earliest suffix occurrence at or after start_suffix
                    k = next_suffix[start_suffix]
                    if k != float('inf'):
                        # The substring is from idx to k+len_suffix
                        total_len = k + len_suffix - idx
                        if total_len < min_len:
                            min_len = total_len
            # Move start to next position to find next prefix occurrence
            start = idx + 1
            
        return min_len if min_len != float('inf') else -1