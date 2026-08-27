class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        ans = n

        for k in range(1, 2 * n + 1):
            c0 = cnt[0]
            dp0 = 0
            dp1 = k - 2 * (c0 if c0 < k else k)

            for i in range(1, 26):
                ci = cnt[i]
                prev = cnt[i - 1]

                same = ci if ci < k else k
                unary1 = k - 2 * same

                deficit1 = k - ci if ci < k else 0
                excess1 = prev - k if prev > k else 0

                new0 = dp0 if dp0 < dp1 else dp1

                save_from0 = prev if prev < deficit1 else deficit1
                save_from1 = excess1 if excess1 < deficit1 else deficit1

                best_prev = dp0 - save_from0
                alt_prev = dp1 - save_from1
                if alt_prev < best_prev:
                    best_prev = alt_prev

                new1 = best_prev + unary1

                dp0, dp1 = new0, new1

            best = dp0 if dp0 < dp1 else dp1
            total = n + best
            if total < ans:
                ans = total
                if ans == 0:
                    break

        return ans