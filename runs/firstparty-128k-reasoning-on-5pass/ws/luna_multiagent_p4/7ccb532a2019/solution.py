class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1

        answer = n  # Delete every character.

        # Try every positive common frequency.
        for k in range(1, n + 1):
            # dp[0/1]: minimum cost after processing the current prefix,
            # where the current character is absent/present in the target.
            dp = [
                abs(count[0] - 0),
                abs(count[0] - k),
            ]

            for i in range(1, 26):
                absent_cost = abs(count[i])
                present_cost = abs(count[i] - k)

                # Reward for changing one character from i-1 to i.
                # Such a change saves one operation compared with deleting
                # the old character and inserting the new one.
                reward_00 = 0
                reward_01 = min(
                    max(count[i - 1], 0),
                    max(k - count[i], 0),
                )
                reward_10 = 0
                reward_11 = min(
                    max(count[i - 1] - k, 0),
                    max(k - count[i], 0),
                )

                ndp0 = min(
                    dp[0] + absent_cost - reward_00,
                    dp[1] + absent_cost - reward_10,
                )
                ndp1 = min(
                    dp[0] + present_cost - reward_01,
                    dp[1] + present_cost - reward_11,
                )
                dp = [ndp0, ndp1]

            answer = min(answer, dp[0], dp[1])

        return answer