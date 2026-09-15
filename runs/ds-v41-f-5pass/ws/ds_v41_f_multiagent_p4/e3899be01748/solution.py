class Solution:
    def countSubstrings(self, s: str) -> int:
        # Flat storage for residue counts of divisors 1..9.
        # off[d] is the start index of the block for divisor d.
        off = [0] * 10
        total = 0
        for d in range(1, 10):
            off[d] = total
            total += d

        cnt = [0] * total
        ans = 0

        for ch in s:
            c = ord(ch) - 48
            new = [0] * total

            for d in range(1, 10):
                base = off[d]
                # Extend every substring ending at the previous position.
                for r in range(d):
                    new[base + (r * 10 + c) % d] += cnt[base + r]
                # Add the substring consisting only of the current digit.
                new[base + c % d] += 1

            # If the last digit is non-zero, all valid substrings ending here
            # have last digit c and must be 0 modulo c.
            if c:
                ans += new[off[c]]

            cnt = new

        return ans