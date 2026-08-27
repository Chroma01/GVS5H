class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1

        n = len(s)
        answer = n  # Delete every character.

        # No useful positive target frequency exceeds the largest existing count.
        for k in range(1, max(cnt) + 1):
            # dp[state]: minimum cost after processing the current prefix.
            # state 0 means the current letter is absent; state 1 means it
            # occurs exactly k times.
            c = cnt[0]
            dp0 = c
            dp1 = abs(c - k)

            for i in range(1, 26):
                prev = cnt[i - 1]
                cur = cnt[i]

                # Surplus characters at the previous letter can be changed
                # into the next letter, saving one operation compared with
                # deleting and inserting.
                surplus0 = prev
                surplus1 = max(prev - k, 0)
                deficit0 = 0
                deficit1 = max(k - cur, 0)

                cost0 = cur
                cost1 = abs(cur - k)

                ndp0 = min(
                    dp0 + cost0,  # previous absent -> current absent
                    dp1 + cost0 - min(surplus1, deficit0),
                )
                ndp1 = min(
                    dp0 + cost1 - min(surplus0, deficit1),
                    dp1 + cost1 - min(surplus1, deficit1),
                )

                dp0, dp1 = ndp0, ndp1

            answer = min(answer, dp0, dp1)

        return answer