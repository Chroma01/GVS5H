class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        # Step 1: Compute prefix counts across all words
        cnt = {}
        for w in words:
            for j in range(1, len(w) + 1):
                p = w[:j]
                cnt[p] = cnt.get(p, 0) + 1
        
        # Step 2: Compute max1[L] and max2[L] for each length L
        max_len = max(len(w) for w in words)
        max1 = [0] * (max_len + 1)
        max2 = [0] * (max_len + 1)
        
        for p, c in cnt.items():
            L = len(p)
            if c > max1[L]:
                max2[L] = max1[L]
                max1[L] = c
            elif c == max1[L]:
                max2[L] = c
            elif c > max2[L]:
                max2[L] = c
                
        # Step 3: Identify universally valid lengths (U_max) and special lengths
        special_lengths = []
        U_max = 0
        for L in range(1, max_len + 1):
            if max1[L] >= k:
                # If the second highest count is also >= k, then even after removing 
                # the word with the best prefix, another prefix of length L remains valid.
                if max2[L] >= k:
                    U_max = max(U_max, L)
                else:
                    special_lengths.append(L)
                    
        special_lengths.sort(reverse=True)
        
        # Step 4: Initialize B array with U_max
        B = [U_max] * n
        
        # Step 5: Build mapping from special length to list of word indices having that prefix
        special_indices = {}
        special_set = set(special_lengths)
        for i, w in enumerate(words):
            for j in range(1, len(w) + 1):
                if j in special_set:
                    if j not in special_indices:
                        special_indices[j] = []
                    special_indices[j].append(i)
                    
        # Step 6: Process special lengths to update B
        # We maintain a list of 'active' indices that haven't been assigned a B value yet.
        # For each special length L (descending), if a word's index is NOT in the set of 
        # words having the unique best prefix of length L, then L is valid for that word.
        active = list(range(n))
        for L in special_lengths:
            if L <= U_max:
                break
            if L not in special_indices:
                continue
            S_L = set(special_indices[L])
            new_active = []
            for i in active:
                if i not in S_L:
                    B[i] = L
                else:
                    new_active.append(i)
            active = new_active
            if not active:
                break
                
        # Step 7: Compute A array
        # A[i] is the longest prefix of words[i] that has global frequency >= k+1
        A = [0] * n
        for i, w in enumerate(words):
            for j in range(1, len(w) + 1):
                p = w[:j]
                if cnt[p] >= k + 1:
                    A[i] = j
                else:
                    # Since counts are non-increasing for longer prefixes, we can break early
                    break
                    
        # Step 8: Combine results
        return [max(A[i], B[i]) for i in range(n)]