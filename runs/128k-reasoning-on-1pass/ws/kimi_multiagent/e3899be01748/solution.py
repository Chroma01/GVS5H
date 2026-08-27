class Solution:
    def countSubstrings(self, s: str) -> int:
        ans = 0

        # Prefix states for the moduli that need remainder matching.
        p3 = 0          # digit-sum prefix mod 3  (10 ≡ 1 mod 3)
        p9 = 0          # digit-sum prefix mod 9  (10 ≡ 1 mod 9)
        p7 = 0          # numeric prefix mod 7
        inv7 = 1        # inv(10)^t mod 7 = 5^t mod 7
        freq3 = [0] * 3
        freq9 = [0] * 9
        freq7 = [0] * 7
        # Seed with the empty prefix (index 0) so substrings starting at 0 count.
        freq3[0] = 1
        freq9[0] = 1
        freq7[0] = 1

        for j, ch in enumerate(s):
            d = ord(ch) - 48

            # Advance all prefixes to length j + 1.
            p3 = (p3 + d) % 3
            p9 = (p9 + d) % 9
            p7 = (p7 * 10 + d) % 7
            inv7 = (inv7 * 5) % 7

            if d == 0:
                pass  # substrings may not end in zero
            elif d == 1 or d == 2 or d == 5:
                ans += j + 1                      # every start works
            elif d == 3 or d == 6:
                ans += freq3[p3]                  # 6: evenness is automatic
            elif d == 9:
                ans += freq9[p9]
            elif d == 7:
                ans += freq7[(p7 * inv7) % 7]     # normalized remainder match
            elif d == 4:
                ans += 1                          # "4" itself
                if j > 0 and (ord(s[j - 1]) - 48) % 2 == 0:
                    ans += j                      # all lengths >= 2 work
            elif d == 8:
                ans += 1                          # "8" itself
                if j >= 1:
                    b = ord(s[j - 1]) - 48
                    if (10 * b + 8) % 8 == 0:
                        ans += 1                  # length exactly 2
                if j >= 2:
                    a = ord(s[j - 2]) - 48
                    b = ord(s[j - 1]) - 48
                    if (100 * a + 10 * b + 8) % 8 == 0:
                        ans += j - 1              # all lengths >= 3 work

            # Insert current prefix states AFTER querying (exclude empty substring).
            freq3[p3] += 1
            freq9[p9] += 1
            freq7[(p7 * inv7) % 7] += 1

        return ans