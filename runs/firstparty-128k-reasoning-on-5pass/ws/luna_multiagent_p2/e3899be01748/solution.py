class Solution:
    def countSubstrings(self, s: str) -> int:
        # dp[m][r] is the number of substrings ending at the
        # previous position whose value has remainder r modulo m.
        dp = [[0] * m for m in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')

            for m in range(1, 10):
                old = dp[m - 1]
                new = [0] * m

                # Extend every substring ending at the previous position.
                for remainder, count in enumerate(old):
                    new[(remainder * 10 + digit) % m] += count

                # Start a new one-character substring at this digit.
                new[digit % m] += 1
                dp[m - 1] = new

            # All substrings ending here are now represented in dp[digit - 1].
            if digit != 0:
                answer += dp[digit - 1][0]

        return answer