class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        
        # word as list of chars, fixed[i] = True if position is forced by some 'T'
        word = [None] * L
        fixed = [False] * L
        
        # Apply T constraints
        for i, c in enumerate(str1):
            if c == 'T':
                for j in range(m):
                    pos = i + j
                    ch = str2[j]
                    if word[pos] is None:
                        word[pos] = ch
                        fixed[pos] = True
                    elif word[pos] != ch:
                        return ""
        
        # Fill remaining positions with 'a'
        for i in range(L):
            if word[i] is None:
                word[i] = 'a'
        
        # Helper: check if window [i, i+m) equals str2
        def window_equals_str2(i):
            for j in range(m):
                if word[i + j] != str2[j]:
                    return False
            return True
        
        # Helper: try to find a position in window [i, i+m) that we can increment
        # to make the window != str2 while staying lexicographically minimal.
        # We look from right to left (smallest lex increase).
        def fix_window(i):
            # We need to find k from m-1 down to 0 such that:
            # 1. position i+k is not fixed by any 'T' (so we can change it)
            # 2. word[i+k] != 'z' (can be incremented)
            for k in range(m - 1, -1, -1):
                pos = i + k
                if fixed[pos]:
                    continue
                if word[pos] == 'z':
                    continue
                # Increment this position and reset following positions to 'a' (if not fixed).
                # This is valid because the rightmost change ensures the window becomes > str2.
                new_char = chr(ord(word[pos]) + 1)
                word[pos] = new_char
                for j in range(k + 1, m):
                    p = i + j
                    if not fixed[p]:
                        word[p] = 'a'
                return True
            return False
        
        # Process F constraints
        for i, c in enumerate(str1):
            if c == 'F':
                if window_equals_str2(i):
                    if not fix_window(i):
                        return ""
        
        # Final verification
        for i, c in enumerate(str1):
            window = ''.join(word[i:i+m])
            if c == 'T' and window != str2:
                return ""
            if c == 'F' and window == str2:
                return ""
        
        return ''.join(word)