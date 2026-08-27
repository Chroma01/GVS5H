class Solution:
    def countSubstrings(self, s: str) -> int:
        # cnt[d][r] = number of substrings ending at the previous position
        # whose value modulo d equals r (for d in 1..9).
        cnt = [[0] * d for d in range(10)]
        ans = 0
        for ch in s:
            v = ord(ch) - 48  # current digit
            nxt = [[0] * d for d in range(10)]
            # Extend every active substring by this digit:
            # new remainder = (old * 10 + v) % d
            for d in range(1, 10):
                row = cnt[d]
                nrow = nxt[d]
                for r in range(d):
                    c = row[r]
                    if c:
                        nrow[(r * 10 + v) % d] += c
                # The new single-digit substring starting here
                nrow[v % d] += 1
            # Substrings ending here qualify iff last digit v != 0 and value % v == 0
            if v != 0:
                ans += nxt[v][0]
            cnt = nxt
        return ans