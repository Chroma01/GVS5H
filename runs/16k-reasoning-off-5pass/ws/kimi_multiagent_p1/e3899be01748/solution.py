class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0

        # Counters of keys K[k] = P[k] * inv(10^k) mod m, for k = 0..j
        # For m = 3 and m = 9, 10 ≡ 1 (mod m), so K[k] = P[k] (plain prefix sum mod m).
        # For m = 7, 10 ≡ 3, inv(10) ≡ 5 (mod 7); maintain running inverse power.
        cnt3 = [0] * 3
        cnt7 = [0] * 7
        cnt9 = [0] * 9
        cnt3[0] = 1
        cnt7[0] = 1
        cnt9[0] = 1

        p3 = p7 = p9 = 0
        inv7 = 1  # inv(10^j) mod 7 at step j

        for j, ch in enumerate(s):
            d = ord(ch) - 48
            p3 = (p3 * 10 + d) % 3
            p7 = (p7 * 10 + d) % 7
            p9 = (p9 * 10 + d) % 9
            inv7 = (inv7 * 5) % 7  # now inv(10^(j+1)) mod 7

            if d == 0:
                pass  # last digit must be a non-zero divisor
            elif d in (1, 2, 5):
                ans += j + 1
            elif d == 3:
                ans += cnt3[p3]
            elif d == 9:
                ans += cnt9[p9]
            elif d == 6:
                # even last digit already satisfied; need divisibility by 3
                ans += cnt3[p3]
            elif d == 7:
                ans += cnt7[p7 * inv7 % 7]
            elif d == 4:
                # mod 4 depends only on last two digits
                if j == 0:
                    ans += 1
                else:
                    two = (ord(s[j - 1]) - 48) * 10 + 4
                    ans += (j + 1) if two % 4 == 0 else 1
            else:  # d == 8
                # mod 8 depends only on last three digits
                if j >= 2:
                    three = ((ord(s[j - 2]) - 48) * 100
                             + (ord(s[j - 1]) - 48) * 10 + 8)
                    if three % 8 == 0:
                        ans += j + 1
                    else:
                        two = (ord(s[j - 1]) - 48) * 10 + 8
                        ans += 1 + (1 if two % 8 == 0 else 0)
                elif j == 1:
                    two = (ord(s[0]) - 48) * 10 + 8
                    ans += 1 + (1 if two % 8 == 0 else 0)
                else:
                    ans += 1

            cnt3[p3] += 1
            cnt7[p7 * inv7 % 7] += 1
            cnt9[p9] += 1

        return ans