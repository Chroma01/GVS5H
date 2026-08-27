class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern p into prefix, middle, suffix based on two '*'
        # p structure: prefix + '*' + middle + '*' + suffix
        parts = p.split('*')
        # Since there are exactly two '*', split will result in exactly 3 parts
        prefix = parts[0]
        middle = parts[1]
        suffix = parts[2]
        
        n = len(s)
        m_pre = len(prefix)
        m_mid = len(middle)
        m_suf = len(suffix)
        
        # If all segments are empty, the shortest substring is empty (length 0)
        if m_pre == 0 and m_mid == 0 and m_suf == 0:
            return 0
        
        # Find all starting indices for prefix, middle, and suffix
        # Using a loop with find() is efficient O(N)
        pre_indices = []
        curr = 0
        while True:
            idx = s.find(prefix, curr)
            if idx == -1:
                break
            pre_indices.append(idx)
            curr = idx + 1 # Allow overlapping occurrences if prefix is short
        
        mid_indices = []
        curr = 0
        while True:
            idx = s.find(middle, curr)
            if idx == -1:
                break
            mid_indices.append(idx)
            curr = idx + 1
        
        suf_indices = []
        curr = 0
        while True:
            idx = s.find(suffix, curr)
            if idx == -1:
                break
            suf_indices.append(idx)
            curr = idx + 1
            
        # If any segment is not found, return -1
        if not pre_indices or not mid_indices or not suf_indices:
            return -1
        
        # Precompute next occurrence for middle and suffix to allow O(1) lookup
        # next_mid[i] = index of first occurrence of middle at or after i
        # next_suf[i] = index of first occurrence of suffix at or after i
        
        # Initialize next arrays with -1
        next_mid = [-1] * (n + 1)
        next_suf = [-1] * (n + 1)
        
        # Fill next_mid using two-pointer approach
        p_idx = 0
        for i in range(n):
            while p_idx < len(mid_indices) and mid_indices[p_idx] < i:
                p_idx += 1
            if p_idx < len(mid_indices):
                next_mid[i] = mid_indices[p_idx]
            else:
                next_mid[i] = -1
        
        # Fill next_suf using two-pointer approach
        p_idx = 0
        for i in range(n):
            while p_idx < len(suf_indices) and suf_indices[p_idx] < i:
                p_idx += 1
            if p_idx < len(suf_indices):
                next_suf[i] = suf_indices[p_idx]
            else:
                next_suf[i] = -1
                
        min_len = float('inf')
        
        # Iterate through all occurrences of prefix
        for start_pre in pre_indices:
            # The match must start at start_pre.
            # The prefix ends at start_pre + m_pre.
            # The middle must start at or after start_pre + m_pre.
            start_mid = start_pre + m_pre
            
            # If start_mid is beyond the string length, no valid middle can exist
            if start_mid > n:
                continue
                
            first_mid = next_mid[start_mid]
            if first_mid == -1:
                continue
            
            # The middle ends at first_mid + m_mid.
            # The suffix must start at or after first_mid + m_mid.
            start_suf = first_mid + m_mid
            
            # If start_suf is beyond the string length, no valid suffix can exist
            if start_suf > n:
                continue
                
            first_suf = next_suf[start_suf]
            if first_suf == -1:
                continue
            
            # Calculate length
            # Substring is from start_pre to first_suf + m_suf - 1
            # Length = (first_suf + m_suf) - start_pre
            current_len = (first_suf + m_suf) - start_pre
            if current_len < min_len:
                min_len = current_len
        
        return min_len if min_len != float('inf') else -1