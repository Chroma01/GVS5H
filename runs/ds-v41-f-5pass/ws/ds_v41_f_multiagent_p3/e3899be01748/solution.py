class Solution:
    def countSubstrings(self, s: str) -> int:
        # Precompute transitions: trans[x][m][r] = (r * 10 + x) % m
        trans = [[None] * 10 for _ in range(10)]
        for x in range(10):
            for m in range(1, 10):
                trans[x][m] = [(r * 10 + x) % m for r in range(m)]

        # cnt[m][r] = number of substrings ending at the previous index
        #             whose numeric value is congruent to r modulo m.
        cnt = [None] * 10
        for m in range(1, 10):
            cnt[m] = [0] * m

        ans = 0
        for ch in s:
            x = ord(ch) - 48
            new_cnt = [None] * 10

            # m = 1: every substring is congruent to 0 (mod 1)
            new_cnt[1] = [cnt[1][0] + 1]

            # m = 2 .. 9: extend each old substring, plus the fresh 1-char substring
            for m in range(2, 10):
                old = cnt[m]
                new = [0] * m
                tr = trans[x][m]
                for t, o in zip(tr, old):
                    new[t] += o
                new[x % m] += 1
                new_cnt[m] = new

            # Substrings ending here are divisible by the last digit iff digit != 0
            # and the value is congruent to 0 modulo that digit.
            if x:
                ans += new_cnt[x][0]

            cnt = new_cnt

        return ans


if __name__ == "__main__":
    import random
    import time

    sol = Solution()

    samples = [
        ("12936", 11),
        ("5701283", 18),
        ("1010101010", 25),
        ("0", 0),
        ("1", 1),
        ("01", 2),
        ("00", 0),
        ("10", 1),
        ("202", 4),
    ]

    ok_all = True
    for s, exp in samples:
        got = sol.countSubstrings(s)
        ok = got == exp
        ok_all = ok_all and ok
        print(f"s={s!r:>14}  got={got:<7} expected={exp:<7} {'PASS' if ok else 'FAIL'}")
    print("sample tests:", "PASS" if ok_all else "FAIL")

    def brute(s):
        n = len(s)
        c = 0
        for i in range(n):
            d = ord(s[i]) - 48
            if d == 0:
                continue
            v = 0
            p = 1
            for j in range(i, -1, -1):
                v += (ord(s[j]) - 48) * p
                p *= 10
                if v % d == 0:
                    c += 1
        return c

    random.seed(12345)
    mismatches = 0
    for _ in range(3000):
        L = random.randint(1, 12)
        s = "".join(random.choice("0123456789") for _ in range(L))
        a = sol.countSubstrings(s)
        b = brute(s)
        if a != b:
            mismatches += 1
            print("MISMATCH", s, a, b)
    print("random cross-check:", "PASS" if mismatches == 0 else f"FAIL ({mismatches})")

    s = "".join(random.choice("0123456789") for _ in range(100000))
    t0 = time.time()
    res = sol.countSubstrings(s)
    t1 = time.time()
    print(f"timing n=100000: {t1 - t0:.3f}s (result={res})")