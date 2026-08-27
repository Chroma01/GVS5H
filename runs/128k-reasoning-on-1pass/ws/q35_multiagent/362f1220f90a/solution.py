class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        
        word = [None] * L
        match_count = [0] * n
        
        # Process 'T' constraints to fix characters
        for i in range(n):
            if str1[i] == 'T':
                for k in range(m):
                    pos = i + k
                    char = str2[k]
                    if word[pos] is not None and word[pos] != char:
                        return ""
                    word[pos] = char
        
        # Initialize match_count for 'F' windows based on fixed characters
        for i in range(n):
            if str1[i] == 'F':
                cnt = 0
                for k in range(m):
                    pos = i + k
                    if word[pos] is not None and word[pos] == str2[k]:
                        cnt += 1
                match_count[i] = cnt
                # If 'T' constraints already force an 'F' window to match str2, it's invalid
                if cnt == m:
                    return ""
        
        # Greedily fill remaining positions
        for j in range(L):
            if word[j] is not None:
                continue
            
            # Determine forbidden characters at position j
            forbidden = set()
            start_i = max(0, j - m + 1)
            end_i = min(j, n - 1)
            for i in range(start_i, end_i + 1):
                # If an 'F' window has m-1 matches, the current char cannot complete the match
                if str1[i] == 'F' and match_count[i] == m - 1:
                    forbidden.add(str2[j - i])
            
            # Pick the lexicographically smallest valid character
            chosen = None
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c not in forbidden:
                    chosen = c
                    break
            
            if chosen is None:
                return ""
            
            word[j] = chosen
            
            # Update match_count for affected 'F' windows
            for i in range(start_i, end_i + 1):
                if str1[i] == 'F':
                    if chosen == str2[j - i]:
                        match_count[i] += 1
                        # Safety check; forbidden logic should prevent this
                        if match_count[i] == m:
                            return ""
        
        return "".join(word)