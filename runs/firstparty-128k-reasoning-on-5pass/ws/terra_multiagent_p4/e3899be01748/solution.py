class Solution:
    def countSubstrings(self, s: str) -> int:
        states = [None] + [[0] * d for d in range(1, 10)]
        answer = 0

        for ch in s:
            digit = ord(ch) - ord('0')

            for d in range(1, 10):
                old = states[d]
                new = [0] * d

                for remainder, count in enumerate(old):
                    if count:
                        new[(remainder * 10 + digit) % d] += count

                new[digit % d] += 1
                states[d] = new

            if digit:
                answer += states[digit][0]

        return answer