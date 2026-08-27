class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0

        # Counters for prefix states
        cnt3 = [0] * 3   # prefix digit-sum mod 3 (for last digits 3 and 6)
        cnt9 = [0] * 9   # prefix digit-sum mod 9 (for last digit 9)
        cnt7 = [0] * 7   # scaled prefix hash mod 7 (for last digit 7)

        sum3 = 0
        sum9 = 0
        P7 = 0          # prefix value mod 7: P[i] = (P[i-1]*10 + digit) % 7
        invPow = 1      # inv(10^(i+1)) mod 7; inv(10) mod 7 = 5 (10 ≡ 3, 3*5 = 15 ≡ 1)

        cnt3[0] = 1     # empty prefix
        cnt9[0] = 1
        cnt7[0] = 1     # Q[-1] = P[-1] * inv(10^0) = 0

        for i, ch in enumerate(s):
            d = ord(ch) - 48

            sum3 = (sum3 + d) % 3
            sum9 = (sum9 + d) % 9
            P7 = (P7 * 10 + d) % 7
            invPow = (invPow * 5) % 7
            q7 = (P7 * invPow) % 7

            if d == 0:
                pass  # last digit must be non-zero
            elif d == 1 or d == 2 or d == 5:
                ans += i + 1  # every substring ending here qualifies
            elif d == 4:
                # length-1 substring "4" always works; length>=2 depends on last two digits
                ans += 1
                if i >= 1:
                    prev = ord(s[i - 1]) - 48
                    if (prev * 10 + d) % 4 == 0:
                        ans += i  # all substrings of length >= 2 ending at i
            elif d == 8:
                # length 1: "8" works; length 2: last two digits mod 8; length>=3: last three digits mod 8
                ans += 1
                if i >= 1:
                    prev = ord(s[i - 1]) - 48
                    if (prev * 10 + d) % 8 == 0:
                        ans += 1
                if i >= 2:
                    prev2 = ord(s[i - 2]) - 48
                    prev1 = ord(s[i - 1]) - 48
                    if (prev2 * 100 + prev1 * 10 + d) % 8 == 0:
                        ans += i - 1  # all substrings of length >= 3 ending at i
            elif d == 3 or d == 6:
                # divisible by 3 (6 is even, so only mod 3 matters) via digit sum
                ans += cnt3[sum3]
            elif d == 9:
                ans += cnt9[sum9]
            else:  # d == 7
                ans += cnt7[q7]

            cnt3[sum3] += 1
            cnt9[sum9] += 1
            cnt7[q7] += 1

        return ans