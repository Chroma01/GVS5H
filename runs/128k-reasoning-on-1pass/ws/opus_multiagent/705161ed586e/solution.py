import os


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        s = caption
        n = len(s)
        if n < 3:
            return ""

        # rows[v][c] = |v - c|
        rows = [tuple(abs(v - c) for c in range(26)) for v in range(26)]
        vals = [ord(ch) - 97 for ch in s]
        C = [rows[v] for v in vals]

        # h[j][c] : min cost of suffix j, given the run ending at j-1 has char c
        #           and already has length >= 3.  h[n][c] = 0.
        h = [None] * (n + 1)
        h[n] = [0] * 26

        for j in range(n - 1, -1, -1):
            cj = C[j]
            hn = h[j + 1]
            t = [a + b for a, b in zip(cj, hn)]           # continue current char
            if j + 3 <= n:
                cj1 = C[j + 1]
                cj2 = C[j + 2]
                h3 = h[j + 3]
                # g[j][d] = |s[j]-d|+|s[j+1]-d|+|s[j+2]-d| + h[j+3][d]
                # Since g[j][c] >= C[j][c] + h[j+1][c], using the *global* min
                # (instead of min over d != c) is safe.
                m1 = min(a + b + c + d for a, b, c, d in zip(cj, cj1, cj2, h3))
                h[j] = [x if x < m1 else m1 for x in t]
            else:
                h[j] = t

        # ---------------- reconstruction (lexicographically smallest optimum) ----------------
        c0 = C[0]
        c1 = C[1]
        c2 = C[2]
        h3 = h[3]
        best = None
        cur = 0
        for d in range(26):
            v = c0[d] + c1[d] + c2[d] + h3[d]
            if best is None or v < best:
                best = v
                cur = d

        res = [cur, cur, cur]
        j = 3
        while j < n:
            target = h[j][cur]
            cj = C[j]
            hj1 = h[j + 1]
            can_block = (j + 3 <= n)
            if can_block:
                cj1 = C[j + 1]
                cj2 = C[j + 2]
                hj3 = h[j + 3]
            chosen = -1
            for d in range(26):
                if d == cur:
                    if cj[cur] + hj1[cur] == target:
                        chosen = d
                        res.append(cur)
                        j += 1
                        break
                else:
                    if can_block and (cj[d] + cj1[d] + cj2[d] + hj3[d]) == target:
                        chosen = d
                        res.append(d)
                        res.append(d)
                        res.append(d)
                        cur = d
                        j += 3
                        break
            if chosen == -1:
                # unreachable: target is always attainable by some transition
                return ""

        return "".join(chr(97 + x) for x in res)


# --------------------------------------------------------------------------------------
# Brute-force validator (inert unless the env var RUN_BRUTE is set).
# --------------------------------------------------------------------------------------
def _brute(s: str) -> str:
    import itertools
    n = len(s)
    if n < 3:
        return ""
    vals = [ord(c) - 97 for c in s]
    lo = max(0, min(vals) - 1)
    hi = min(25, max(vals) + 1)
    best = None
    for t in itertools.product(range(lo, hi + 1), repeat=n):
        ok = True
        i = 0
        while i < n:
            k = i
            while k < n and t[k] == t[i]:
                k += 1
            if k - i < 3:
                ok = False
                break
            i = k
        if not ok:
            continue
        cost = 0
        for a, b in zip(vals, t):
            cost += a - b if a > b else b - a
        st = "".join(chr(97 + x) for x in t)
        if best is None or cost < best[0] or (cost == best[0] and st < best[1]):
            best = (cost, st)
    return best[1] if best else ""


def _cost(s, t):
    if t == "":
        return None
    return sum(abs(ord(a) - ord(b)) for a, b in zip(s, t))


def _run_tests():
    import itertools
    import random

    sol = Solution()
    bad = 0

    # n = 1, 2 must be impossible
    for n in (1, 2):
        for tup in itertools.product("abc", repeat=n):
            s = "".join(tup)
            got = sol.minCostGoodCaption(s)
            if got != "":
                print("MISMATCH (short):", s, "expected '' got", got)
                bad += 1

    # exhaustive: n = 3..6 over {'a'..'d'}
    for n in range(3, 7):
        for tup in itertools.product("abcd", repeat=n):
            s = "".join(tup)
            exp = _brute(s)
            got = sol.minCostGoodCaption(s)
            if exp != got:
                print("MISMATCH:", s, "expected", exp, _cost(s, exp),
                      "got", got, _cost(s, got))
                bad += 1
                if bad > 20:
                    return

    # random: n = 7..9 over {'a'..'e'} and over 'a'..'z' (clipped alphabets)
    random.seed(12345)
    for _ in range(400):
        n = random.randint(7, 9)
        alpha = random.choice(["abcde", "abc", "xyz", "acegi"])
        s = "".join(random.choice(alpha) for _ in range(n))
        exp = _brute(s)
        got = sol.minCostGoodCaption(s)
        if exp != got:
            print("MISMATCH:", s, "expected", exp, _cost(s, exp),
                  "got", got, _cost(s, got))
            bad += 1
            if bad > 20:
                return

    # samples
    for s, exp in [("cdcd", "cccc"), ("aca", "aaa"), ("bc", "")]:
        got = sol.minCostGoodCaption(s)
        if got != exp:
            print("SAMPLE MISMATCH:", s, exp, got)
            bad += 1

    # big performance / validity smoke test
    import time
    big = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(50000))
    t0 = time.time()
    out = sol.minCostGoodCaption(big)
    t1 = time.time()
    assert len(out) == len(big)
    i = 0
    while i < len(out):
        k = i
        while k < len(out) and out[k] == out[i]:
            k += 1
        assert k - i >= 3, "bad run in big output"
        i = k
    print("big n=50000 time: %.3fs cost=%d" % (t1 - t0, _cost(big, out)))

    print("done, mismatches:", bad)


if __name__ == "__main__" and os.environ.get("RUN_BRUTE"):
    _run_tests()