class Solution:
    def countSubstrings(self, s: str) -> int:
        # trans[x][d][r] = (r * 10 + x) % d
        # rem[x][d] = x % d
        trans = [[None] * 10 for _ in range(10)]
        rem = [[0] * 10 for _ in range(10)]

        for x in range(10):
            for d in range(1, 10):
                trans[x][d] = [(r * 10 + x) % d for r in range(d)]
                rem[x][d] = x % d

        # For each digit x, precompute the update descriptors for d = 1..9.
        updates = [
            [(d, trans[x][d], rem[x][d]) for d in range(1, 10)]
            for x in range(10)
        ]

        # counts[d][r] = number of suffixes ending at the current position
        # whose numeric value has remainder r modulo d.
        counts = [[0] * d for d in range(10)]

        ans = 0

        for ch in s:
            x = ord(ch) - 48

            for d, tr, r0 in updates[x]:
                old = counts[d]
                new = [0] * d

                for r, c in enumerate(old):
                    new[tr[r]] += c

                # Add the new one-character suffix.
                new[r0] += 1

                counts[d] = new

            # If the last digit is nonzero, valid substrings ending here are
            # exactly those with remainder 0 modulo x.
            if x != 0:
                ans += counts[x][0]

        return ans