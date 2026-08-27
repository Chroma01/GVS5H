class Solution:
    def countSubstrings(self, s: str) -> int:
        # dp[m][r] is the number of substrings ending at the
        # previous position whose value has remainder r modulo m.
        dp = [[0] * m for m in range(10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')
            new_dp = [[0] * m for m in range(10)]

            for modulus in range(1, 10):
                current = dp[modulus]
                updated = new_dp[modulus]

                # Extend all substrings ending at the previous position.
                for remainder, count in enumerate(current):
                    if count:
                        new_remainder = (remainder * 10 + digit) % modulus
                        updated[new_remainder] += count

                # Start the one-character substring at this position.
                updated[digit % modulus] += 1

            dp = new_dp

            # Only nonzero last digits define a valid divisor.
            if digit != 0:
                answer += dp[digit][0]

        return answer