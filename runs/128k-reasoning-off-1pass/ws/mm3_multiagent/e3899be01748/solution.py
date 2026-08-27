class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        
        # d=1,2,5: all substrings ending with the digit are valid
        for d in [1, 2, 5]:
            for j in range(n):
                if s[j] == str(d):
                    ans += j + 1
        
        # d=3 and d=6: use prefix sums mod 3
        pref3 = 0
        freq3 = [0, 0, 0]
        freq3[0] = 1  # prefix of length 0
        for j in range(n):
            pref3 = (pref3 + int(s[j])) % 3
            if s[j] == '3' or s[j] == '6':
                ans += freq3[pref3]
            freq3[pref3] += 1
        
        # d=9: use prefix sums mod 9
        pref9 = 0
        freq9 = [0] * 9
        freq9[0] = 1
        for j in range(n):
            pref9 = (pref9 + int(s[j])) % 9
            if s[j] == '9':
                ans += freq9[pref9]
            freq9[pref9] += 1
        
        # d=4: check last two digits
        for j in range(n):
            if s[j] == '4':
                ans += 1  # length 1
                if j >= 1:
                    two = int(s[j-1]) * 10 + 4
                    if two % 4 == 0:
                        ans += 1
                if j >= 2:
                    two = int(s[j-1]) * 10 + 4
                    if two % 4 == 0:
                        ans += (j - 1)  # all substrings of length >= 3
        
        # d=8: check last three digits
        for j in range(n):
            if s[j] == '8':
                ans += 1  # length 1
                if j >= 1:
                    two = int(s[j-1]) * 10 + 8
                    if two % 8 == 0:
                        ans += 1
                if j >= 2:
                    three = int(s[j-2]) * 100 + int(s[j-1]) * 10 + 8
                    if three % 8 == 0:
                        ans += (j - 1)  # length >= 3
        
        # d=7: use 2D frequency array with period 6
        pow10_mod7 = [1, 3, 2, 6, 4, 5]
        inv_pow10_mod7 = [1, 5, 4, 6, 2, 3]  # modular inverses
        cnt = [[0] * 7 for _ in range(6)]
        pref7 = 0
        cnt[0 % 6][pref7] = 1  # prefix of length 0
        for j in range(n):
            if j > 0:
                cnt[j % 6][pref7] += 1
            pref7_next = (pref7 * 10 + int(s[j])) % 7
            if s[j] == '7':
                for i0 in range(6):
                    k = (j + 1 - i0) % 6
                    r = (pref7_next * inv_pow10_mod7[k]) % 7
                    ans += cnt[i0][r]
            pref7 = pref7_next
        
        return ans