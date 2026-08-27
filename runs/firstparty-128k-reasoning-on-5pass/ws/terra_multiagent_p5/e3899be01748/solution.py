class Solution:
    def countSubstrings(self, s: str) -> int:
        # rem[d][r] = count of substrings ending at the previous position
        # whose numeric value has remainder r modulo d.
        rem = [None] + [[0] * d for d in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')

            for d in range(1, 10):
                old = rem[d]
                new = [0] * d

                for r, count in enumerate(old):
                    if count:
                        new[(r * 10 + digit) % d] += count

                # Start the one-character substring at this position.
                new[digit % d] += 1
                rem[d] = new

            # Substrings ending in zero are excluded.
            if digit:
                answer += rem[digit][0]

        return answer