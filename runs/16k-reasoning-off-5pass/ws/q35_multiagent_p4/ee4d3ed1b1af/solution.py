import bisect

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern into prefix, middle, suffix
        # p has exactly two '*'
        first_star = p.find('*')
        second_star = p.find('*', first_star + 1)
        
        prefix = p[:first_star]
        middle = p[first_star+1:second_star]
        suffix = p[second_star+1:]
        
        n = len(s)
        len_prefix = len(prefix)
        len_middle = len(middle)
        len_suffix = len(suffix)
        
        # Trivial case: if all parts are empty, return 0
        if len_prefix == 0 and len_middle == 0 and len_suffix == 0:
            return 0
        
        # Find all starting indices of prefix in s
        prefix_starts = []
        if len_prefix > 0:
            start = 0
            while start <= n - len_prefix:
                idx = s.find(prefix, start)
                if idx == -1:
                    break
                prefix_starts.append(idx)
                start = idx + 1
        else:
            # Empty prefix matches at every position from 0 to n
            # But we only need to consider positions where the rest can fit
            # Actually, for empty prefix, it can start at any index from 0 to n
            # But we'll handle it by having prefix_starts be all indices 0..n
            # However, to be consistent, we can generate them
            prefix_starts = list(range(n + 1))  # prefix of length 0 can start at 0..n
        
        # Find all starting indices of suffix in s
        suffix_starts = []
        if len_suffix > 0:
            start = 0
            while start <= n - len_suffix:
                idx = s.find(suffix, start)
                if idx == -1:
                    break
                suffix_starts.append(idx)
                start = idx + 1
        else:
            # Empty suffix: can start at any index from 0 to n
            suffix_starts = list(range(n + 1))
        
        # If no prefix or suffix found, return -1
        if not prefix_starts or not suffix_starts:
            return -1
        
        # Find all starting indices of middle in s
        middle_starts = []
        if len_middle > 0:
            start = 0
            while start <= n - len_middle:
                idx = s.find(middle, start)
                if idx == -1:
                    break
                middle_starts.append(idx)
                start = idx + 1
        # If middle is empty, we don't need to store starts; we'll handle it specially
        
        # Precompute earliest_middle_end: for each index k, what is the minimum end (start + len) 
        # of a middle occurrence that starts at or after k.
        # If middle is empty, then for any k, the "end" is k (since it matches empty string at k, ending at k).
        if len_middle == 0:
            # For empty middle, the earliest end from k is k itself.
            # So required_suffix_start = max(gap_start, gap_start) = gap_start
            # We can skip the array and just use gap_start
            min_end_from = None  # marker for empty middle
        else:
            min_end_from = [float('inf')] * (n + 1)
            # For each middle start, set the end
            for m in middle_starts:
                end = m + len_middle
                if end < min_end_from[m]:
                    min_end_from[m] = end
            # Backward pass: min_end_from[i] = min(min_end_from[i], min_end_from[i+1])
            for i in range(n - 1, -1, -1):
                if min_end_from[i+1] < min_end_from[i]:
                    min_end_from[i] = min_end_from[i+1]
        
        result = float('inf')
        
        # For each prefix start, find the best suffix start
        for i_p in prefix_starts:
            # The prefix ends at i_p + len_prefix - 1, so the next character is at i_p + len_prefix
            gap_start = i_p + len_prefix
            
            # The suffix must start at or after gap_start
            # Also, if middle is not empty, the suffix must start at or after the earliest middle end from gap_start
            if len_middle == 0:
                required_suffix_start = gap_start
            else:
                if gap_start > n:
                    break
                me = min_end_from[gap_start]
                if me == float('inf'):
                    # No middle found from gap_start onwards
                    continue
                required_suffix_start = max(gap_start, me)
            
            # Find the smallest suffix start >= required_suffix_start
            # suffix_starts is sorted
            idx_in_suffix = bisect.bisect_left(suffix_starts, required_suffix_start)
            if idx_in_suffix < len(suffix_starts):
                i_s = suffix_starts[idx_in_suffix]
                # The total substring is from i_p to i_s + len_suffix - 1
                length = i_s + len_suffix - i_p
                if length < result:
                    result = length
        
        return result if result != float('inf') else -1