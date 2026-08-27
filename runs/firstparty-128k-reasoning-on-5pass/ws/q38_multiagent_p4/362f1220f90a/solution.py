class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)

        # Prefix function for str2.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and str2[i] != str2[j]:
                j = pi[j - 1]
            if str2[i] == str2[j]:
                j += 1
            pi[i] = j

        last_idx = ord(str2[-1]) - 97

        # KMP transition table over states 0..m-1.
        # A full match from state m-1 with last char falls back to pi[m-1].
        trans = [[0] * 26 for _ in range(m)]
        for s in range(m):
            pat_s = ord(str2[s]) - 97
            row = trans[s]
            fb_row = trans[pi[s - 1]] if s > 0 else None
            for c in range(26):
                if c == pat_s:
                    nxt = s + 1
                    if nxt == m:
                        nxt = pi[m - 1]
                    row[c] = nxt
                else:
                    row[c] = 0 if s == 0 else fb_row[c]

        bits = [1 << i for i in range(m)]
        all_mask = (1 << m) - 1

        # reach_all[s] / reach_F[s]: next-state masks reachable from state s.
        # pre_all[t] / pre_F[t]: states that can reach next state t.
        reach_all = [0] * m
        reach_F = [0] * m
        pre_all = [0] * m
        pre_F = [0] * m

        for s in range(m):
            row = trans[s]
            bit_s = bits[s]
            mask_all = 0
            mask_F = 0
            last_state = (s == m - 1)
            for c in range(26):
                nxt = row[c]
                bit = bits[nxt]
                mask_all |= bit
                pre_all[nxt] |= bit_s
                if not (last_state and c == last_idx):
                    mask_F |= bit
                    pre_F[nxt] |= bit_s
            reach_all[s] = mask_all
            reach_F[s] = mask_F

        pairs_all = list(zip(bits, reach_all))
        pairs_F = list(zip(bits, reach_F))

        L = n + m - 1

        # types[p] = 0: no window ends here, 1: T, 2: F.
        types = [0] * L
        for i, ch in enumerate(str1):
            types[i + m - 1] = 1 if ch == 'T' else 2

        # dp[p] is a bitset of KMP states before position p that can be completed.
        dp = [0] * (L + 1)
        dp[L] = all_mask

        t_state_bit = bits[m - 1]
        t_next_bit = bits[pi[m - 1]]

        for p in range(L - 1, -1, -1):
            B = dp[p + 1]
            if B == 0:
                dp[p] = 0
                continue

            typ = types[p]
            if typ == 0:
                if B == all_mask:
                    dp[p] = all_mask
                elif B & (B - 1) == 0:
                    dp[p] = pre_all[B.bit_length() - 1]
                else:
                    mask = 0
                    for bit, r in pairs_all:
                        if r & B:
                            mask |= bit
                    dp[p] = mask
            elif typ == 1:
                dp[p] = t_state_bit if (B & t_next_bit) else 0
            else:
                if B == all_mask:
                    dp[p] = all_mask
                elif B & (B - 1) == 0:
                    dp[p] = pre_F[B.bit_length() - 1]
                else:
                    mask = 0
                    for bit, r in pairs_F:
                        if r & B:
                            mask |= bit
                    dp[p] = mask

        if (dp[0] & 1) == 0:
            return ""

        ans = []
        state = 0
        chars = [chr(97 + i) for i in range(26)]
        last_char = str2[-1]

        for p in range(L):
            B = dp[p + 1]
            typ = types[p]
            row = trans[state]

            if typ == 1:
                if state != m - 1:
                    return ""
                c = last_idx
                nxt = row[c]
                if not (B & bits[nxt]):
                    return ""
                ans.append(last_char)
                state = nxt
            elif typ == 2:
                chosen = False
                for c in range(26):
                    if state == m - 1 and c == last_idx:
                        continue
                    nxt = row[c]
                    if B & bits[nxt]:
                        ans.append(chars[c])
                        state = nxt
                        chosen = True
                        break
                if not chosen:
                    return ""
            else:
                chosen = False
                for c in range(26):
                    nxt = row[c]
                    if B & bits[nxt]:
                        ans.append(chars[c])
                        state = nxt
                        chosen = True
                        break
                if not chosen:
                    return ""

        return ''.join(ans)


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ("TFTF", "ab", "ababa"),
        ("TFTF", "abc", ""),
        ("F", "d", "a"),
        ("T", "a", "a"),
        ("F", "a", "b"),
        ("TT", "aa", "aaa"),
        ("TT", "ab", ""),
        ("F", "aaa", "aab"),
        ("T", "abc", "abc"),
        ("FFF", "b", "aaa"),
        ("TTT", "ab", ""),
        ("TTT", "aa", "aaaa"),
        ("F", "bc", "aa"),
        ("F", "aa", "ab"),
        ("FTF", "aa", "baab"),
        ("TFT", "aba", "ababa"),
        ("TFT", "abc", ""),
    ]
    for s1, s2, exp in cases:
        assert sol.generateString(s1, s2) == exp