class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        s2 = str2.encode()
        word = bytearray(b'a' * L)
        pinned = bytearray(L)

        # ---------- Z-function of str2 (O(1) period tests) ----------
        z = [0] * m
        z[0] = m
        l = r = 0
        for i in range(1, m):
            k = 0
            if i < r:
                k = r - i
                if z[i - l] < k:
                    k = z[i - l]
            while i + k < m and s2[k] == s2[i + k]:
                k += 1
            z[i] = k
            if i + k > r:
                l = i
                r = i + k

        # ---------- Stage 1: place every T-pinned window ----------
        # Two overlapping T's at distance d < m are compatible iff d is a period
        # of str2  <=>  z[d] >= m - d.  Checking consecutive T's suffices, since
        # for p<q<r the overlap of windows p and r lies inside window q.
        prev_t = -1
        end = 0                        # first index not yet painted
        for t in range(n):
            if str1[t] == 'T':
                if prev_t >= 0:
                    d = t - prev_t
                    if d < m and z[d] < m - d:
                        return ""
                st = end if end > t else t
                if st < t + m:
                    word[st:t + m] = s2[st - t:]
                    pinned[st:t + m] = b'\x01' * (t + m - st)
                    end = t + m
                prev_t = t

        # ---------- prev_free[x] = largest index <= x that is not T-pinned ----------
        prev_free = [-1] * L
        last = -1
        for x in range(L):
            if not pinned[x]:
                last = x
            prev_free[x] = last

        # ---------- Stage 2: repair violated F windows (left -> right) ----------
        while True:
            changed = False
            i = 0
            while i < n:
                p = word.find(s2, i)
                if p < 0 or p >= n:
                    break
                if str1[p] == 'T':
                    i = p + 1
                    continue
                # F window at p currently equals str2 -> must break it
                j = prev_free[p + m - 1]     # rightmost modifiable cell in window
                if j < p:
                    return ""                # whole window is T-pinned: impossible
                c = word[j] + 1
                if c == s2[j - p]:
                    c += 1
                if c > 122:                  # ord('z')
                    return ""
                word[j] = c
                changed = True
                i = p                        # window p is broken now; go on from p
            if not changed:
                break

        return word.decode()