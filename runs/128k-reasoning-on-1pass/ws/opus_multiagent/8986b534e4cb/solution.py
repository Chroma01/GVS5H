import sys, random

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1]); q = int(data[2])

    base = 3
    sub = data[base:base + 2 * m]
    Ss = list(map(int, sub[0::2]))
    Ts = list(map(int, sub[1::2]))
    A = list(map(min, Ss, Ts))
    B = list(map(max, Ss, Ts))
    SG = [0 if s < t else 1 for s, t in zip(Ss, Ts)]
    del Ss, Ts, sub

    grb = random.getrandbits
    TAG = [grb(61) for _ in range(m)]

    bit0 = [0] * (n + 2)
    bit1 = [0] * (n + 2)
    TREES = (bit0, bit1)
    cntL = [0] * (n + 2)
    cntR = [0] * (n + 2)
    minL = [0] * m
    L = 0

    for R in range(m):
        a = A[R]; b = B[R]; s = SG[R]
        tree = TREES[s]
        # D = prefixXor(a) ^ prefixXor(b) computed on the symmetric difference
        # of the two Fenwick chains (they merge, common nodes cancel).
        i = a; j = b; D = 0
        while i != j:
            if i > j:
                D ^= tree[i]
                i &= i - 1
            else:
                D ^= tree[j]
                j &= j - 1
        while D or cntL[a] or cntR[b]:
            aj = A[L]; bj = B[L]; sj = SG[L]; tg = TAG[L]
            cntL[aj] -= 1
            cntR[bj] -= 1
            t2 = TREES[sj]
            # remove: XOR tag at aj+1 and bj (paths merge -> stop when equal)
            i = aj + 1; j = bj
            while i != j:
                if i < j:
                    if i > n:
                        break
                    t2[i] ^= tg
                    i += i & (-i)
                else:
                    if j > n:
                        break
                    t2[j] ^= tg
                    j += j & (-j)
            if sj == s:
                if (aj < a < bj) != (aj < b < bj):
                    D ^= tg
            L += 1
        # insert R
        cntL[a] += 1
        cntR[b] += 1
        tg = TAG[R]
        i = a + 1; j = b
        while i != j:
            if i < j:
                if i > n:
                    break
                tree[i] ^= tg
                i += i & (-i)
            else:
                if j > n:
                    break
                tree[j] ^= tg
                j += j & (-j)
        minL[R] = L

    tail = data[base + 2 * m:]
    Lq = list(map(int, tail[0::2]))
    Rq = list(map(int, tail[1::2]))
    out = ["Yes" if l - 1 >= minL[r - 1] else "No" for l, r in zip(Lq, Rq)]
    sys.stdout.write("\n".join(out) + "\n")


# ---------------------------------------------------------------------------
# Standalone brute-force validator (only runs with:  python sol.py --selftest)
# and benchmark harness (--bench).  Neither touches the judge path.
# ---------------------------------------------------------------------------

def _bf_feasible(items):
    """Exact feasibility by difference constraints.
    items: list of (a, b, s) with a < b, b - a >= 2, s == 0 => rightward
    (interior potentials strictly greater), s == 1 => leftward (strictly less).
    Constraints:  P_a = P_b  and for a<c<b:  P_c > P_a (s=0) / P_c < P_a (s=1).
    Feasible over the integers  <=>  after contracting equality classes the
    strict-inequality digraph has no self loop and no directed cycle."""
    par = {}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for (a, b, s) in items:
        for c in range(a, b + 1):
            if c not in par:
                par[c] = c
    for (a, b, s) in items:
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb

    adj = {}
    for (a, b, s) in items:
        ra = find(a)
        for c in range(a + 1, b):
            rc = find(c)
            if rc == ra:
                return False            # self loop: P_c > P_c (or <)
            if s == 0:
                u, v = ra, rc           # P_rc > P_ra
            else:
                u, v = rc, ra           # P_ra > P_rc
            adj.setdefault(u, set()).add(v)

    color = {}
    for start in list(adj.keys()):
        if color.get(start, 0) != 0:
            continue
        color[start] = 1
        stack = [(start, iter(adj.get(start, ())))]
        while stack:
            node, it = stack[-1]
            advanced = False
            for nx in it:
                c = color.get(nx, 0)
                if c == 1:
                    return False        # back edge => directed cycle
                if c == 0:
                    color[nx] = 1
                    stack.append((nx, iter(adj.get(nx, ()))))
                    advanced = True
                    break
            if not advanced:
                color[node] = 2
                stack.pop()
    return True


