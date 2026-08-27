class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        for d in range(1, 10):
            d_str = str(d)
            for j in range(n):
                if s[j] == d_str:
                    val = 0
                    power = 1
                    # Look back up to 9 characters
                    # The period of 10^k mod d is at most 9 for d in 1..9
                    # So looking back 9 characters is sufficient to capture one full period
                    for i in range(j, max(j - 9, -1), -1):
                        digit = int(s[i])
                        val = (digit * power + val) % d
                        power = (power * 10) % d
                        if val == 0:
                            ans += 1
        return ans