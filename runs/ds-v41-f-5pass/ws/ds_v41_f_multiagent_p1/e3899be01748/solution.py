class Solution:
    def countSubstrings(self, s: str) -> int:
        # trans[d][x][r] = (r * 10 + x) % d
        # single[d][x] = x % d
        trans = [None] * 10
        single = [None] * 10
        for d in range(1, 10):
            trans[d] = [[(r * 10 + x) % d for r in range(d)] for x in range(10)]
            single[d] = [x % d for x in range(10)]

        # cnt[d][r] = number of substrings ending at the previous position
        # whose value is congruent to r modulo d. Index 0 is unused.
        cnt = [[0] * d for d in range(10)]
        ans = 0

        for ch in s:
            x = ord(ch) - 48  # last digit of every substring ending here
            for d in range(1, 10):
                old = cnt[d]
                new = [0] * d
                td = trans[d][x]
                for r in range(d):
                    new[td[r]] += old[r]
                new[single[d][x]] += 1  # the single-character substring "x"
                cnt[d] = new

            # Substrings ending here have last digit x and are divisible by x
            # exactly when their value is 0 modulo x. Zero is never a divisor.
            if x:
                ans += cnt[x][0]

        return ans