def _criterion(items):
    """Pairwise criterion used by the submitted solution:
    infeasible iff two items share a left endpoint, share a right endpoint,
    or properly cross with the same sign."""
    k = len(items)
    for i in range(k):
        a1, b1, s1 = items[i]
        for j in range(i + 1, k):
            a2, b2, s2 = items[j]
            if a1 == a2 or b1 == b2:
                return False
            if s1 == s2 and (a1 < a2 < b1 < b2 or a2 < a1 < b2 < b1):
                return False
    return True


def _run_main(inp_bytes):
    import io

    class _FakeIn(object):
        pass

    old_in, old_out = sys.stdin, sys.stdout
    fi = _FakeIn()
    fi.buffer = io.BytesIO(inp_bytes)
    out = io.StringIO()
    sys.stdin = fi
    sys.stdout = out
    try:
        main()
    finally:
        sys.stdin = old_in
        sys.stdout = old_out
    return out.getvalue().split()


SAMPLE1_IN = b"""5 4 2
4 2
1 3
3 5
2 4
1 3
2 4
"""
SAMPLE1_OUT = ["Yes", "No"]

SAMPLE2_IN = b"""7 6 3
1 5
2 4
4 6
7 1
5 3
1 6
1 6
4 4
2 5
"""
SAMPLE2_OUT = ["No", "Yes", "Yes"]


def _check_samples():
    bad = 0
    for name, inp, exp in (("sample1", SAMPLE1_IN, SAMPLE1_OUT),
                           ("sample2", SAMPLE2_IN, SAMPLE2_OUT)):
        got = _run_main(inp)
        if got != exp:
            bad += 1
            print("SAMPLE MISMATCH %s: got %s expected %s" % (name, got, exp))
        else:
            print("%s OK: %s" % (name, got))
    # run each sample a few more times: TAG values are random, so this checks
    # that the answers do not depend on the particular hash draw
    for rep in range(30):
        if _run_main(SAMPLE1_IN) != SAMPLE1_OUT or \
           _run_main(SAMPLE2_IN) != SAMPLE2_OUT:
            bad += 1
            print("SAMPLE MISMATCH on repeat %d (random tags)" % rep)
            break
    return bad


