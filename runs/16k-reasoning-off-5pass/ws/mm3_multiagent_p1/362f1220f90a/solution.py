class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        
        # For each position j in the result word, collect constraints
        # Each constraint: (i, offset, char) where i is the index in str1,
        # offset is the index in str2 (j - i), and char is str2[offset]
        # T constraints require word[j] == char
        # F constraints require word[j] != char unless a prefix mismatch exists
        constraints = [[] for _ in range(L)]
        for i in range(n):
            for offset in range(m):
                j = i + offset
                if j >= L:
                    break
                constraints[j].append((i, offset, str2[offset]))
        
        word = [''] * L
        
        for j in range(L):
            # Determine if there's a forced character from T constraints
            forced = None
            for i, off, ch in constraints[j]:
                if str1[i] == 'T':
                    if forced is None:
                        forced = ch
                    elif forced != ch:
                        return ""  # Conflicting T constraints
            
            # Try characters from 'a' to 'z'
            found = False
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if forced is not None and c != forced:
                    continue
                
                # Check if this candidate works
                valid = True
                for i, off, ch in constraints[j]:
                    if str1[i] == 'T':
                        if c != ch:
                            valid = False
                            break
                    else:  # F constraint
                        if c == ch:
                            # Check if there's already a mismatch in the prefix of this substring
                            prefix_mismatch = False
                            for k in range(i, j):
                                if word[k] != '' and word[k] != str2[k - i]:
                                    prefix_mismatch = True
                                    break
                            if not prefix_mismatch:
                                valid = False
                                break
                
                if valid:
                    word[j] = c
                    found = True
                    break
            
            if not found:
                return ""
        
        return ''.join(word)