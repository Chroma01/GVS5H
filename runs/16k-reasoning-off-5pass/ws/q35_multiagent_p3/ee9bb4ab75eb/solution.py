class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        # Create a list of (word, original_index) and sort by word
        # Using stable sort to keep original indices consistent for duplicates
        indexed_words = [(w, i) for i, w in enumerate(words)]
        indexed_words.sort(key=lambda x: x[0])
        
        # Extract sorted words
        sorted_words = [w for w, i in indexed_words]
        
        # Precompute LCP between adjacent words in sorted array
        # lcp_arr[i] = LCP(sorted_words[i], sorted_words[i+1])
        def get_lcp(s1, s2):
            min_len = min(len(s1), len(s2))
            i = 0
            while i < min_len and s1[i] == s2[i]:
                i += 1
            return i
        
        lcp_arr = []
        for i in range(n - 1):
            lcp_arr.append(get_lcp(sorted_words[i], sorted_words[i+1]))
        
        # If k == 1, the answer is the max length of any word in the remaining array
        # But note: the problem says "longest common prefix among any k strings"
        # For k=1, any single string has LCP equal to its own length.
        # So we need the max word length in the remaining array.
        if k == 1:
            # Precompute max word length
            max_len = 0
            for w in words:
                if len(w) > max_len:
                    max_len = len(w)
            # When removing a word, if it was the unique max, the max might drop
            # We need to handle this carefully.
            # Actually, for k=1, the answer for removal of word at index i is the max length
            # of any word in words excluding words[i].
            # We can precompute the two largest lengths.
            # But let's stick to the general method below for consistency, or handle separately.
            # The general method below works for k>=2. For k=1, the window size in lcp_arr is 0.
            # Let's handle k=1 separately for clarity and efficiency.
            # Count frequencies of lengths? Or just precompute top 2.
            lengths = [len(w) for w in words]
            # Find the two largest lengths
            max1 = -1
            max2 = -1
            for l in lengths:
                if l > max1:
                    max2 = max1
                    max1 = l
                elif l > max2:
                    max2 = l
            # For each removal, if the word removed has length == max1 and it's the only one with that length,
            # then the new max is max2, else max1.
            # But we need to know how many words have length max1.
            from collections import Counter
            len_count = Counter(lengths)
            res = []
            for l in lengths:
                if l == max1 and len_count[max1] == 1:
                    res.append(max2 if max2 != -1 else 0)
                else:
                    res.append(max1)
            return res
        
        # For k >= 2:
        # M[i] = min(lcp_arr[i], lcp_arr[i+1], ..., lcp_arr[i+k-2])
        # This is the LCP of the window of k words starting at sorted index i.
        # Valid i ranges from 0 to n - k.
        
        # Compute M array using a sliding window minimum of size k-1 over lcp_arr
        # lcp_arr has size n-1. We need windows of size k-1.
        # If k-1 > n-1, then no window exists, but since n >= k, n-1 >= k-1, so it's fine.
        
        # Use deque for sliding window minimum
        from collections import deque
        dq = deque()
        M = [0] * (n - k + 1)  # M[i] corresponds to window starting at i in sorted_words
        
        # We want min of lcp_arr[i : i+k-1] for i in 0..n-k
        # lcp_arr indices: 0 to n-2
        # Window size: k-1
        
        # Initialize deque for first window
        for i in range(k - 1):
            while dq and lcp_arr[dq[-1]] >= lcp_arr[i]:
                dq.pop()
            dq.append(i)
        
        M[0] = lcp_arr[dq[0]]
        
        for i in range(1, n - k + 1):
            # Remove indices out of current window [i, i+k-2]
            if dq and dq[0] == i - 1:
                dq.popleft()
            # Add new element at i+k-2
            idx = i + k - 2
            while dq and lcp_arr[dq[-1]] >= lcp_arr[idx]:
                dq.pop()
            dq.append(idx)
            M[i] = lcp_arr[dq[0]]
            
        # Now, for each removal of a word at original index, we need to find the max M[i]
        # for valid windows that don't include the removed word.
        
        # Map each original index to its position in the sorted array
        sorted_pos = [0] * n
        for pos, (w, orig_idx) in enumerate(indexed_words):
            sorted_pos[orig_idx] = pos
            
        # Precompute prefix max and suffix max for M
        # prefix_max[i] = max(M[0], M[1], ..., M[i])
        # suffix_max[i] = max(M[i], M[i+1], ..., M[n-k])
        prefix_max = [0] * (n - k + 1)
        suffix_max = [0] * (n - k + 1)
        
        prefix_max[0] = M[0]
        for i in range(1, n - k + 1):
            prefix_max[i] = max(prefix_max[i-1], M[i])
            
        suffix_max[n - k] = M[n - k]
        for i in range(n - k - 1, -1, -1):
            suffix_max[i] = max(suffix_max[i+1], M[i])
            
        ans = [0] * n
        
        for orig_idx in range(n):
            p = sorted_pos[orig_idx]  # position in sorted array
            
            # The removed word is at sorted position p.
            # Valid windows are those that do not include word at p.
            # A window starting at i covers words i to i+k-1.
            # It is invalid if i <= p <= i+k-1.
            # So valid i are: i <= p - k  OR  i >= p + 1
            
            # Range 1: i from 0 to p - k (if p - k >= 0)
            # Range 2: i from p + 1 to n - k (if p + 1 <= n - k)
            
            res = 0
            
            # Check range 1
            if p - k >= 0:
                res = max(res, prefix_max[p - k])
                
            # Check range 2
            if p + 1 <= n - k:
                res = max(res, suffix_max[p + 1])
                
            ans[orig_idx] = res
            
        return ans