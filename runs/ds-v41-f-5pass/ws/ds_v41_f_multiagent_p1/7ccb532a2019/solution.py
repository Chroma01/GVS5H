class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1
        n = len(s)
        best = n  # target frequency k = 0: delete every character
        C = cnt
        for k in range(1, n + 1):
            c0 = C[0]
            dp0 = c0                 # state: this letter's target count is 0
            dp1 = c0 - k
            if dp1 < 0:
                dp1 = -dp1            # state: this letter's target count is k
            prev = c0
            for i in range(1, 26):
                c = C[i]
                # deficit of letter i when its target is k
                def1 = k - c
                if def1 < 0:
                    def1 = 0
                ab = c - k
                if ab < 0:
                    ab = -ab
                # excess of the previous letter when its target is k
                ep = prev - k
                if ep < 0:
                    ep = 0
                # savings for edges ending in state k:
                #   prev target 0  -> excess = prev
                #   prev target k  -> excess = ep
                s01 = prev if prev < def1 else def1
                s11 = ep if ep < def1 else def1
                base = dp0 if dp0 < dp1 else dp1
                ndp0 = c + base        # target 0 has no deficit -> no saving
                a = dp0 - s01
                b = dp1 - s11
                ndp1 = ab + (a if a < b else b)
                dp0 = ndp0
                dp1 = ndp1
                prev = c
            cur = dp0 if dp0 < dp1 else dp1
            if cur < best:
                best = cur
        return best