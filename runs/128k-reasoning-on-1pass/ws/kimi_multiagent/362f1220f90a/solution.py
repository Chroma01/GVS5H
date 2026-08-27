class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        s2 = list(str2)
        word = [None] * L

        # 1) Overlay str2 at every 'T' index; a conflicting overwrite => impossible.
        for i in range(n):
            if str1[i] == 'T':
                for k in range(m):
                    p = i + k
                    c = word[p]
                    if c is None:
                        word[p] = s2[k]
                    elif c != s2[k]:
                        return ""

        # 2)+3) Fill free slots with 'a' and build prevFree:
        # prevFree[p] = rightmost index <= p not forced by any 'T' (-1 if none).
        # Forced/free status is static (fixes below never change it), so one pass suffices.
        prevFree = [-1] * L
        last = -1
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'
                last = p
            prevFree[p] = last

        # 4) Scan F windows left to right; break any accidental match at the
        # window's rightmost free cell using the smallest char != str2 at that offset.
        for i in range(n):
            if str1[i] == 'F' and word[i:i + m] == s2:
                p = prevFree[i + m - 1]
                if p < i:  # no free cell inside window i -> cannot break the match
                    return ""
                word[p] = 'b' if s2[p - i] == 'a' else 'a'

        return ''.join(word)