class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern into prefix, middle, suffix
        parts = p.split('*')
        # parts should have exactly 3 elements because p has exactly two '*'
        prefix, middle, suffix = parts[0], parts[1], parts[2]
        
        n = len(s)
        len_prefix = len(prefix)
        len_middle = len(middle)
        len_suffix = len(suffix)
        
        # Edge case: if both prefix and suffix are empty, the shortest match is empty string
        if len_prefix == 0 and len_suffix == 0:
            return 0
        
        # Precompute next occurrence of middle after each index
        # next_middle[i] = starting index of the first occurrence of middle in s at or after i
        # If no such occurrence, set to infinity
        import math
        next_middle = [math.inf] * (n + 1)
        
        # Fill next_middle from right to left
        # We can use string find to locate middle
        # But to do it efficiently, we'll iterate backwards
        # Actually, we can just use a loop with find for each position? That would be O(n*m) worst case.
        # Instead, we can precompute all occurrences of middle and then fill next_middle.
        
        # Find all occurrences of middle in s
        middle_occurrences = []
        if len_middle == 0:
            # If middle is empty, it occurs at every position
            # next_middle[i] = i
            for i in range(n + 1):
                next_middle[i] = i
        else:
            # Find all occurrences of middle
            start = 0
            while True:
                idx = s.find(middle, start)
                if idx == -1:
                    break
                middle_occurrences.append(idx)
                start = idx + 1
            
            # Fill next_middle from right to left
            # next_middle[i] is the smallest occurrence >= i
            occ_idx = len(middle_occurrences) - 1
            for i in range(n, -1, -1):
                if occ_idx >= 0 and middle_occurrences[occ_idx] >= i:
                    next_middle[i] = middle_occurrences[occ_idx]
                    # Keep occ_idx as is because next_middle[i-1] might use the same occurrence
                else:
                    # Move occ_idx backwards until we find an occurrence >= i or run out
                    while occ_idx >= 0 and middle_occurrences[occ_idx] >= i:
                        occ_idx -= 1
                    if occ_idx >= 0:
                        next_middle[i] = middle_occurrences[occ_idx]
                    else:
                        next_middle[i] = math.inf
        
        # Precompute next occurrence of suffix after each index
        # next_suffix[i] = starting index of the first occurrence of suffix in s at or after i
        next_suffix = [math.inf] * (n + 1)
        
        if len_suffix == 0:
            # If suffix is empty, it occurs at every position
            for i in range(n + 1):
                next_suffix[i] = i
        else:
            # Find all occurrences of suffix
            suffix_occurrences = []
            start = 0
            while True:
                idx = s.find(suffix, start)
                if idx == -1:
                    break
                suffix_occurrences.append(idx)
                start = idx + 1
            
            # Fill next_suffix from right to left
            occ_idx = len(suffix_occurrences) - 1
            for i in range(n, -1, -1):
                if occ_idx >= 0 and suffix_occurrences[occ_idx] >= i:
                    next_suffix[i] = suffix_occurrences[occ_idx]
                else:
                    while occ_idx >= 0 and suffix_occurrences[occ_idx] >= i:
                        occ_idx -= 1
                    if occ_idx >= 0:
                        next_suffix[i] = suffix_occurrences[occ_idx]
                    else:
                        next_suffix[i] = math.inf
        
        # Find all occurrences of prefix and store their end indices
        # For each prefix occurrence ending at i (so prefix is s[i-len_prefix+1 : i+1]),
        # we need:
        #   m_start = next_middle[i+1]  (first occurrence of middle at or after i+1)
        #   if m_start is valid, then we need suffix to start at or after m_start + len_middle
        #   k = next_suffix[m_start + len_middle]
        #   if k is valid, then the substring is from (i - len_prefix + 1) to (k + len_suffix - 1)
        #   length = (k + len_suffix - 1) - (i - len_prefix + 1) + 1 = k + len_suffix - i + len_prefix - 1
        
        min_len = math.inf
        
        # Find all prefix occurrences
        start = 0
        while True:
            idx = s.find(prefix, start)
            if idx == -1:
                break
            # prefix starts at idx, ends at idx + len_prefix - 1
            end_prefix = idx + len_prefix - 1
            # We need middle to start at or after end_prefix + 1
            m_start = next_middle[end_prefix + 1]
            if m_start != math.inf:
                # We need suffix to start at or after m_start + len_middle
                k = next_suffix[m_start + len_middle]
                if k != math.inf:
                    # The substring is from idx to k + len_suffix - 1
                    length = k + len_suffix - idx
                    if length < min_len:
                        min_len = length
            start = idx + 1
        
        return min_len if min_len != math.inf else -1