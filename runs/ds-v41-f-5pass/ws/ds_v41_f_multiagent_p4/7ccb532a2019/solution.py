class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        maxc = max(cnt)
        best = len(s)  # deleting everything is always a (weak) upper bound

        for f in range(1, maxc + 1):
            # letter 0: no predecessor
            d = cnt[0]            # delete letter 0 entirely
            k = abs(cnt[0] - f)   # keep letter 0 at exactly f
            for i in range(1, 26):
                c = cnt[i]
                pc = cnt[i - 1]
                base = abs(c - f)
                deficit = f - c
                if deficit < 0:
                    deficit = 0
                # surplus available from previous letter
                availD = pc                 # prev deleted -> all its chars usable
                availK = pc - f             # prev kept   -> only surplus usable
                if availK < 0:
                    availK = 0
                recvD = availD if availD < deficit else deficit
                recvK = availK if availK < deficit else deficit

                nd = c + (d if d < k else k)        # current deleted
                cd = d + base - recvD               # current kept, prev deleted
                ck = k + base - recvK               # current kept, prev kept
                nk = cd if cd < ck else ck

                d, k = nd, nk
            if d < best:
                best = d
            if k < best:
                best = k

        return best