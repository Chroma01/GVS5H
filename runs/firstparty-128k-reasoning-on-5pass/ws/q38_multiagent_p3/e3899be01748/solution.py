class Solution:
    TRANS = [[[(r * 10 + x) % d for r in range(d)] for x in range(10)] for d in range(1, 10)]

    def countSubstrings(self, s: str) -> int:
        # cnt[d - 1][r] = number of substrings ending at the current position
        # whose numeric value is congruent to r modulo d.
        cnt = [[0] * d for d in range(1, 10)]
        ans = 0
        trans = self.TRANS

        for ch in s:
            x = ord(ch) - 48

            # Build fresh histograms for all moduli from the previous position.
            for d in range(1, 10):
                old = cnt[d - 1]
                new = [0] * d
                t = trans[d - 1][x]

                # Extend every previous substring by digit x.
                for r, c in enumerate(old):
                    new[t[r]] += c

                # Add the new one-character substring consisting of x.
                new[x % d] += 1

                cnt[d - 1] = new

            # If the current last digit is non-zero, count valid substrings ending here.
            if x != 0:
                ans += cnt[x - 1][0]

        return ans