def _selftest():
    import itertools
    bad = _check_samples()

    # ---- explicit hand-made cases ------------------------------------
    named = [
        ("touching chain same sign", [(1, 3, 0), (3, 5, 0)]),
        ("touching chain diff sign", [(1, 3, 0), (3, 5, 1)]),
        ("opposite sign crossing", [(1, 3, 0), (2, 4, 1)]),
        ("same sign crossing", [(1, 3, 0), (2, 4, 0)]),
        ("nesting same sign", [(1, 5, 0), (2, 4, 0)]),
        ("nesting opposite sign", [(1, 5, 0), (2, 4, 1)]),
        ("nesting shared left", [(1, 5, 0), (1, 3, 1)]),
        ("nesting shared right", [(1, 5, 0), (3, 5, 1)]),
        ("duplicate opposite signs", [(1, 4, 0), (1, 4, 1)]),
        ("3 chain + crossing", [(1, 3, 0), (3, 5, 0), (2, 4, 1)]),
    ]
    for name, items in named:
        if _bf_feasible(items) != _criterion(items):
            bad += 1
            print("COUNTEREXAMPLE (named %s): %s bf=%s crit=%s" %
                  (name, items, _bf_feasible(items), _criterion(items)))

    # ---- exhaustive over all subsets, small N -------------------------
    for n in (3, 4, 5, 6):
        allit = [(a, b, s) for a in range(1, n + 1) for b in range(a + 2, n + 1)
                 for s in (0, 1)]
        for size in range(0, 5):
            for comb in itertools.combinations(allit, size):
                items = list(comb)
                f1 = _bf_feasible(items)
                f2 = _criterion(items)
                if f1 != f2:
                    bad += 1
                    print("COUNTEREXAMPLE n=%d %s bf=%s crit=%s" %
                          (n, items, f1, f2))
                    if bad > 20:
                        return

    # ---- random subsets of size 5 for N = 7, 8 ------------------------
    rnd = random.Random(12345)
    for n in (7, 8):
        allit = [(a, b, s) for a in range(1, n + 1) for b in range(a + 2, n + 1)
                 for s in (0, 1)]
        for _ in range(20000):
            items = rnd.sample(allit, min(5, len(allit)))
            f1 = _bf_feasible(items)
            f2 = _criterion(items)
            if f1 != f2:
                bad += 1
                print("COUNTEREXAMPLE(rand) n=%d %s bf=%s crit=%s" %
                      (n, items, f1, f2))
                if bad > 20:
                    return

    # ---- end-to-end check of main() against the brute force -----------
    for it in range(500):
        n = rnd.randint(3, 10)
        allpairs = [(s, t) for s in range(1, n + 1) for t in range(1, n + 1)
                    if abs(s - t) > 1]
        if not allpairs:
            continue
        m = rnd.randint(1, min(7, len(allpairs)))
        ppl = rnd.sample(allpairs, m)
        items = []
        for (s, t) in ppl:
            if s < t:
                items.append((s, t, 0))
            else:
                items.append((t, s, 1))
        qs = [(l, r) for l in range(1, m + 1) for r in range(l, m + 1)]
        lines = ["%d %d %d" % (n, m, len(qs))]
        for (s, t) in ppl:
            lines.append("%d %d" % (s, t))
        for (l, r) in qs:
            lines.append("%d %d" % (l, r))
        inp = ("\n".join(lines) + "\n").encode()
        got = _run_main(inp)
        exp = ["Yes" if _bf_feasible(items[l - 1:r]) else "No" for (l, r) in qs]
        if got != exp:
            bad += 1
            print("E2E MISMATCH input:\n" + inp.decode())
            print("got", got)
            print("exp", exp)
            if bad > 5:
                return

    if bad == 0:
        print("all tests passed: no counterexample found")


def _gen(kind, n=400000, m=200000, q=200000, seed=1):
    rnd = random.Random(seed)
    pairs = []
    seen = set()
    if kind == "random":
        while len(pairs) < m:
            s = rnd.randint(1, n)
            t = rnd.randint(1, n)
            if abs(s - t) <= 1 or (s, t) in seen:
                continue
            seen.add((s, t))
            pairs.append((s, t))
    elif kind == "cross":
        # consecutive persons are same-sign properly crossing => a pop almost
        # every step (total pops still O(M), but the window churns maximally)
        span = n // 3
        x = 1
        while len(pairs) < m:
            s = x
            t = x + span
            if t > n:
                x = 1
                span = max(3, span - 1)
                continue
            if (s, t) not in seen:
                seen.add((s, t))
                pairs.append((s, t))
            x += 1
    else:  # "long": maximal Fenwick chain lengths
        while len(pairs) < m:
            a = rnd.randint(1, n // 2)
            b = rnd.randint(n // 2 + 1, n)
            if b - a <= 1:
                continue
            s, t = (a, b) if rnd.getrandbits(1) else (b, a)
            if (s, t) in seen:
                continue
            seen.add((s, t))
            pairs.append((s, t))
    out = ["%d %d %d" % (n, m, q)]
    for (s, t) in pairs:
        out.append("%d %d" % (s, t))
    for _ in range(q):
        l = rnd.randint(1, m)
        r = rnd.randint(l, m)
        out.append("%d %d" % (l, r))
    return ("\n".join(out) + "\n").encode()


def _bench():
    import time
    for kind in ("random", "cross", "long"):
        inp = _gen(kind)
        t0 = time.perf_counter()
        _run_main(inp)
        t1 = time.perf_counter()
        print("%-7s : %.3f s" % (kind, t1 - t0))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        _selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "--bench":
        _bench()
    elif len(sys.argv) > 1 and sys.argv[1] == "--samples":
        _check_samples()
    else:
        main()