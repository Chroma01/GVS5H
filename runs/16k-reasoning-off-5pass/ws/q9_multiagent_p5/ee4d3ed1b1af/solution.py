import bisect

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern p by '*' to get prefix, middle, and suffix
        # Since p contains exactly two '*', split will result in exactly 3 parts
        parts = p.split('*')
        if len(parts) != 3:
            return -1
        
        prefix, middle, suffix = parts
        
        # Find all starting indices of prefix in s
        prefix_indices = []
        start = 0
        while True:
            idx = s.find(prefix, start)
            if idx == -1:
                break
            prefix_indices.append(idx)
            start = idx + 1
        
        # Find all starting indices of suffix in s
        suffix_indices = []
        start = 0
        while True:
            idx = s.find(suffix, start)
            if idx == -1:
                break
            suffix_indices.append(idx)
            start = idx + 1
        
        # If either prefix or suffix is not found, no match possible
        if not prefix_indices or not suffix_indices:
            return -1
        
        min_len = float('inf')
        mid_len = len(middle)
        suf_len = len(suffix)
        prefix_len = len(prefix)
        
        # For each occurrence of prefix, find the earliest occurrence of suffix
        # such that the middle segment fits in between.
        # The constraint is that the substring must contain 'prefix', then 'middle', then 'suffix'.
        # Based on Example 1 analysis, 'middle' and 'suffix' must not overlap if 'suffix' is non-empty.
        # Specifically, the start of 'suffix' must be strictly after the end of 'middle'.
        # End of 'middle' is at p_idx + prefix_len + mid_len.
        # So, s_idx >= p_idx + prefix_len + mid_len + (1 if suffix else 0).
        
        for p_idx in prefix_indices:
            min_suf_start = p_idx + prefix_len + mid_len
            if suf_len > 0:
                min_suf_start += 1
            
            # Find the first suffix index >= min_suf_start
            idx = bisect.bisect_left(suffix_indices, min_suf_start)
            
            if idx < len(suffix_indices):
                s_idx = suffix_indices[idx]
                # Total length is from p_idx to end of suffix
                current_len = s_idx + suf_len - p_idx
                if current_len < min_len:
                    min_len = current_len
        
        return min_len if min_len != float('inf') else -1