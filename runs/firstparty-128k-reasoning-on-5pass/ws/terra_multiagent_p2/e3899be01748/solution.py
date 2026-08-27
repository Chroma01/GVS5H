class Solution:
    def countSubstrings(self, s: str) -> int:
        # dp[m][r] = count of substrings ending at the previous position
        # with value congruent to r modulo m.
        dp = [None] + [[0] * m for m in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')

            for m in range(1, 10):
                previous = dp[m]
                current = [0] * m

                for remainder, count in enumerate(previous):
                    if count:
                        current[(remainder * 10 + digit) % m] += count

                current[digit % m] += 1
                dp[m] = current

            if digit != 0:
                answer += dp[digit][0]

        return answer