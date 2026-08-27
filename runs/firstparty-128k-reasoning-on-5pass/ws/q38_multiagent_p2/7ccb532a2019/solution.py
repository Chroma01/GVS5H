class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1

        n = len(s)
        ans = n
        neg = -10**18

        for k in range(1, n + 1):
            dp0 = 0
            dp1 = neg

            for i in range(26):
                c = cnt[i]
                keep = c if c < k else k
                rem = k - keep

                if i == 0:
                    avail0 = 0
                    avail1 = 0
                else:
                    prev = cnt[i - 1]
                    avail0 = prev
                    avail1 = prev - k if prev > k else 0

                inc0 = avail0 if avail0 < rem else rem
                inc1 = avail1 if avail1 < rem else rem

                w0 = 2 * keep + inc0 - k
                w1 = 2 * keep + inc1 - k

                ndp0 = dp0 if dp0 > dp1 else dp1
                v0 = dp0 + w0
                v1 = dp1 + w1
                ndp1 = v0 if v0 > v1 else v1

                dp0, dp1 = ndp0, ndp1

                best = dp0 if dp0 > dp1 else dp1
                if best > 0:
                    cost = n - best
                    if cost < ans:
                        ans = cost
                        if ans == 0:
                            return 0

        return ans