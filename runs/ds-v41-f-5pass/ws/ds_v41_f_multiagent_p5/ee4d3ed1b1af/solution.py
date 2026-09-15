import random, time, re


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # p has exactly two '*', so p = A + '*' + B + '*' + C
        A, B, C = p.split('*')
        n = len(s)

        # KMP: return all start indices (overlapping) of pat in s
        def kmp_occ(pat):
            if not pat:
                return []
            m = len(pat)
            fail = [0] * m
            j = 0
            for i in range(1, m):
                while j > 0 and pat[i] != pat[j]:
                    j = fail[j - 1]
                if pat[i] == pat[j]:
                    j += 1
                fail[i] = j
            occ = []
            j = 0
            for i in range(n):
                while j > 0 and s[i] != pat[j]:
                    j = fail[j - 1]
                if s[i] == pat[j]:
                    j += 1
                    if j == m:
                        occ.append(i - m + 1)
                        j = fail[j - 1]   # keep scanning for overlaps
            return occ

        occA = kmp_occ(A)
        occB = kmp_occ(B)
        occC = kmp_occ(C)

        lenA, lenB, lenC = len(A), len(B), len(C)
        nonempty_count = (1 if A else 0) + (1 if B else 0) + (1 if C else 0)

        # p == "**": empty substring matches
        if nonempty_count == 0:
            return 0

        # exactly one literal: shortest match is that literal itself
        if nonempty_count == 1:
            if A:
                return lenA if occA else -1
            if B:
                return lenB if occB else -1
            return lenC if occC else -1

        INF = float('inf')
        ans = INF

        if A and B and C:
            # fix B occurrence b; best a is rightmost A start <= b-lenA,
            # best c is leftmost C start >= b+lenB; both monotone in b.
            ia = -1
            ic = 0
            la, lc = len(occA), len(occC)
            for b in occB:
                ta = b - lenA
                while ia + 1 < la and occA[ia + 1] <= ta:
                    ia += 1
                tc = b + lenB
                while ic < lc and occC[ic] < tc:
                    ic += 1
                if ic == lc:          # no C can ever fit for this or later b
                    break
                if ia < 0:
                    continue
                cand = occC[ic] + lenC - occA[ia]
                if cand < ans:
                    ans = cand
        elif B and C:
            # A empty: leading '*' absorbs prefix, substring starts at b
            ic = 0
            lc = len(occC)
            for b in occB:
                tc = b + lenB
                while ic < lc and occC[ic] < tc:
                    ic += 1
                if ic == lc:
                    break
                cand = occC[ic] + lenC - b
                if cand < ans:
                    ans = cand
        elif A and B:
            # C empty: trailing '*' absorbs suffix, substring ends at b+lenB
            ia = -1
            la = len(occA)
            for b in occB:
                ta = b - lenA
                while ia + 1 < la and occA[ia + 1] <= ta:
                    ia += 1
                if ia < 0:
                    continue
                cand = b + lenB - occA[ia]
                if cand < ans:
                    ans = cand
        else:
            # B empty: p = A + '*' + C ; fix c, best a is rightmost A <= c-lenA
            ia = -1
            la = len(occA)
            for c in occC:
                ta = c - lenA
                while ia + 1 < la and occA[ia + 1] <= ta:
                    ia += 1
                if ia < 0:
                    continue
                cand = c + lenC - occA[ia]
                if cand < ans:
                    ans = cand

        return ans if ans != INF else -1


# ---------------- Test harness ----------------
def brute(s, p):
    n = len(s)
    rx = re.compile(p.replace('*', '.*'))
    for L in range(n + 1):
        for i in range(n - L + 1):
            if rx.fullmatch(s[i:i + L]):
                return L
    return -1


