class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        word = [None] * length
        
        # Step 1: Fill all 'T' constraints
        for i in range(n):
            if str1[i] == 'T':
                # Check for conflicts with already filled characters
                for j in range(m):
                    if word[i + j] is not None and word[i + j] != str2[j]:
                        return ""
                # Fill the window
                for j in range(m):
                    word[i + j] = str2[j]
        
        # Step 2: Check all 'F' constraints to ensure no fully filled window equals str2
        for i in range(n):
            if str1[i] == 'F':
                # Check if this window is fully filled
                is_full = True
                for j in range(m):
                    if word[i + j] is None:
                        is_full = False
                        break
                
                if is_full:
                    # If fully filled, it must not equal str2
                    if word[i:i+m] == str2:
                        return ""
        
        # Step 3: Fill remaining None positions greedily from left to right
        for k in range(length):
            if word[k] is None:
                # Determine the forbidden character if this position completes an 'F' window
                forbidden_char = None
                start_idx = k - m + 1
                if start_idx >= 0 and start_idx < n and str1[start_idx] == 'F':
                    # Check if the prefix of the window (indices start_idx to k-1) matches str2[0..m-2]
                    prefix_matches = True
                    for j in range(m - 1):
                        if word[start_idx + j] != str2[j]:
                            prefix_matches = False
                            break
                    
                    if prefix_matches:
                        # The current position k must not be str2[m-1]
                        forbidden_char = str2[m - 1]
                
                # Try characters 'a' to 'z'
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c == forbidden_char:
                        continue
                    word[k] = c
                    break
                else:
                    # Should not happen if Step 2 passed correctly
                    return ""
        
        return "".join(word)