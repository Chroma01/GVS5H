class Solution:
    _TRANS = [[[(10 * r + x) % d for r in range(d)] for d in range(1, 10)] for x in range(10)]
    _MODS = [[x % d for d in range(1, 10)] for x in range(10)]
    _DIGITS = range(1, 10)

    def countSubstrings(self, s: str) -> int:
        trans = self._TRANS
        mods = self._MODS
        digits = self._DIGITS

        freq = [None] + [[0] * d for d in digits]
        ans = 0

        for ch in s:
            x = ord(ch) - 48
            tx = trans[x]
            mx = mods[x]
            new_freq = [None] * 10

            for d in digits:
                old = freq[d]
                nf = [0] * d
                t = tx[d - 1]

                for r, c in enumerate(old):
                    if c:
                        nf[t[r]] += c

                nf[mx[d - 1]] += 1
                new_freq[d] = nf

            if x:
                ans += new_freq[x][0]

            freq = new_freq

        return ans