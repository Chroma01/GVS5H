class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        parts = p.split('*')
        blocks = [part for part in parts if part]

        # Pattern is "**" (all literal blocks empty): empty substring matches.
        if not blocks:
            return 0

        # Find all occurrences of each distinct non-empty literal block.
        cache = {}
        occs = []
        for b in blocks:
            if b not in cache:
                cache[b] = self._kmp_occurrences(s, b)
            occs.append(cache[b])

        # Every non-empty literal block must appear at least once.
        for occ in occs:
            if not occ:
                return -1

        if len(blocks) == 1:
            return len(blocks[0])

        if len(blocks) == 2:
            return self._min_two(
                occs[0], len(blocks[0]),
                occs[1], len(blocks[1])
            )

        if len(blocks) == 3:
            return self._min_three(
                occs[0], len(blocks[0]),
                occs[1], len(blocks[1]),
                occs[2], len(blocks[2])
            )

        # Constraints guarantee at most three non-empty blocks.
        return -1

    def _kmp_occurrences(self, s: str, pat: str):
        n = len(s)
        m = len(pat)

        if m == 0 or m > n:
            return []

        # Prefix function for KMP.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and pat[i] != pat[j]:
                j = pi[j - 1]
            if pat[i] == pat[j]:
                j += 1
            pi[i] = j

        # Scan s and collect all start positions, including overlapping ones.
        occ = []
        j = 0
        for i, ch in enumerate(s):
            while j > 0 and ch != pat[j]:
                j = pi[j - 1]
            if ch == pat[j]:
                j += 1
                if j == m:
                    occ.append(i - m + 1)
                    j = pi[j - 1]

        return occ

    def _min_two(self, occ1, len1, occ2, len2):
        INF = 10 ** 18
        ans = INF

        i = 0
        best_start1 = -1
        n1 = len(occ1)

        # For each occurrence of the second block, keep the latest first-block
        # occurrence that ends at or before this second-block start.
        for st2 in occ2:
            while i < n1 and occ1[i] + len1 <= st2:
                best_start1 = occ1[i]
                i += 1

            if best_start1 != -1:
                cand = st2 + len2 - best_start1
                if cand < ans:
                    ans = cand

        return -1 if ans == INF else ans

    def _min_three(self, occ1, len1, occ2, len2, occ3, len3):
        INF = 10 ** 18
        ans = INF

        i1 = 0
        best_start1 = -1
        n1 = len(occ1)

        i3 = 0
        n3 = len(occ3)

        # Middle occurrences are processed in increasing start order.
        # best_start1 is the latest first-block occurrence ending before middle.
        # i3 is the first third-block occurrence starting after middle ends.
        for st2 in occ2:
            end2 = st2 + len2

            while i1 < n1 and occ1[i1] + len1 <= st2:
                best_start1 = occ1[i1]
                i1 += 1

            while i3 < n3 and occ3[i3] < end2:
                i3 += 1

            if best_start1 != -1 and i3 < n3:
                cand = occ3[i3] + len3 - best_start1
                if cand < ans:
                    ans = cand

        return -1 if ans == INF else ans


def run_tests():
    sol = Solution()
    cases = [
        ("abaacbaecebce", "ba*c*ce", 8),
        ("baccbaadbc", "cc*baa*adb", -1),
        ("a", "**", 0),
        ("madlogic", "*adlogi*", 6),
        ("abc", "**", 0),
        ("abc", "*b*", 1),
        ("abc", "*d*", -1),
        ("abc", "a*c*", 3),
        ("abc", "a*b*", 2),
        ("abc", "ab**bc", -1),
        ("abbc", "ab**bc", 4),
        ("abc", "a*b*c", 3),
        ("axbxc", "a*b*c", 5),
        ("aa", "a**a", 2),
        ("ab", "a**a", -1),
        ("aaa", "a*a*a", 3),
        ("aa", "a*a*a", -1),
        ("abc", "a**", 1),
        ("abc", "**c", 1),
        ("abab", "a**b", 2),
        ("abab", "a**a", 3),
        ("abc", "ab**", 2),
        ("abc", "**bc", 2),
        ("abc", "c**a", -1),
        ("abc", "*a*b", 2),
    ]

    for s, p, expected in cases:
        got = sol.shortestMatchingSubstring(s, p)
        if got == expected:
            print("PASS")
        else:
            print(f"FAIL s={s!r} p={p!r}")


if __name__ == "__main__":
    run_tests()