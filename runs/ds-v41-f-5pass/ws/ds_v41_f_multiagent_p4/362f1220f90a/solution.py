class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # prefix function of str2
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and str2[i] != str2[j]:
                j = pi[j - 1]
            if str2[i] == str2[j]:
                j += 1
            pi[i] = j

        # KMP failure links over states 0..m
        fail = [0] * (m + 1)
        for s in range(1, m + 1):
            fail[s] = pi[s - 1]

        # delta[s][c] = next state
        delta = [[0] * 26 for _ in range(m + 1)]
        for s in range(m + 1):
            row = delta[s]
            if s < m:
                nxt = s + 1
                mc = ord(str2[s]) - 97
                if s == 0:
                    for c in range(26):
                        row[c] = nxt if c == mc else 0
                else:
                    fr = delta[fail[s]]
                    for c in range(26):
                        row[c] = nxt if c == mc else fr[c]
            else:
                fr = delta[fail[s]]
                for c in range(26):
                    row[c] = fr[c]

        # back[t] = bitmask of states s with some c giving delta[s][c] == t
        back = [0] * (m + 1)
        for s in range(m + 1):
            bs = 1 << s
            ds = delta[s]
            for c in range(26):
                back[ds[c]] |= bs

        nstates = m + 1
        nchunks = (nstates + 7) // 8
        tables = []
        for k in range(nchunks):
            tbl = [0] * 256
            base = 8 * k
            for byte in range(1, 256):
                low = byte & (-byte)
                j = low.bit_length() - 1
                prev = tbl[byte ^ low]
                t = base + j
                tbl[byte] = (prev | back[t]) if t <= m else prev
            tables.append(tbl)

        def preimage(A):
            res = 0
            k = 0
            while A:
                res |= tables[k][A & 255]
                A >>= 8
                k += 1
            return res

        full = (1 << nstates) - 1
        F = [0] * (L + 1)
        F[L] = full
        for p in range(L - 1, -1, -1):
            A = F[p + 1]
            if p >= m - 1:
                i = p - m + 1
                if str1[i] == 'T':
                    A &= (1 << m)
                else:
                    A &= ~(1 << m)
            F[p] = preimage(A)

        if not (F[0] & 1):
            return ""

        res = []
        state = 0
        for p in range(L):
            Fnext = F[p + 1]
            ch = str1[p - m + 1] if p >= m - 1 else None
            for c in range(26):
                t = delta[state][c]
                if ch == 'T':
                    if t != m:
                        continue
                elif ch == 'F':
                    if t == m:
                        continue
                if (Fnext >> t) & 1:
                    res.append(chr(97 + c))
                    state = t
                    break
            else:
                return ""
        return ''.join(res)


if __name__ == "__main__":
    import sys, random, itertools
    sys.setrecursionlimit(10000)
    sol = Solution()

    # ---------- provided examples ----------
    examples = [("TFTF", "ab", "ababa"), ("TFTF", "abc", ""), ("F", "d", "a")]
    all_ok = True
    for a, b, exp in examples:
        got = sol.generateString(a, b)
        good = got == exp
        all_ok &= good
        print(f"example str1={a!r} str2={b!r}: got={got!r} exp={exp!r} -> {'PASS' if good else 'FAIL'}")

    # ---------- independent brute force (DFS, lexicographic, full 26 alphabet) ----------
    def brute(str1, str2, limit=3_000_000):
        n = len(str1); m = len(str2); L = n + m - 1
        tgt = [ord(ch) - 97 for ch in str2]
        word = []
        st = {"nodes": 0}

        def check(pos):
            i = pos - m + 1
            if 0 <= i < n:
                eq = True
                for k in range(m):
                    if word[i + k] != tgt[k]:
                        eq = False
                        break
                if str1[i] == 'T' and not eq:
                    return False
                if str1[i] == 'F' and eq:
                    return False
            return True

        def dfs(pos):
            st["nodes"] += 1
            if st["nodes"] > limit:
                raise RuntimeError("limit")
            if pos == L:
                return True
            for ci in range(26):
                word.append(ci)
                if check(pos) and dfs(pos + 1):
                    return True
                word.pop()
            return False

        try:
            if dfs(0):
                return ''.join(chr(97 + x) for x in word)
            return ""
        except RuntimeError:
            return None  # unknown (search too big)

    fails = []
    skipped = 0
    tested = 0

    # exhaustive over every T/F pattern and small str2 alphabets
    for n in range(1, 5):
        for m in range(1, 4):
            for pat in itertools.product('TF', repeat=n):
                str1 = ''.join(pat)
                for s2 in itertools.product('abc', repeat=m):
                    str2 = ''.join(s2)
                    b = brute(str1, str2)
                    if b is None:
                        skipped += 1
                        continue
                    g = sol.generateString(str1, str2)
                    tested += 1
                    if g != b:
                        fails.append((str1, str2, b, g))

    # random trials (str2 random over lowercase; word alphabet still full 26 in brute)
    random.seed(20240517)
    for _ in range(3000):
        n = random.randint(1, 4)
        m = random.randint(1, 3)
        str1 = ''.join(random.choice('TF') for _ in range(n))
        str2 = ''.join(random.choice('abcd') for _ in range(m))
        b = brute(str1, str2)
        if b is None:
            skipped += 1
            continue
        g = sol.generateString(str1, str2)
        tested += 1
        if g != b:
            fails.append((str1, str2, b, g))

    # validity check on larger random inputs (verify returned nonempty strings satisfy all constraints)
    def satisfies(str1, str2, w):
        n = len(str1); m = len(str2)
        if len(w) != n + m - 1:
            return False
        for i in range(n):
            eq = w[i:i + m] == str2
            if str1[i] == 'T' and not eq:
                return False
            if str1[i] == 'F' and eq:
                return False
        return True

    bad_large = []
    for _ in range(400):
        n = random.randint(1, 40)
        m = random.randint(1, 8)
        str1 = ''.join(random.choice('TF') for _ in range(n))
        str2 = ''.join(random.choice('abc') for _ in range(m))
        g = sol.generateString(str1, str2)
        if g != "" and not satisfies(str1, str2, g):
            bad_large.append((str1, str2, g))

    print(f"brute-force compared cases: {tested} (skipped due to search limit: {skipped})")
    print(f"large validity violations: {len(bad_large)}")
    if fails:
        print("COUNTEREXAMPLES FOUND:")
        for f in fails[:10]:
            print("  str1=%r str2=%r brute=%r solution=%r" % f)
    else:
        print("no counterexamples vs brute force")
    print("ALL EXAMPLES PASS" if all_ok else "EXAMPLE FAILURE")