import sys
import random

# ================= submitted solution (refactored: input str -> list of answers) =================
def solve(inp):
    vals = list(map(int, inp.split()))
    p = 0
    N = vals[p]; M = vals[p+1]; Q = vals[p+2]; p += 3
    M1 = M + 1
    Ls = [0]*M1; Rs = [0]*M1; Ts = [0]*M1
    allv = [0]*(2*M)
    k = 0
    for i in range(1, M1):
        s = vals[p]; t = vals[p+1]; p += 2
        if s < t:
            Ls[i] = s; Rs[i] = t          # type 0 = U (endpoints strict min)
        else:
            Ls[i] = t; Rs[i] = s; Ts[i] = 1  # type 1 = D (endpoints strict max)
        allv[k] = s; allv[k+1] = t; k += 2
    qL = [0]*Q; qR = [0]*Q
    for i in range(Q):
        qL[i] = vals[p]; qR[i] = vals[p+1]; p += 2
    del vals

    xs = sorted(set(allv))
    del allv
    cidx = {v: i for i, v in enumerate(xs)}
    K = len(xs)
    size = 1
    while size < K:
        size <<= 1
    INF = N + 1
    QL = [0]*M1; QR = [0]*M1; LeafL = [0]*M1; LeafR = [0]*M1
    for i in range(1, M1):
        li = cidx[Ls[i]]; ri = cidx[Rs[i]]
        QL[i] = li + 1          # query range [li+1, ri) = coords strictly between l and r
        QR[i] = ri
        LeafL[i] = li + size
        LeafR[i] = ri + size
    del cidx

    # Per type: mn-tree over r-coordinates (stores left endpoint, min),
    #           mx-tree over l-coordinates (stores right endpoint, max).
    mn0 = [INF]*(2*size); mx0 = [0]*(2*size)
    mn1 = [INF]*(2*size); mx1 = [0]*(2*size)
    cntL = [0]*(N+1); cntR = [0]*(N+1)
    limit = [0]*M1
    R = 0
    for L in range(1, M1):
        if R < L:
            # empty window: person L can always be added, skip checks
            l = Ls[L]; r = Rs[L]
            cntL[l] = 1; cntR[r] = 1
            if Ts[L]:
                mna = mn1; mxa = mx1
            else:
                mna = mn0; mxa = mx0
            i = LeafR[L]
            mna[i] = l
            i >>= 1
            while i:
                c = i << 1
                x = mna[c]; y = mna[c | 1]
                mna[i] = x if x < y else y
                i >>= 1
            i = LeafL[L]
            mxa[i] = r
            i >>= 1
            while i:
                c = i << 1
                x = mxa[c]; y = mxa[c | 1]
                mxa[i] = x if x > y else y
                i >>= 1
            R = L
        while R < M:
            pr = R + 1
            l = Ls[pr]; r = Rs[pr]
            if cntL[l] or cntR[r]:
                break
            if Ts[pr]:
                mna = mn1; mxa = mx1
            else:
                mna = mn0; mxa = mx0
            li = QL[pr]; ri = QR[pr]
            ok = True
            if li < ri:
                a = li + size; b = ri + size
                while a < b:
                    if a & 1:
                        if mna[a] < l or mxa[a] > r:
                            ok = False; break
                        a += 1
                    if b & 1:
                        b -= 1
                        if mna[b] < l or mxa[b] > r:
                            ok = False; break
                    a >>= 1; b >>= 1
            if not ok:
                break
            cntL[l] = 1; cntR[r] = 1
            i = LeafR[pr]
            mna[i] = l
            i >>= 1
            while i:
                c = i << 1
                x = mna[c]; y = mna[c | 1]
                mna[i] = x if x < y else y
                i >>= 1
            i = LeafL[pr]
            mxa[i] = r
            i >>= 1
            while i:
                c = i << 1
                x = mxa[c]; y = mxa[c | 1]
                mxa[i] = x if x > y else y
                i >>= 1
            R = pr
        limit[L] = R
        if R >= L:
            l = Ls[L]; r = Rs[L]
            cntL[l] = 0; cntR[r] = 0
            if Ts[L]:
                mna = mn1; mxa = mx1
            else:
                mna = mn0; mxa = mx0
            i = LeafR[L]
            mna[i] = INF
            i >>= 1
            while i:
                c = i << 1
                x = mna[c]; y = mna[c | 1]
                mna[i] = x if x < y else y
                i >>= 1
            i = LeafL[L]
            mxa[i] = 0
            i >>= 1
            while i:
                c = i << 1
                x = mxa[c]; y = mxa[c | 1]
                mxa[i] = x if x > y else y
                i >>= 1

    out = []
    ap = out.append
    for i in range(Q):
        ap("Yes" if qR[i] <= limit[qL[i]] else "No")
    return out

