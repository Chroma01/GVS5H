class Solution:
    def countSubstrings(self, s: str) -> int:
        # dp[m - 1][r] stores the number of substrings ending at the
        # previous position whose value has remainder r modulo m.
        dp = [[0] * m for m in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')
            next_dp = []

            for m in range(1, 10):
                current = [0] * m

                # Extend every substring ending at the previous position.
                for remainder, count in enumerate(dp[m - 1]):
                    if count:
                        new_remainder = (remainder * 10 + digit) % m
                        current[new_remainder] += count

                # Start the one-character substring at this position.
                current[digit % m] += 1
                next_dp.append(current)

            dp = next_dp

            # Only non-zero final digits define a valid divisor.
            if digit != 0:
                answer += dp[digit - 1][0]

        return answer