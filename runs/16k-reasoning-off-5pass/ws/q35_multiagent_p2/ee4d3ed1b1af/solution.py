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
        
        # If both prefix and suffix are empty, then we just need to find middle
        # The shortest substring containing middle is middle itself, if it exists.
        # But note: the pattern is "**" -> prefix="", middle="", suffix=""
        # Then the answer is 0.
        # If prefix="" and suffix="", then we need to find middle in s.
        # The shortest substring is len(middle) if middle is found, else -1.
        # But actually, the problem says: the substring must start with prefix, end with suffix, and contain middle.
        # If prefix and suffix are empty, then the substring can be just middle.
        
        # Helper function to find all starting indices of a pattern in s
        def find_all_occurrences(text, pattern):
            if not pattern:
                # If pattern is empty, it occurs at every position from 0 to n
                # But for our purposes, we can handle empty patterns separately.
                return list(range(n + 1))  # empty pattern occurs at every index from 0 to n
            indices = []
            start = 0
            while True:
                idx = text.find(pattern, start)
                if idx == -1:
                    break
                indices.append(idx)
                start = idx + 1
            return indices
        
        # Get all starting indices for prefix, middle, suffix
        # Note: for suffix, we store the starting index of the suffix occurrence.
        prefix_starts = find_all_occurrences(s, prefix)
        middle_starts = find_all_occurrences(s, middle)
        suffix_starts = find_all_occurrences(s, suffix)
        
        # If prefix is empty, then prefix_starts should be [0, 1, ..., n] but actually,
        # an empty prefix matches at every position. However, for the purpose of the substring starting at i,
        # if prefix is empty, then i can be any index from 0 to n - len(middle) - len(suffix) ... but actually,
        # we'll handle it naturally: if prefix is empty, then prefix_starts will be all indices from 0 to n.
        # But to avoid O(n) iteration when prefix is empty, we can optimize.
        
        # Similarly for suffix: if suffix is empty, then suffix_starts will be all indices from 0 to n.
        
        # We want to minimize: (j + len_suffix) - i, where:
        #   i is in prefix_starts
        #   j is in suffix_starts
        #   and there exists k in middle_starts such that:
        #       i + len_prefix <= k  and  k + len_middle <= j
        #   which is equivalent to: j >= k + len_middle and k >= i + len_prefix
        
        # Precompute for each possible "left bound" L = i + len_prefix, the minimum required j.
        # Actually, we can iterate over i in prefix_starts, and for each i:
        #   L = i + len_prefix
        #   We need the smallest k in middle_starts such that k >= L.
        #   Then the minimal j needed is k + len_middle.
        #   Then we need the smallest j in suffix_starts such that j >= k + len_middle.
        
        # To do this efficiently:
        # 1. If middle is empty, then any j >= L works. So we just need the smallest j in suffix_starts >= L.
        # 2. If middle is not empty, then for each i, we find the first k in middle_starts >= L (using bisect),
        #    then we need j >= k + len_middle, so we find the smallest j in suffix_starts >= k + len_middle.
        
        import bisect
        
        # Sort the lists (they are already sorted by construction)
        # prefix_starts, middle_starts, suffix_starts are sorted.
        
        ans = float('inf')
        
        # If middle is empty, then the condition is just: j >= i + len_prefix
        # So for each i, we need smallest j in suffix_starts >= i + len_prefix
        if len_middle == 0:
            # For each i in prefix_starts, find smallest j in suffix_starts >= i + len_prefix
            for i in prefix_starts:
                L = i + len_prefix
                # Find smallest j in suffix_starts >= L
                idx = bisect.bisect_left(suffix_starts, L)
                if idx < len(suffix_starts):
                    j = suffix_starts[idx]
                    # The substring is from i to j + len_suffix - 1
                    length = j + len_suffix - i
                    if length < ans:
                        ans = length
        else:
            # For each i in prefix_starts:
            #   L = i + len_prefix
            #   Find the first k in middle_starts >= L
            #   Then we need j >= k + len_middle
            #   Find smallest j in suffix_starts >= k + len_middle
            for i in prefix_starts:
                L = i + len_prefix
                # Find first k in middle_starts >= L
                idx_k = bisect.bisect_left(middle_starts, L)
                if idx_k < len(middle_starts):
                    k = middle_starts[idx_k]
                    # The middle part ends at k + len_middle - 1, so the suffix must start at j >= k + len_middle
                    min_j = k + len_middle
                    # Find smallest j in suffix_starts >= min_j
                    idx_j = bisect.bisect_left(suffix_starts, min_j)
                    if idx_j < len(suffix_starts):
                        j = suffix_starts[idx_j]
                        length = j + len_suffix - i
                        if length < ans:
                            ans = length
        
        return ans if ans != float('inf') else -1