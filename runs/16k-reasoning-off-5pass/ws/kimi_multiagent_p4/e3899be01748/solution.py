class Solution:
    def countSubstrings(self, s: str) -> int:
        # cnt[d][r] = number of suffixes of the processed prefix whose
        # numeric value mod d == r, for d in 1..9.
        cnt = [None] + [[0] * d for d in range(1, 10)]
        ans = 0
        for ch in s:
            x = ord(ch) - 48  # int(ch)
            for d in range(1, 10):
                old = cnt[d]
                new = [0] * d
                # Every existing suffix gets extended by digit x:
                # value' = value * 10 + x  (mod d)
                for r in range(d):
                    c = old[r]
                    if c:
                        new[(r * 10 + x) % d] += c
                # The new single-character suffix "x"
                new[x % d] += 1
                cnt[d] = new
            if x != 0:
                # Substrings ending here qualify iff their value mod x == 0
                ans += cnt[x][0]
        return ans