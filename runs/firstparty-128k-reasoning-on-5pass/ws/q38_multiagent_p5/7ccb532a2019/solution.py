class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        nonzero = [x for x in cnt if x]
        if nonzero and all(x == nonzero[0] for x in nonzero):
            return 0

        best = n - max(cnt)
        if best == 0:
            return 0

        INF = 10**18

        for k in range(1, n + 1):
            dp0 = 0
            dp1 = INF

            for i in range(26):
                ci = cnt[i]

                # Current letter is not used.
                ndp0 = dp0 if dp0 < dp1 else dp1

                # Current letter is used with frequency k.
                base = k - 2 * (ci if ci < k else k)

                if i == 0:
                    ndp1 = dp0 + base
                else:
                    deficit = k - ci
                    if deficit < 0:
                        deficit = 0

                    prev = cnt[i - 1]

                    # Previous letter unused: all prev characters can move to i.
                    save0 = prev if prev < deficit else deficit
                    val0 = dp0 + base - save0

                    # Previous letter used: only excess after keeping k copies can move.
                    excess1 = prev - k
                    if excess1 < 0:
                        excess1 = 0
                    save1 = excess1 if excess1 < deficit else deficit
                    val1 = dp1 + base - save1

                    ndp1 = val0 if val0 < val1 else val1

                dp0, dp1 = ndp0, ndp1

            cur = n + (dp0 if dp0 < dp1 else dp1)
            if cur < best:
                best = cur
                if best == 0:
                    return 0

        return best