class Solution:
    def countSubstrings(self, s: str) -> int:
        cnt1 = [1]
        cnt2 = [1, 0]
        cnt3 = [1, 0, 0]
        cnt4 = [1, 0, 0, 0]
        cnt7 = [1, 0, 0, 0, 0, 0, 0]
        cnt9 = [1, 0, 0, 0, 0, 0, 0, 0, 0]

        ans = 0
        for ch in s:
            d = ord(ch) - 48

            if d:
                if d == 1 or d == 2 or d == 5:
                    ans += cnt1[0]
                elif d == 3 or d == 6:
                    ans += cnt3[0]
                elif d == 4:
                    ans += cnt2[0]
                elif d == 7:
                    ans += cnt7[0]
                elif d == 8:
                    ans += cnt4[0]
                else:  # d == 9
                    ans += cnt9[0]

            cnt1[0] += 1

            t = d & 1
            new2 = [0, 0]
            new2[t] = cnt2[0] + cnt2[1]
            new2[0] += 1
            cnt2 = new2

            new3 = [0, 0, 0]
            for r in range(3):
                new3[(r + d) % 3] += cnt3[r]
            new3[0] += 1
            cnt3 = new3

            new4 = [0, 0, 0, 0]
            for r in range(4):
                new4[(2 * r + d) & 3] += cnt4[r]
            new4[0] += 1
            cnt4 = new4

            new7 = [0] * 7
            for r in range(7):
                new7[(3 * r + d) % 7] += cnt7[r]
            new7[0] += 1
            cnt7 = new7

            new9 = [0] * 9
            for r in range(9):
                new9[(r + d) % 9] += cnt9[r]
            new9[0] += 1
            cnt9 = new9

        return ans