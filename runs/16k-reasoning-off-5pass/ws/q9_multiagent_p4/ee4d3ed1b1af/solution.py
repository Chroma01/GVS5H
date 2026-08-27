import bisect

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern p into three parts based on the two '*' characters
        # p is guaranteed to have exactly two '*'
        parts = p.split('*')
        prefix = parts[0]
        middle = parts[1]
        suffix = parts[2]
        
        len_prefix = len(prefix)
        len_middle = len(middle)
        len_suffix = len(suffix)
        
        # Helper to find all starting indices of a substring in s
        def get_indices(substring):
            indices = []
            start = 0
            while True:
                idx = s.find(substring, start)
                if idx == -1:
                    break
                indices.append(idx)
                start = idx + 1
            return indices
        
        idx_prefix = get_indices(prefix)
        idx_middle = get_indices(middle)
        idx_suffix = get_indices(suffix)
        
        min_len = float('inf')
        
        # Iterate through each occurrence of prefix
        for i in idx_prefix:
            # Find the first occurrence of middle that starts at or after the end of prefix
            # The middle part can start at index (i + len_prefix)
            # We use bisect_left to find the first element >= (i + len_prefix)
            required_j = i + len_prefix
            j_idx = bisect.bisect_left(idx_middle, required_j)
            
            if j_idx >= len(idx_middle):
                continue
            
            j = idx_middle[j_idx]
            
            # Find the first occurrence of suffix that starts at or after the end of middle
            # The suffix part can start at index (j + len_middle)
            required_k = j + len_middle
            k_idx = bisect.bisect_left(idx_suffix, required_k)
            
            if k_idx >= len(idx_suffix):
                continue
            
            k = idx_suffix[k_idx]
            
            # Calculate length of the substring from start of prefix to end of suffix
            # Start index: i
            # End index: k + len_suffix - 1
            # Length: (k + len_suffix) - i
            current_len = (k + len_suffix) - i
            if current_len < min_len:
                min_len = current_len
        
        return min_len if min_len != float('inf') else -1