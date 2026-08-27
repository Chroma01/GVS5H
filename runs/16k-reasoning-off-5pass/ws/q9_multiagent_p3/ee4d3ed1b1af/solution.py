class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern p into prefix, middle, and suffix based on '*'
        stars = p.find('*')
        star2 = p.find('*', stars + 1)
        prefix = p[:stars]
        middle = p[stars+1:star2]
        suffix = p[star2+1:]
        
        n = len(s)
        m_pre = len(prefix)
        m_mid = len(middle)
        m_suf = len(suffix)
        
        # Helper to get all start indices of pattern in s using KMP
        def get_occurrences(text: str, pattern: str):
            if not pattern:
                return [] 
            if len(pattern) > len(text):
                return []
            
            # Compute prefix function (pi array)
            pi = [0] * len(pattern)
            k = 0
            for q in range(1, len(pattern)):
                while k > 0 and pattern[k] != pattern[q]:
                    k = pi[k-1]
                if pattern[k] == pattern[q]:
                    k += 1
                pi[q] = k
            
            # Search
            q = 0 # number of characters matched
            occurrences = []
            for i in range(len(text)):
                while q > 0 and pattern[q] != text[i]:
                    q = pi[q-1]
                if pattern[q] == text[i]:
                    q += 1
                if q == len(pattern):
                    occurrences.append(i - len(pattern) + 1)
                    q = pi[q-1]
            return occurrences

        # Special handling for empty middle
        if m_mid == 0:
            pre_occ = get_occurrences(s, prefix)
            suf_occ = get_occurrences(s, suffix)
            
            if not pre_occ or not suf_occ:
                return -1
            
            min_len = float('inf')
            suf_idx = 0
            num_suf = len(suf_occ)
            
            for pre_start in pre_occ:
                # The prefix ends at pre_start + m_pre - 1
                # We need a suffix starting at or after this end index
                target = pre_start + m_pre - 1
                while suf_idx < num_suf and suf_occ[suf_idx] < target:
                    suf_idx += 1
                
                if suf_idx < num_suf:
                    # Suffix starts at suf_occ[suf_idx]
                    # Length is (start of suffix) - (start of prefix) + 1
                    # But wait, the pattern is prefix + * + suffix.
                    # The substring in s is from pre_start to (suf_start + m_suf - 1).
                    # Length = (suf_start + m_suf - 1) - pre_start + 1 = suf_start - pre_start + m_suf
                    current_len = suf_occ[suf_idx] - pre_start + m_suf
                    if current_len < min_len:
                        min_len = current_len
            
            return min_len if min_len != float('inf') else -1

        # General case: middle is not empty
        pre_occ = get_occurrences(s, prefix)
        mid_occ = get_occurrences(s, middle)
        suf_occ = get_occurrences(s, suffix)
        
        if not pre_occ or not mid_occ or not suf_occ:
            return -1
        
        # Precompute best prefix start for each index in s
        # best_pre[i] = max(pre_start) such that pre_start + m_pre - 1 <= i
        best_pre = [-1] * n
        ptr = 0
        num_pre = len(pre_occ)
        
        for i in range(n):
            while ptr + 1 < num_pre and pre_occ[ptr+1] + m_pre - 1 <= i:
                ptr += 1
            
            if ptr < num_pre:
                best_pre[i] = pre_occ[ptr]
        
        # Precompute best suffix end for each index in s
        # best_suf[i] = min(suf_end) such that suf_start >= i
        # We need to handle index n for the case where m_end + 1 == n
        best_suf = [float('inf')] * (n + 1)
        suf_ptr = num_suf - 1
        num_suf = len(suf_occ)
        
        for i in range(n - 1, -1, -1):
            while suf_ptr > 0 and suf_occ[suf_ptr-1] >= i:
                suf_ptr -= 1
            
            if suf_ptr < num_suf:
                best_suf[i] = suf_occ[suf_ptr] + m_suf - 1
        
        # best_suf[n] remains inf unless there's a suffix starting exactly at n (impossible as indices are 0..n-1)
        # However, if m_end + 1 == n, we access best_suf[n]. 
        # A suffix starting at n is impossible in 0-indexed string of length n.
        # So best_suf[n] should be inf, which is correct (no valid suffix).
        
        min_total_len = float('inf')
        
        for m_start in mid_occ:
            m_end = m_start + m_mid - 1
            
            p_start = best_pre[m_start]
            if p_start == -1:
                continue
            
            suf_start_idx = m_end + 1
            if suf_start_idx > n:
                continue
                
            s_end = best_suf[suf_start_idx]
            if s_end == float('inf'):
                continue
            
            total_len = s_end - p_start + 1
            if total_len < min_total_len:
                min_total_len = total_len
        
        return min_total_len if min_total_len != float('inf') else -1