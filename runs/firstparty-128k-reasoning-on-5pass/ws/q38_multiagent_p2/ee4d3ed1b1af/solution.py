from bisect import bisect_left, bisect_right
import random


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        parts = p.split("*")
        blocks = [part for part in parts if part]

        if not blocks:
            return 0

        def kmp_occurrences(text: str, pat: str):
            n = len(text)
            m = len(pat)
            if m == 0 or m > n:
                return []

            lps = [0] * m
            length = 0
            for i in range(1, m):
                while length > 0 and pat[i] != pat[length]:
                    length = lps[length - 1]
                if pat[i] == pat[length]:
                    length += 1
                    lps[i] = length

            res = []
            j = 0
            for i in range(n):
                ch = text[i]
                while j > 0 and ch != pat[j]:
                    j = lps[j - 1]
                if ch == pat[j]:
                    j += 1
                if j == m:
                    res.append(i - m + 1)
                    j = lps[j - 1]
            return res

        cache = {}
        for block in blocks:
            if block not in cache:
                cache[block] = kmp_occurrences(s, block)

        occ = [cache[block] for block in blocks]

        if len(blocks) == 1:
            return len(blocks[0]) if occ[0] else -1

        ans = len(s) + 1

        if len(blocks) == 2:
            first, second = blocks
            len_first, len_second = len(first), len(second)
            first_occ, second_occ = occ[0], occ[1]

            for start_second in second_occ:
                idx = bisect_right(first_occ, start_second - len_first) - 1
                if idx >= 0:
                    candidate = start_second - first_occ[idx] + len_second
                    if candidate < ans:
                        ans = candidate

            return -1 if ans == len(s) + 1 else ans

        if len(blocks) == 3:
            a, b, c = blocks
            len_a, len_b, len_c = len(a), len(b), len(c)
            a_occ, b_occ, c_occ = occ[0], occ[1], occ[2]

            for start_b in b_occ:
                idx_a = bisect_right(a_occ, start_b - len_a) - 1
                if idx_a < 0:
                    continue

                idx_c = bisect_left(c_occ, start_b + len_b)
                if idx_c == len(c_occ):
                    continue

                candidate = c_occ[idx_c] + len_c - a_occ[idx_a]
                if candidate < ans:
                    ans = candidate

            return -1 if ans == len(s) + 1 else ans

        return -1


def brute_force(s: str, p: str) -> int:
    n = len(s)
    m = len(p)

    def matches(t: str) -> bool:
        l = len(t)
        dp = [[False] * (l + 1) for _ in range(m + 1)]
        dp[m][l] = True

        for i in range(m - 1, -1, -1):
            if p[i] == '*':
                for j in range(l, -1, -1):
                    dp[i][j] = dp[i + 1][j] or (j < l and dp[i][j + 1])
            else:
                for j in range(l - 1, -1, -1):
                    dp[i][j] = (t[j] == p[i] and dp[i + 1][j + 1])

        return dp[0][0]

    for length in range(n + 1):
        for i in range(n - length + 1):
            if matches(s[i:i + length]):
                return length
    return -1


def run_tests() -> None:
    sol = Solution()
    cases = [
        ("abaacbaecebce", "ba*c*ce", 8),
        ("baccbaadbc", "cc*baa*adb", -1),
        ("a", "**", 0),
        ("madlogic", "*adlogi*", 6),
        ("abc", "**", 0),
        ("abc", "*b*", 1),
        ("abc", "b**", 1),
        ("abc", "**b", 1),
        ("abc", "*z*", -1),
        ("a", "a*a", -1),
        ("aa", "a*a", 2),
        ("a", "a**a", -1),
        ("aa", "a**a", 2),
        ("abc", "a**c", 3),
        ("ac", "a**c", 2),
        ("abbc", "ab**bc", 4),
        ("abc", "a**bc", 3),
        ("abc", "a*b*c", 3),
        ("abbc", "a*b*c", 4),
        ("abc", "d*e*f", -1),
        ("aaaa", "aa**aa", 4),
        ("aaaaa", "aa**aa", 4),
        ("abab", "ab**ab", 4),
        ("ababa", "ab**ab", 4),
        ("abcabc", "abc**abc", 6),
    ]

    failures = []
    for s, p, expected in cases:
        got = sol.shortestMatchingSubstring(s, p)
        bf = brute_force(s, p)
        if got != expected or bf != expected:
            failures.append((s, p, expected, got, bf))

    rng = random.Random(12345)
    alphabet = "ab"
    for _ in range(2000):
        n = rng.randint(0, 8)
        s = ''.join(rng.choice(alphabet) for _ in range(n))
        la = rng.randint(0, 3)
        lb = rng.randint(0, 3)
        lc = rng.randint(0, 3)
        a = ''.join(rng.choice(alphabet) for _ in range(la))
        b = ''.join(rng.choice(alphabet) for _ in range(lb))
        c = ''.join(rng.choice(alphabet) for _ in range(lc))
        p = a + '*' + b + '*' + c

        expected = brute_force(s, p)
        got = sol.shortestMatchingSubstring(s, p)
        if got != expected:
            failures.append((s, p, expected, got, None))
            if len(failures) > 5:
                break

    if failures:
        print("SAMPLE TESTS: FAIL")
        for item in failures[:10]:
            print(item)
    else:
        print("SAMPLE TESTS: PASS")


if __name__ == "__main__":
    run_tests()