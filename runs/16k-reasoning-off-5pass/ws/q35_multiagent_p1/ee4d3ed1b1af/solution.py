class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        # Split p into prefix, middle, suffix
        parts = p.split('*')
        # There should be 3 parts because there are exactly two '*'
        prefix, middle, suffix = parts[0], parts[1], parts[2]
        
        len_prefix = len(prefix)
        len_middle = len(middle)
        len_suffix = len(suffix)
        
        # Precompute all prefix matches: list of start indices
        prefix_matches = []
        if len_prefix == 0:
            # Empty prefix matches at every position from 0 to n
            prefix_matches = list(range(n + 1))
        else:
            start = 0
            while start <= n - len_prefix:
                idx = s.find(prefix, start)
                if idx == -1:
                    break
                prefix_matches.append(idx)
                start = idx + 1
        
        # Precompute all suffix matches: list of start indices
        suffix_matches = []
        if len_suffix == 0:
            # Empty suffix matches at every position from 0 to n
            suffix_matches = list(range(n + 1))
        else:
            start = 0
            while start <= n - len_suffix:
                idx = s.find(suffix, start)
                if idx == -1:
                    break
                suffix_matches.append(idx)
                start = idx + 1
        
        # Precompute min_suf: min_suffix_start_after[i] = min start index of a suffix match that starts at or after i
        min_suf = [float('inf')] * (n + 2)  # extra space for safety
        for s1 in suffix_matches:
            if s1 <= n:
                min_suf[s1] = min(min_suf[s1], s1)
        # Backward pass
        for i in range(n - 1, -1, -1):
            min_suf[i] = min(min_suf[i], min_suf[i + 1])
        
        # Precompute max_pre: max_prefix_start_before[i] = max start index of a prefix match that ends at or before i
        max_pre = [-1] * (n + 2)
        for s0 in prefix_matches:
            e0 = s0 + len_prefix
            if e0 <= n:
                max_pre[e0] = max(max_pre[e0], s0)
        # Forward pass
        for i in range(1, n + 1):
            max_pre[i] = max(max_pre[i], max_pre[i - 1])
        
        ans = float('inf')
        
        if len_middle == 0:
            # For each prefix match, find the earliest suffix that starts at or after the prefix end
            for s0 in prefix_matches:
                e0 = s0 + len_prefix
                if e0 > n:
                    continue
                s1 = min_suf[e0]
                if s1 != float('inf'):
                    # The matched substring is from s0 to s1 + len_suffix
                    length = s1 + len_suffix - s0
                    ans = min(ans, length)
        else:
            # Find all occurrences of middle in s
            middle_matches = []
            start = 0
            while start <= n - len_middle:
                idx = s.find(middle, start)
                if idx == -1:
                    break
                middle_matches.append(idx)
                start = idx + 1
            
            for k in middle_matches:
                e_mid = k + len_middle
                if e_mid > n:
                    continue
                # Get the best prefix start that ends at or before k
                s0 = max_pre[k]
                if s0 == -1:
                    continue
                # Get the best suffix start that starts at or after e_mid
                s1 = min_suf[e_mid]
                if s1 == float('inf'):
                    continue
                length = s1 + len_suffix - s0
                ans = min(ans, length)
        
        return ans if ans != float('inf') else -1