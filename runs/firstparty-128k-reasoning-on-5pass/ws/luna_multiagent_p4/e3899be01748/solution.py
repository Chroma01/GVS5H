class Solution:
    def countSubstrings(self, s: str) -> int:
        # states[d][r] = number of substrings ending at the previous
        # position whose value is congruent to r modulo d.
        states = [None] + [[0] * d for d in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')

            for d in range(1, 10):
                old = states[d]
                updated = [0] * d

                for residue, count in enumerate(old):
                    updated[(residue * 10 + digit) % d] += count

                # The one-digit substring consisting of the current digit.
                updated[digit % d] += 1
                states[d] = updated

            if digit != 0:
                answer += states[digit][0]

        return answer