class Solution:
    def countSubstrings(self, s: str) -> int:
        # counts[d][r] = number of substrings ending at the previous
        # position whose value is congruent to r modulo d.
        counts = [[0] * d for d in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')

            for d in range(1, 10):
                old = counts[d - 1]
                new = [0] * d

                # Extend every substring ending at the previous position.
                for remainder, amount in enumerate(old):
                    new[(remainder * 10 + digit) % d] += amount

                # Start the one-digit substring at this position.
                new[digit % d] += 1
                counts[d - 1] = new

                # Only substrings ending in digit d are tested modulo d.
                if digit == d:
                    answer += new[0]

        return answer