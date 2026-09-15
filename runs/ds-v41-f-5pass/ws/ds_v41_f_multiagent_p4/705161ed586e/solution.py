from itertools import product


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        s = [ord(ch) - 97 for ch in caption]
        INF = float("inf")

        # Rolling DP arrays corresponding to index i+1: g[i+1][c][L]
        # L = 1, 2, and 3 (meaning >= 3)
        n1 = [INF] * 26
        n2 = [INF] * 26
        n3 = [0] * 26

        # choice[i*26 + c] = character placed at position i for state (i, c, L>=3)
        choice = bytearray(n * 26)

        for i in range(n - 1, 0, -1):
            si = s[i]
            # best / second-best cost of switching to a new run char x at pos i
            # switch cost = |s[i]-x| + g[i+1][x][1]
            b1v, b1x = INF, -1
            b2v, b2x = INF, -1
            for x in range(26):
                d = si - x if si >= x else x - si
                val = d + n1[x]
                if val < b1v:
                    b2v, b2x = b1v, b1x
                    b1v, b1x = val, x
                elif val < b2v:
                    b2v, b2x = val, x

            c1 = [INF] * 26
            c2 = [INF] * 26
            c3 = [INF] * 26
            base = i * 26
            for c in range(26):
                dist = si - c if si >= c else c - si
                c1[c] = dist + n2[c]      # L=1 -> must continue -> L=2
                c2[c] = dist + n3[c]      # L=2 -> must continue -> L=3
                cont = c2[c]              # L>=3 -> continue same char
                if b1x != c:
                    sv, sx = b1v, b1x
                else:
                    sv, sx = b2v, b2x
                if cont < sv:
                    c3[c] = cont
                    choice[base + c] = c
                elif sv < cont:
                    c3[c] = sv
                    choice[base + c] = sx
                else:
                    c3[c] = cont
                    choice[base + c] = sx if (sx != -1 and sx < c) else c
            n1, n2, n3 = c1, c2, c3

        # pick the smallest first character achieving the minimum total cost
        s0 = s[0]
        bv, bx = INF, -1
        for x in range(26):
            d = s0 - x if s0 >= x else x - s0
            val = d + n1[x]
            if val < bv:
                bv = val
                bx = x

        res = [chr(bx + 97)]
        cur_c, cur_L = bx, 1
        for i in range(1, n):
            if cur_L == 3:
                x = choice[i * 26 + cur_c]
            else:
                x = cur_c
            res.append(chr(x + 97))
            if x == cur_c:
                if cur_L < 3:
                    cur_L += 1
            else:
                cur_c, cur_L = x, 1
        return "".join(res)


# ---------------------------------------------------------------------------
# Independent brute force + cross-check harness (runs only as __main__)
# ---------------------------------------------------------------------------

def _compositions(n, minpart=3):
    out = []
    cur = []

    def rec(rem):
        if rem == 0:
            out.append(tuple(cur))
            return
        for p in range(minpart, rem + 1):
            cur.append(p)
            rec(rem - p)
            cur.pop()

    rec(n)
    return out


def _brute_best(s, A=26):
    """Enumerate every good caption over alphabet [0,A) of length len(s).
    Returns (min_cost, lex_smallest) or None if len(s) < 3."""
    n = len(s)
    if n < 3:
        return None
    sv = [ord(ch) - 97 for ch in s]
    best_cost = None
    best_str = None
    for comp in _compositions(n):
        r = len(comp)
        for assign in product(range(A), repeat=r):
            ok = True
            for k in range(r - 1):
                if assign[k] == assign[k + 1]:
                    ok = False
                    break
            if not ok:
                continue
            t = []
            for ch, ln in zip(assign, comp):
                t.extend([ch] * ln)
            cost = 0
            for j in range(n):
                d = sv[j] - t[j]
                if d < 0:
                    d = -d
                cost += d
            cand = "".join(chr(c + 97) for c in t)
            if best_cost is None or cost < best_cost or (cost == best_cost and cand < best_str):
                best_cost = cost
                best_str = cand
    return best_cost, best_str


def _is_good(t):
    n = len(t)
    if n < 3:
        return False
    i = 0
    while i < n:
        j = i
        while j < n and t[j] == t[i]:
            j += 1
        if j - i < 3:
            return False
        i = j
    return True


def _run_cross_check():
    import random
    sol = Solution()

    def cost_of(s, t):
        return sum(abs(ord(a) - ord(b)) for a, b in zip(s, t))

    checked = 0
    mism = []

    def check(s, A):
        nonlocal checked
        b = _brute_best(s, A)
        got = sol.minCostGoodCaption(s)
        exp = "" if b is None else b[1]
        checked += 1
        if got != exp:
            good = _is_good(got) if got else (exp == "")
            gc = cost_of(s, got) if got else 0
            mism.append((s, b, got, gc, good))
            return False
        return True

    # n = 1, 2 -> impossible
    for s in ("a", "z", "ab", "zz"):
        if not check(s, 2):
            return checked, mism

    # exhaustive: lengths 3..7 over alphabets {a,b,c} and {a,b,c,d}
    for k in (3, 4):
        letters = [chr(97 + i) for i in range(k)]
        for L in range(3, 8):
            for tup in product(letters, repeat=L):
                s = "".join(tup)
                if not check(s, k):
                    return checked, mism

    # full 26-letter target alphabet on tiny inputs (extra-strength check)
    for k in (3, 4):
        letters = [chr(97 + i) for i in range(k)]
        for L in range(3, 6):
            for tup in product(letters, repeat=L):
                s = "".join(tup)
                if not check(s, 26):
                    return checked, mism

    # random small / medium inputs
    random.seed(20240517)
    for _ in range(1500):
        k = random.choice([2, 3, 4, 5, 26])
        L = random.randint(3, 8)
        s = "".join(chr(97 + random.randrange(k)) for _ in range(L))
        if not check(s, k if k < 26 else 26):
            return checked, mism

    for _ in range(150):
        k = random.choice([2, 3, 4])
        L = random.randint(9, 11)
        s = "".join(chr(97 + random.randrange(k)) for _ in range(L))
        if not check(s, k):
            return checked, mism

    return checked, mism


if __name__ == "__main__":
    import random
    import time

    sol = Solution()
    assert sol.minCostGoodCaption("cdcd") == "cccc"
    assert sol.minCostGoodCaption("aca") == "aaa"
    assert sol.minCostGoodCaption("bc") == ""
    assert sol.minCostGoodCaption("a") == ""
    print("examples ok:", sol.minCostGoodCaption("cdcd"),
          sol.minCostGoodCaption("aca"), repr(sol.minCostGoodCaption("bc")))

    # crafted: DP state (i, c, L>=3) where the best switch char equals the run char
    print("crafted aaaaabc ->", sol.minCostGoodCaption("aaaaabc"))

    checked, mism = _run_cross_check()
    if mism:
        s, b, got, gc, good = mism[0]
        print("FIRST MISMATCH")
        print("input      :", repr(s))
        print("brute      :", b)
        print("dp output  :", repr(got), "cost", gc, "good", good)
    else:
        print("CROSS-CHECK OK: %d inputs, zero mismatches" % checked)

    random.seed(7)
    big = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(50000))
    t0 = time.perf_counter()
    r = sol.minCostGoodCaption(big)
    dt = time.perf_counter() - t0
    print("n=50000 -> len %d, good %s, %.2f s" % (len(r), _is_good(r), dt))