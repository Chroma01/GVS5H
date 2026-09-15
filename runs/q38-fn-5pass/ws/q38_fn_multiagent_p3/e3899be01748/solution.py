class Solution:
    def countSubstrings(self, s: str) -> int:
        cnt = [[0] * d for d in range(10)]
        ans = 0

        for ch in s:
            x = ord(ch) - 48

            for d in range(1, 10):
                old = cnt[d]
                new = [0] * d

                for r, c in enumerate(old):
                    if c:
                        new[(r * 10 + x) % d] += c

                new[x % d] += 1
                cnt[d] = new

            if x != 0:
                ans += cnt[x][0]

        return ans