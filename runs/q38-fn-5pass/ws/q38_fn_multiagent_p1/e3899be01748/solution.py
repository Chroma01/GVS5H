class Solution:
    def countSubstrings(self, s: str) -> int:
        # trans[d][x][r] = (r * 10 + x) % d
        trans = [[] for _ in range(10)]
        for d in range(1, 10):
            trans[d] = [[(r * 10 + x) % d for r in range(d)] for x in range(10)]

        # mods[d][x] = x % d
        mods = [[0] * 10 for _ in range(10)]
        for d in range(1, 10):
            for x in range(10):
                mods[d][x] = x % d

        # dp[d][r] = number of substrings ending at the previous position
        # whose value is congruent to r modulo d.
        dp = [[0] * d for d in range(10)]
        ans = 0
        divisors = range(1, 10)

        for ch in s:
            x = ord(ch) - 48

            # Build a fresh table to avoid in-place corruption.
            ndp = [[0] * d for d in range(10)]

            for d in divisors:
                old = dp[d]
                new = ndp[d]
                tr = trans[d][x]

                # Extend every substring that ended at the previous position.
                for r, cnt in enumerate(old):
                    if cnt:
                        new[tr[r]] += cnt

                # Add the one-character substring consisting of x.
                new[mods[d][x]] += 1

            dp = ndp

            # If the last digit is non-zero, count substrings ending here
            # that are divisible by that digit.
            if x:
                ans += dp[x][0]

        return ans