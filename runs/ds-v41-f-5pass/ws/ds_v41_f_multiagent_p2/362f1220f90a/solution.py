class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1

        ans = [''] * L
        fixed = [False] * L

        # 1) Apply every 'T' constraint; detect conflicts.
        for i, c in enumerate(str1):
            if c == 'T':
                for j in range(m):
                    pos = i + j
                    if fixed[pos]:
                        if ans[pos] != str2[j]:
                            return ""
                    else:
                        ans[pos] = str2[j]
                        fixed[pos] = True

        # 2) Baseline: every remaining (free) position becomes 'a'.
        for i in range(L):
            if not fixed[i]:
                ans[i] = 'a'

        target = list(str2)

        # 3) Break violating 'F' windows, left to right, rightmost free position.
        for i in range(n):
            if str1[i] == 'F' and ans[i:i + m] == target:
                for j in range(i + m - 1, i - 1, -1):
                    if not fixed[j]:
                        ans[j] = 'b'
                        fixed[j] = True
                        break
                else:
                    return ""

        return ''.join(ans)


if __name__ == "__main__":
    from itertools import product

    def brute(str1, str2):
        n, m = len(str1), len(str2)
        L = n + m - 1
        alpha = sorted(set(str2) | {'a', 'b'})
        best = None
        for tup in product(alpha, repeat=L):
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

    sol = Solution()
    cases = [
        ("TFTF", "ab", "ababa"),
        ("TFTF", "abc", ""),
        ("F", "d", "a"),
        ("F", "a", "b"),
        ("TF", "ab", "aba"),
        ("TT", "ab", ""),
        ("FF", "aa", "aba"),
    ]
    print("=== Provided / tricky cases ===")
    for s1, s2, exp in cases:
        got = sol.generateString(s1, s2)
        print(f"str1={s1!r} str2={s2!r} -> {got!r} exp={exp!r} {'OK' if got == exp else 'FAIL'}")

    print("=== Brute-force cross-check (n<=4, m<=3) ===")
    mismatches = 0
    tested = 0
    for n in range(1, 5):
        for m in range(1, 4):
            for bits in product("TF", repeat=n):
                s1 = ''.join(bits)
                for s2 in product("abc", repeat=m):
                    s2 = ''.join(s2)
                    got = sol.generateString(s1, s2)
                    exp = brute(s1, s2)
                    tested += 1
                    if got != exp:
                        mismatches += 1
                        print(f"MISMATCH str1={s1!r} str2={s2!r} got={got!r} exp={exp!r}")
    print(f"tested={tested} mismatches={mismatches}")