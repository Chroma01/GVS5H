class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        freq = [0] * 26

        for ch in s:
            freq[ord(ch) - ord('a')] += 1

        # Deleting all characters is always a safe upper bound.
        answer = n

        for k in range(1, n + 1):
            # Target count for each letter is either 0 or k.
            d0 = freq[0]       # discrepancy when target is 0
            d1 = freq[0] - k   # discrepancy when target is k

            dp0 = abs(d0)
            dp1 = abs(d1)

            for i in range(1, 26):
                cur_d0 = freq[i]
                cur_d1 = freq[i] - k

                # If the current letter is retained, it may receive
                # useful changes from the previous letter.
                need = max(-cur_d1, 0)

                # Previous target is 0.
                benefit0 = min(max(d0, 0), need)

                # Previous target is k.
                benefit1 = min(max(d1, 0), need)

                # Current target is 0: it never needs incoming changes.
                ndp0 = cur_d0 + min(dp0, dp1)

                # Current target is k.
                ndp1 = abs(cur_d1) + min(
                    dp0 - benefit0,
                    dp1 - benefit1
                )

                dp0, dp1 = ndp0, ndp1
                d0, d1 = cur_d0, cur_d1

            answer = min(answer, dp0, dp1)

        return answer