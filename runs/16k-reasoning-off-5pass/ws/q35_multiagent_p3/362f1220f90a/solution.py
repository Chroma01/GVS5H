class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total_len = n + m - 1
        
        # Step 1: Determine forced characters from 'T' constraints
        # forced[j] will store the character that must be at word[j], or None if not forced
        forced = [None] * total_len
        
        for i in range(n):
            if str1[i] == 'T':
                for k in range(m):
                    j = i + k
                    c = str2[k]
                    if forced[j] is not None and forced[j] != c:
                        return ""
                    forced[j] = c
        
        # Step 2: For each 'F' constraint, we need to track how many positions in the window match str2.
        # match_count[i] for i in range(n) where str1[i]=='F' stores the number of positions in word[i:i+m] that equal str2[k].
        # We'll use an array of size n, but only care about indices where str1[i]=='F'.
        match_count = [0] * n
        
        # Initialize match_count for all F windows based on forced characters
        # For each F window i, count how many k in [0, m-1] have forced[i+k] == str2[k]
        # Note: For positions not forced, they don't contribute to match_count initially (they are not matching yet)
        # But actually, we should only count forced positions that match. Unforced positions are not set, so they don't match yet.
        # However, when we set a character, we need to update the counts.
        
        # Precompute which F windows cover each position j in word
        # f_windows[j] = list of i such that str1[i]=='F' and i <= j < i+m
        f_windows = [[] for _ in range(total_len)]
        for i in range(n):
            if str1[i] == 'F':
                for k in range(m):
                    j = i + k
                    if j < total_len:
                        f_windows[j].append(i)
        
        # Initialize match_count for F windows
        for i in range(n):
            if str1[i] == 'F':
                cnt = 0
                for k in range(m):
                    j = i + k
                    if forced[j] is not None and forced[j] == str2[k]:
                        cnt += 1
                match_count[i] = cnt
        
        # Step 3: Build the word greedily
        word = [None] * total_len
        
        for j in range(total_len):
            # Determine the character to place at word[j]
            if forced[j] is not None:
                c = forced[j]
            else:
                # Try 'a' to 'z'
                c = None
                for char_code in range(ord('a'), ord('z') + 1):
                    candidate = chr(char_code)
                    # Check if setting word[j] = candidate violates any F constraint
                    # A violation occurs if for some F window i covering j, match_count[i] becomes m
                    # But note: match_count[i] counts matches. When we set word[j], we need to:
                    # 1. If word[j] was previously set (it shouldn't be, since we go left to right), subtract its contribution.
                    # 2. Add contribution of candidate.
                    # 3. Check if any match_count[i] == m for i in f_windows[j]
                    
                    # Since we are building left to right, word[j] is currently None.
                    # So we just need to check: for each F window i covering j,
                    # new_match_count = match_count[i] + (1 if candidate == str2[j-i] else 0)
                    # If new_match_count == m, then this candidate is invalid for that window.
                    
                    valid = True
                    for i in f_windows[j]:
                        # The position in str2 corresponding to word[j] is j - i
                        k = j - i
                        # k is in [0, m-1] because i <= j < i+m
                        new_cnt = match_count[i]
                        if candidate == str2[k]:
                            new_cnt += 1
                        if new_cnt == m:
                            valid = False
                            break
                    if valid:
                        c = candidate
                        break
                
                if c is None:
                    return ""
            
            word[j] = c
            
            # Update match_count for all F windows covering j
            for i in f_windows[j]:
                k = j - i
                if c == str2[k]:
                    match_count[i] += 1
        
        return "".join(word)