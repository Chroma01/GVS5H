class Solution:
    def countSubstrings(self, s: str) -> int:
        # dp[d][r] = number of substrings ending at the previous position
        # whose value has remainder r modulo d.
        dp = [None] + [[0] * d for d in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')

            for d in range(1, 10):
                old = dp[d]
                new = [0] * d

                for remainder, count in enumerate(old):
                    if count:
                        new[(remainder * 10 + digit) % d] += count

                # Start the one-digit substring at this position.
                new[digit % d] += 1
                dp[d] = new

            # A substring is counted only when its final digit is non-zero.
            if digit != 0:
                answer += dp[digit][0]

        return answer