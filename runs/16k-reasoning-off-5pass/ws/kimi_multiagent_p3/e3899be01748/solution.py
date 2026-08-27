class Solution:
    def countSubstrings(self, s: str) -> int:
        # cnt[d][r] = number of substrings ending at the previous position
        # whose value mod d == r, for d in 1..9.
        cnt = [None] + [[0] * d for d in range(1, 10)]
        ans = 0
        for ch in s:
            x = ord(ch) - 48  # int(ch)
            nxt = [None] + [[0] * d for d in range(1, 10)]
            for d in range(1, 10):
                cd = cnt[d]
                nd = nxt[d]
                # Every substring ending at the previous position extends by x:
                # new value = old * 10 + x, so new remainder = (r*10 + x) % d.
                for r in range(d):
                    c = cd[r]
                    if c:
                        nd[(r * 10 + x) % d] += c
                # The length-1 substring consisting of just this digit.
                nd[x % d] += 1
            # Substrings ending here are valid iff last digit x != 0 and value % x == 0.
            if x != 0:
                ans += nxt[x][0]
            cnt = nxt
        return ans