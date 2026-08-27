class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        
        res = [None] * length
        forced = [False] * length
        
        # Apply all 'T' constraints
        for i in range(n):
            if str1[i] == 'T':
                for j in range(m):
                    pos = i + j
                    if res[pos] is not None and res[pos] != str2[j]:
                        return ""
                    res[pos] = str2[j]
                    forced[pos] = True
        
        # Fill unforced positions with 'a'
        for i in range(length):
            if res[i] is None:
                res[i] = 'a'
        
        # Check and fix 'F' constraints
        for i in range(n):
            if str1[i] == 'F':
                # Check if the window equals str2
                if all(res[i + k] == str2[k] for k in range(m)):
                    # Find the rightmost non-forced character in the window
                    j = i + m - 1
                    while j >= i and forced[j]:
                        j -= 1
                    if j < i:
                        return ""
                    # Change res[j] to the smallest character not equal to str2[j-i]
                    c = 'a'
                    while c == str2[j - i]:
                        c = chr(ord(c) + 1)
                    res[j] = c
        
        return "".join(res)