if __name__ == "__main__":
    sol = Solution()

    print("=== Provided examples ===")
    samples = [
        ("abaacbaecebce", "ba*c*ce", 8),
        ("baccbaadbc", "cc*baa*adb", -1),
        ("a", "**", 0),
        ("madlogic", "*adlogi*", 6),
    ]
    all_pass = True
    for idx, (s, p, exp) in enumerate(samples, 1):
        got = sol.shortestMatchingSubstring(s, p)
        ok = got == exp
        all_pass &= ok
        print(f"Example {idx}: s={s!r} p={p!r} -> got {got}, expected {exp}  [{'PASS' if ok else 'FAIL'}]")
    print("Sample verdict:", "PASS" if all_pass else "FAIL")

    print("\n=== Edge cases ===")
    edges = [
        ("xabx", "ab**", 2),          # only A nonempty
        ("xy", "ab**", -1),           # only A nonempty, absent
        ("xbx", "*b*", 1),            # only B nonempty
        ("xyz", "*b*", -1),
        ("xcy", "**c", 1),            # only C nonempty
        ("xyz", "**c", -1),
        ("a", "**", 0),               # empty pattern
        ("abc", "**", 0),
        ("aaa", "a*a*a", 3),          # overlap, must use disjoint A,B,C
        ("aa", "a*a*a", -1),          # too few copies
        ("ab", "ab**", 2),
        ("zabcz", "*b*", 1),
    ]
    edge_fail = 0
    for s, p, exp in edges:
        got = sol.shortestMatchingSubstring(s, p)
        ok = got == exp
        edge_fail += (not ok)
        print(f"s={s!r:10} p={p!r:9} -> got {got}, expected {exp}  [{'PASS' if ok else 'FAIL'}]")
    print("Edge verdict:", "PASS" if edge_fail == 0 else "FAIL")

    print("\n=== Randomized stress vs brute force ===")
    random.seed(12345)
    fails = 0
    trials = 3000
    for t in range(trials):
        n = random.randint(1, 9)
        alpha = random.choice("ab", "abc")
        s = ''.join(random.choice(alpha) for _ in range(n))
        A = ''.join(random.choice(alpha) for _ in range(random.randint(0, 3)))
        B = ''.join(random.choice(alpha) for _ in range(random.randint(0, 3)))
        C = ''.join(random.choice(alpha) for _ in range(random.randint(0, 3)))
        p = A + '*' + B + '*' + C
        got = sol.shortestMatchingSubstring(s, p)
        exp = brute(s, p)
        if got != exp:
            fails += 1
            if fails <= 10:
                print(f"  MISMATCH s={s!r} p={p!r} got={got} exp={exp}")
    print(f"Stress: {trials - fails}/{trials} match brute force", "[PASS]" if fails == 0 else "[FAIL]")

    print("\n=== Timing (n = 100000) ===")
    n = 100000
    s_small = ''.join(random.choice('abc') for _ in range(n))

    t0 = time.time()
    r1 = sol.shortestMatchingSubstring('a' * n, 'a*a*a')
    t1 = time.time()
    print(f"  all-'a' s, p='a*a*a'      -> {r1}   ({t1 - t0:.3f}s)")

    t0 = time.time()
    r2 = sol.shortestMatchingSubstring(s_small, 'a*b*c')
    t1 = time.time()
    print(f"  random abc, p='a*b*c'     -> {r2}   ({t1 - t0:.3f}s)")

    s_big = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n))
    A = s_big[100:110]
    B = s_big[50000:50010]
    C = s_big[90000:90010]
    p_big = A + '*' + B + '*' + C
    t0 = time.time()
    r3 = sol.shortestMatchingSubstring(s_big, p_big)
    t1 = time.time()
    print(f"  embedded parts, long p    -> {r3}   ({t1 - t0:.3f}s)")

    t0 = time.time()
    r4 = sol.shortestMatchingSubstring(s_small, 'zz*zz*zz')
    t1 = time.time()
    print(f"  no-match p='zz*zz*zz'     -> {r4}   ({t1 - t0:.3f}s)")