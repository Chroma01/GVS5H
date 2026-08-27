from math import gcd


class Solution:
    def countSubstrings(self, s: str) -> int:
        # For substring s[i..j] with last digit d != 0:
        #   value(i..j) = value(i..j-1) * 10 + d
        #   d | value(i..j)  <=>  value(i..j-1) * 10 ≡ 0 (mod d)
        #                   <=>  value(i..j-1) ≡ 0 (mod d / gcd(d, 10))
        # Let m = d / gcd(d, 10) ∈ {1, 2, 3, 4, 7, 9}.
        # value(i..j-1) mod m = P_m[j-1] - P_m[i-1] (mod m), where P_m is the
        # prefix remainder. So we need P_m[i-1] == P_m[j-1] for some i-1 in
        # [-1, j-1]. Count with frequency maps of prefix remainders.
        moduli = (2, 3, 4, 7, 9)
        rem = {m: 0 for m in moduli}          # prefix remainder up to j-1
        cnt = {m: {0: 1} for m in moduli}     # include empty prefix (index -1)
        ans = 0
        for j, ch in enumerate(s):
            d = ord(ch) - 48
            if d != 0:
                m = d // gcd(d, 10)
                if m == 1:
                    # every substring ending at j qualifies
                    ans += j + 1
                else:
                    # query BEFORE folding s[j] into the prefix remainders
                    ans += cnt[m].get(rem[m], 0)
            # fold s[j] into prefix remainders and register index j
            for m in moduli:
                r = (rem[m] * 10 + d) % m
                rem[m] = r
                c = cnt[m]
                c[r] = c.get(r, 0) + 1
        return ans