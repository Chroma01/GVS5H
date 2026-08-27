class Solution:
    def countSubstrings(self, s: str) -> int:
        # counts[d][r] is the number of substrings ending at the previous
        # position whose numeric value has remainder r modulo d.
        counts = [None] + [[0] * d for d in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')
            updated = [None] + [[0] * d for d in range(1, 10)]

            for d in range(1, 10):
                previous = counts[d]
                current = updated[d]

                for remainder, frequency in enumerate(previous):
                    if frequency:
                        current[(remainder * 10 + digit) % d] += frequency

                current[digit % d] += 1

            counts = updated

            if digit != 0:
                answer += counts[digit][0]

        return answer