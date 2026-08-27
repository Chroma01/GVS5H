import bisect

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern into prefix, middle, suffix based on two '*'
        parts = p.split('*')
        # Although constraints guarantee exactly two '*', we handle the split result safely
        if len(parts) != 3:
            return -1
        
        prefix, mid, suffix = parts[0], parts[1], parts[2]
        
        # Helper to find all start indices of a substring in s
        def get_indices(text: str, sub: str) -> list[int]:
            if not sub:
                # If sub is empty, it can start at any position from 0 to len(text)
                return list(range(len(text) + 1))
            indices = []
            start = 0
            while True:
                idx = text.find(sub, start)
                if idx == -1:
                    break
                indices.append(idx)
                start = idx + 1
            return indices
        
        # Get all start indices for prefix, mid, suffix
        prefix_indices = get_indices(s, prefix)
        mid_indices = get_indices(s, mid)
        suffix_indices = get_indices(s, suffix)
        
        # If any part is missing, no match is possible
        if not prefix_indices or not mid_indices or not suffix_indices:
            return -1
        
        min_len = float('inf')
        len_prefix = len(prefix)
        len_mid = len(mid)
        len_suffix = len(suffix)
        
        # Iterate through each starting position of prefix
        for p_idx in prefix_indices:
            # The middle part must start at or after the end of the prefix
            start_mid_min = p_idx + len_prefix
            
            # Find the first occurrence of 'mid' starting at or after start_mid_min
            m_idx = bisect.bisect_left(mid_indices, start_mid_min)
            
            # If no such occurrence exists, skip
            if m_idx == len(mid_indices):
                continue
            
            m_start = mid_indices[m_idx]
            end_mid = m_start + len_mid
            
            # The suffix part must start at or after the end of the middle part
            s_idx = bisect.bisect_left(suffix_indices, end_mid)
            
            # If no such occurrence exists, skip
            if s_idx == len(suffix_indices):
                continue
            
            s_start = suffix_indices[s_idx]
            
            # Calculate length of the matching substring
            # Substring is from p_idx to s_start + len_suffix (exclusive)
            current_len = s_start + len_suffix - p_idx
            if current_len < min_len:
                min_len = current_len
        
        if min_len == float('inf'):
            return -1
        return min_len