import itertools


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        ans = ['?'] * L

        # 1) Apply all 'T' constraints (forced characters).
        for i in range(n):
            if str1[i] == 'T':
                for j in range(m):
                    ch = str2[j]
                    pos = i + j
                    if ans[pos] != '?' and ans[pos] != ch:
                        return ""
                    ans[pos] = ch

        # 2) Fill remaining cells with the smallest letter 'a' and mark free.
        free = [False] * L
        for i in range(L):
            if ans[i] == '?':
                ans[i] = 'a'
                free[i] = True

        # 3) Scan 'F' windows left to right; break any that equal str2.
        for i in range(n):
            if str1[i] == 'F':
                match = True
                for j in range(m):
                    if ans[i + j] != str2[j]:
                        match = False
                        break
                if match:
                    p = -1
                    for j in range(i + m - 1, i - 1, -1):
                        if free[j]:
                            p = j
                            break
                    if p == -1:
                        return ""
                    ans[p] = 'b' if str2[p - i] == 'a' else 'a'
                    free[p] = False

        return ''.join(ans)


def brute(str1, str2, alphabet):
    """Exhaustively smallest word over `alphabet`, or "" if none."""
    n, m = len(str1), len(str2)
    L = n + m - 1
    best = None
    for tup in itertools.product(alphabet, repeat=L):
        w = ''.join(tup)
        ok = True
        for i in range(n):
            sub = w[i:i + m]
            if str1[i] == 'T':
                if sub != str2:
                    ok = False
                    break
            else:
                if sub == str2:
                    ok = False
                    break
        if ok and (best is None or w < best):
            best = w
    return best if best is not None else ""


def run_tests():
    sol = Solution()

    # Statement examples.
    examples = [
        ("TFTF", "ab", "ababa"),
        ("TFTF", "abc", ""),
        ("F", "d", "a"),
    ]
    for s1, s2, exp in examples:
        got = sol.generateString(s1, s2)
        assert got == exp, ("example failed", s1, s2, got, exp)

    # Validate the brute-force alphabet assumption: the true minimal word never
    # needs a letter outside set(str2) | {'a','b'}.
    alphabet_issues = []
    for n in range(1, 4):
        for m in range(1, 3):
            for s1 in itertools.product('TF', repeat=n):
                str1 = ''.join(s1)
                for s2 in itertools.product('ab', repeat=m):
                    str2 = ''.join(s2)
                    if brute(str1, str2, 'ab') != brute(str1, str2, 'abc'):
                        alphabet_issues.append((str1, str2))
    for n in range(1, 3):
        for m in range(1, 3):
            for s1 in itertools.product('TF', repeat=n):
                str1 = ''.join(s1)
                for s2 in itertools.product('abc', repeat=m):
                    str2 = ''.join(s2)
                    if brute(str1, str2, 'abc') != brute(str1, str2, 'abcd'):
                        alphabet_issues.append((str1, str2))

    tested = 0
    first = None

    # Phase A: str2 over {a,b}, n = 1..6, m = 1..4.
    for n in range(1, 7):
        for m in range(1, 5):
            for s1 in itertools.product('TF', repeat=n):
                str1 = ''.join(s1)
                for s2 in itertools.product('ab', repeat=m):
                    str2 = ''.join(s2)
                    exp = brute(str1, str2, 'ab')
                    got = sol.generateString(str1, str2)
                    tested += 1
                    if got != exp and first is None:
                        first = (str1, str2, got, exp)

    # Phase B: str2 over {a,b,c}, n = 1..5, m = 1..3.
    for n in range(1, 6):
        for m in range(1, 4):
            for s1 in itertools.product('TF', repeat=n):
                str1 = ''.join(s1)
                for s2 in itertools.product('abc', repeat=m):
                    str2 = ''.join(s2)
                    exp = brute(str1, str2, 'abc')
                    got = sol.generateString(str1, str2)
                    tested += 1
                    if got != exp and first is None:
                        first = (str1, str2, got, exp)

    if alphabet_issues:
        print("BRUTE ALPHABET PROBLEM (brute reference may be unreliable):")
        for it in alphabet_issues[:5]:
            print("  ", it)

    if first is not None:
        s1, s2, got, exp = first
        print("FIRST COUNTEREXAMPLE FOUND")
        print("str1   =", repr(s1))
        print("str2   =", repr(s2))
        print("greedy =", repr(got))
        print("true   =", repr(exp))
    else:
        print("NO MISMATCHES across", tested, "cases")

    # ---- verbatim reporting of examples and edge cases ----
    print("statement examples:")
    for s1, s2, exp in examples:
        print(f"  {s1} / {s2} -> {sol.generateString(s1, s2)!r}")

    print("edge cases:")
    edge = [
        ("TFT", "a"),   # m = 1
        ("TT", "aa"),   # all-T str1, consistent
        ("TT", "ab"),   # all-T str1, conflict -> ""
        ("FF", "a"),    # all-F str1, m = 1
        ("FF", "ab"),   # all-F str1, m = 2
        ("TF", "a"),    # str2 = 'a'
        ("TF", "b"),    # str2 = 'b'
    ]
    for s1, s2 in edge:
        print(f"  {s1} / {s2} -> {sol.generateString(s1, s2)!r}")


if __name__ == "__main__":
    run_tests()