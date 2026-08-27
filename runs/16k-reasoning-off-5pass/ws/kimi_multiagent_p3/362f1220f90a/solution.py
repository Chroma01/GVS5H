from collections import deque

class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L
        forced = [False] * L

        # Apply all 'T' constraints
        for i, ch in enumerate(str1):
            if ch == 'T':
                base = i
                for j in range(m):
                    p = base + j
                    c = str2[j]
                    if word[p] is None:
                        word[p] = c
                        forced[p] = True
                    elif word[p] != c:
                        return ""

        # Fill remaining positions with 'a'
        for k in range(L):
            if word[k] is None:
                word[k] = 'a'

        # Helper to check if window starting at i equals str2
        def matches(i: int) -> bool:
            base = i
            for j in range(m):
                if word[base + j] != str2[j]:
                    return False
            return True

        # Queue of F-window start indices that may currently match str2.
        # Initially all F indices; after editing position pos, only windows
        # with start in [pos - m + 1, pos] can be affected.
        dq = deque(i for i, ch in enumerate(str1) if ch == 'F')
        in_queue = [False] * n
        for i in dq:
            in_queue[i] = True

        while dq:
            i = dq.popleft()
            in_queue[i] = False
            if not matches(i):
                continue
            # Window i matches str2 but str1[i] == 'F': must break it.
            # Choose the rightmost free position whose char can be increased
            # (target < 'z'); scan leftward as fallback.
            pos = -1
            for j in range(m - 1, -1, -1):
                p = i + j
                if not forced[p]:
                    if str2[j] < 'z':
                        pos = p
                        break
                    # str2[j] == 'z': word[p] == 'z' (window matches),
                    # cannot increase here; keep scanning left.
            if pos == -1:
                return ""  # no free position can break the match
            # Minimal monotonic increase that breaks the match at pos.
            # Since window matches, word[pos] == str2[pos - i].
            word[pos] = chr(ord(str2[pos - i]) + 1)
            # Re-enqueue all F-windows containing pos (start in [pos-m+1, pos])
            lo = pos - m + 1
            if lo < 0:
                lo = 0
            hi = pos if pos < n else n - 1
            for s in range(lo, hi + 1):
                if str1[s] == 'F' and not in_queue[s]:
                    in_queue[s] = True
                    dq.append(s)

        return "".join(word)