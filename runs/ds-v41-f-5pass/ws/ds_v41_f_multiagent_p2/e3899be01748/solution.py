class Solution:
    def countSubstrings(self, s: str) -> int:
        digits = [ord(ch) - 48 for ch in s]
        present = [False] * 10
        for c in digits:
            present[c] = True

        ans = 0
        for d in range(1, 10):
            if not present[d]:
                continue
            # trans[c][r] = residue after appending digit c to a value with residue r (mod d)
            trans = [[(r * 10 + c) % d for r in range(d)] for c in range(10)]
            cnt = [0] * d  # substrings ending at previous index, by residue mod d
            for c in digits:
                tr = trans[c]
                nc = [0] * d
                for r, v in enumerate(cnt):
                    if v:
                        nc[tr[r]] += v
                nc[c % d] += 1  # length-1 substring ending here
                if c == d:
                    ans += nc[0]
                cnt = nc
        return ans