# ================= exact brute force: Bellman-Ford on difference constraints =================
def feasible(people, N):
    # variables P[1..N]; edge (u,v,w): P[v] <= P[u] + w. Infeasible iff negative cycle.
    edges = []
    for (s, t) in people:
        l, r = (s, t) if s < t else (t, s)
        # P[l] = P[r]  (stamina 0 at both endpoints)
        edges.append((l, r, 0))
        edges.append((r, l, 0))
        if s < t:
            # U: interior strictly greater: P[x] >= P[l]+1  <=>  P[l] <= P[x]-1
            for x in range(l+1, r):
                edges.append((x, l, -1))
        else:
            # D: interior strictly smaller: P[x] <= P[l]-1
            for x in range(l+1, r):
                edges.append((l, x, -1))
    dist = [0]*(N+1)  # super-source with 0 edges to all nodes (all dist start 0)
    for _ in range(N):
        updated = False
        for (u, v, w) in edges:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for (u, v, w) in edges:
        if dist[v] > dist[u] + w:
            return False
    return True

# ================= test driver =================
def make_input(N, people, queries):
    parts = ["%d %d %d" % (N, len(people), len(queries))]
    for (s, t) in people:
        parts.append("%d %d" % (s, t))
    for (l, r) in queries:
        parts.append("%d %d" % (l, r))
    return "\n".join(parts) + "\n"

def all_pairs(N):
    return [(s, t) for s in range(1, N+1) for t in range(1, N+1) if abs(s-t) > 1]

def check(N, people, queries, tag):
    inp = make_input(N, people, queries)
    got = solve(inp)
    for idx, (L, R) in enumerate(queries):
        exp = "Yes" if feasible(people[L-1:R], N) else "No"
        if got[idx] != exp:
            print("MISMATCH [%s] query #%d = (%d,%d): expected %s, got %s"
                  % (tag, idx+1, L, R, exp, got[idx]))
            print("Input:")
            print(inp)
            return False
    return True

def main():
    total = 0

    # 0) sanity: provided samples
    s1 = "5 4 2\n4 2\n1 3\n3 5\n2 4\n1 3\n2 4\n"
    assert solve(s1) == ["Yes", "No"], "sample 1 failed"
    s2 = "7 6 3\n1 5\n2 4\n4 6\n7 1\n5 3\n1 6\n1 6\n4 4\n2 5\n"
    assert solve(s2) == ["No", "Yes", "Yes"], "sample 2 failed"
    print("samples OK")

    # 1) exhaustive over all subsets of people for N = 3,4,5 (all queries)
    for N in (3, 4, 5):
        pairs = all_pairs(N)
        np_ = len(pairs)
        for mask in range(1, 1 << np_):
            people = [pairs[i] for i in range(np_) if (mask >> i) & 1]
            M = len(people)
            queries = [(L, R) for L in range(1, M+1) for R in range(L, M+1)]
            if not check(N, people, queries, "exhaustive N=%d mask=%d" % (N, mask)):
                return
            total += 1
        print("exhaustive N=%d OK (%d subsets)" % (N, (1 << np_) - 1))

    # 2) targeted edge-case batteries
    #    distance-2 intervals, touching intervals, shared endpoints across types
    for N in (3, 4, 5, 6):
        pairs = all_pairs(N)
        # all pairs of people (ordered placements), all 4 query combos
        for i in range(len(pairs)):
            for j in range(len(pairs)):
                if i == j:
                    continue
                people = [pairs[i], pairs[j]]
                queries = [(1, 1), (2, 2), (1, 2)]
                if not check(N, people, queries, "pairs N=%d" % N):
                    return
                total += 1
    print("targeted pair batteries OK")

    # 3) random tests
    rng = random.Random(123456789)
    ITERS = 20000
    for it in range(ITERS):
        N = rng.randint(3, 8)
        pairs = all_pairs(N)
        rng.shuffle(pairs)
        M = rng.randint(1, min(len(pairs), 10))
        people = pairs[:M]
        Q = rng.randint(1, 15)
        queries = []
        for _ in range(Q):
            a = rng.randint(1, M)
            b = rng.randint(a, M)
            queries.append((a, b))
        if not check(N, people, queries, "random it=%d" % it):
            return
        total += 1
    print("random tests OK (%d iterations)" % ITERS)

    print("ALL TESTS PASSED: %d test cases checked" % total)

main()