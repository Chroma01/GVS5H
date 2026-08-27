class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern into pre, mid, suf based on two '*'
        # p contains exactly two '*'
        parts = p.split('*')
        # parts will be [pre, mid, suf]
        pre = parts[0]
        suf = parts[2]
        
        len_pre = len(pre)
        len_suf = len(suf)
        
        # Case 1: Both pre and suf are empty
        # Pattern is "**", matches empty substring
        if len_pre == 0 and len_suf == 0:
            return 0
        
        # Case 2: Only pre is empty
        # Pattern is "*suf". Shortest match is just "suf" if it exists.
        if len_pre == 0:
            if suf in s:
                return len_suf
            else:
                return -1
        
        # Case 3: Only suf is empty
        # Pattern is "pre*". Shortest match is just "pre" if it exists.
        if len_suf == 0:
            if pre in s:
                return len_pre
            else:
                return -1
        
        # Case 4: Both pre and suf are non-empty
        # Find all end indices of pre in s
        # An occurrence of pre starting at i ends at i + len_pre - 1
        ends = []
        start = 0
        while True:
            idx = s.find(pre, start)
            if idx == -1:
                break
            ends.append(idx + len_pre - 1)
            start = idx + 1
        
        if not ends:
            return -1
            
        # Find all start indices of suf in s
        starts = []
        start = 0
        while True:
            idx = s.find(suf, start)
            if idx == -1:
                break
            starts.append(idx)
            start = idx + 1
            
        if not starts:
            return -1
            
        # Two pointers to find min length
        # We need end < start (prefix ends before suffix starts)
        # The substring spans from (end - len_pre + 1) to (start + len_suf - 1)
        # Length = (start + len_suf - 1) - (end - len_pre + 1) + 1
        #        = start - end + len_suf + len_pre - 1
        
        min_len = float('inf')
        j = 0
        n_starts = len(starts)
        
        for i in range(len(ends)):
            end_val = ends[i]
            # Find smallest start_val > end_val
            # Since 'starts' is sorted, we can advance j
            while j < n_starts and starts[j] <= end_val:
                j += 1
            
            if j < n_starts:
                start_val = starts[j]
                # Calculate length
                current_len = start_val - end_val + len_pre + len_suf - 1
                if current_len < min_len:
                    min_len = current_len
        
        return min_len if min_len != float('inf') else -1