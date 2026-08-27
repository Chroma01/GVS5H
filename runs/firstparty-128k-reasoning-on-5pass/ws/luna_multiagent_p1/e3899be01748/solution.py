class Solution:
    def countSubstrings(self, s: str) -> int:
        # dp[m - 1][r] = number of substrings ending at the previous
        # position whose value has remainder r modulo m.
        dp = [[0] * m for m in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')
            new_dp = []

            for m in range(1, 10):
                counts = [0] * m

                # Start a new one-character substring.
                counts[digit % m] = 1

                # Extend every substring ending at the previous position.
                for remainder, amount in enumerate(dp[m - 1]):
                    new_remainder = (remainder * 10 + digit) % m
                    counts[new_remainder] += amount

                new_dp.append(counts)

            dp = new_dp

            # Substrings ending in zero are not considered.
            if digit != 0:
                answer += dp[digit - 1][0]

        return answer