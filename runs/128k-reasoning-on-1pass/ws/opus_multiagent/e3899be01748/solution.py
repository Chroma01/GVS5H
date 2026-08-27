class Solution:
    def countSubstrings(self, s: str) -> int:
        digits = list(map(int, s))
        n = len(digits)

        # prefix digit-sum residue counters (include empty prefix P[-1] = 0)
        cnt3 = [1, 0, 0]
        cnt9 = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        # rolling table: cnt7[r] = # of start positions j <= i with val(s[j..i]) % 7 == r
        cnt7 = [0] * 7

        # transition r -> (3r + d) % 7 is a permutation (3 invertible mod 7, inverse 5)
        # new[t] = old[((t - d) * 5) % 7]
        perms = [[((t - dg) * 5) % 7 for t in range(7)] for dg in range(10)]

        p3 = 0
        p9 = 0
        total = 0

        for i in range(n):
            d = digits[i]
            p3 = (p3 + d) % 3
            p9 = (p9 + d) % 9

            pm = perms[d]
            cnt7 = [cnt7[pm[0]], cnt7[pm[1]], cnt7[pm[2]], cnt7[pm[3]],
                    cnt7[pm[4]], cnt7[pm[5]], cnt7[pm[6]]]
            cnt7[d % 7] += 1

            if d == 0:
                pass
            elif d == 1 or d == 2 or d == 5:
                total += i + 1
            elif d == 3 or d == 6:
                # 6: last digit even -> only mod 3 condition matters
                total += cnt3[p3]
            elif d == 4:
                # 100 % 4 == 0 -> only last two digits matter; 10a+4 = 2a (mod 4)
                total += 1 + (i if (i > 0 and digits[i - 1] % 2 == 0) else 0)
            elif d == 7:
                total += cnt7[0]
            elif d == 8:
                # 1000 % 8 == 0 -> only last three digits matter
                t = 1
                if i > 0 and (digits[i - 1] == 0 or digits[i - 1] == 4 or digits[i - 1] == 8):
                    t += 1
                if i > 1 and (2 * digits[i - 2] + digits[i - 1]) % 4 == 0:
                    t += i - 1
                total += t
            else:  # d == 9
                total += cnt9[p9]

            cnt3[p3] += 1
            cnt9[p9] += 1

        return total