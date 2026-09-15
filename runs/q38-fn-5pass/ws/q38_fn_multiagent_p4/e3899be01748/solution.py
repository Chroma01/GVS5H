class Solution:
    def countSubstrings(self, s: str) -> int:
        # Offsets for residue tables of divisors 1..9 in one flat list.
        offset = [0] * 10
        total = 0
        for d in range(1, 10):
            offset[d] = total
            total += d

        # trans[x][idx] = new flat index after appending digit x to a substring
        # whose residue state is idx.
        trans = [[0] * total for _ in range(10)]
        for x in range(10):
            for d in range(1, 10):
                base = offset[d]
                for r in range(d):
                    trans[x][base + r] = base + ((r * 10 + x) % d)

        # Index of the one-character substring digit x in each divisor table.
        single = [
            tuple(offset[d] + (x % d) for d in range(1, 10))
            for x in range(10)
        ]

        freq = [0] * total
        ans = 0
        indices = range(total)

        for ch in s:
            x = ord(ch) - 48
            new_freq = [0] * total
            tr = trans[x]
            old = freq

            # Extend every substring ending at the previous position.
            for i in indices:
                new_freq[tr[i]] += old[i]

            # Add the one-character substring consisting of x.
            for idx in single[x]:
                new_freq[idx] += 1

            freq = new_freq

            # If the current last digit is non-zero, count substrings ending here
            # whose value is divisible by that digit.
            if x != 0:
                ans += freq[offset[x]]

        return ans