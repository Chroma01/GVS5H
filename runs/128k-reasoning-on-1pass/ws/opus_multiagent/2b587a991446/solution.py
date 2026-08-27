import sys

BIG = 1 << 60


# ---------------------------------------------------------------- graph utils
def build(N, us, vs):
    """CSR adjacency, vertices are 1-indexed (arrays of size N+2)."""
    M = len(us)
    deg = [0] * (N + 2)
    for x in us:
        deg[x] += 1
    for x in vs:
        deg[x] += 1
    start = [0] * (N + 2)
    s = 0
    for i in range(1, N + 1):
        start[i] = s
        s += deg[i]
    start[N + 1] = s
    pos = start[:]
    adj = [0] * (2 * M)
    for u, v in zip(us, vs):
        p = pos[u]
        adj[p] = v
        pos[u] = p + 1
        p = pos[v]
        adj[p] = u
        pos[v] = p + 1
    return deg, start, adj


def bfs(N, start, adj, src, ban=0):
    """BFS distances (-1 = unreachable / banned).  Returns (dist, bfs_order)."""
    dist = [-1] * (N + 1)
    if ban:
        if ban == src:
            return dist, []
        dist[ban] = -2
    dist[src] = 0
    q = [src]
    qi = 0
    push = q.append
    while qi < len(q):
        u = q[qi]
        qi += 1
        du = dist[u] + 1
        for w in adj[start[u]:start[u + 1]]:
            if dist[w] == -1:
                dist[w] = du
                push(w)
    if ban:
        dist[ban] = -1
    return dist, q


# ---------------------------------------------------------------- formula
def formula(N, M, us, vs, S, T, deg, start, adj):
    # ---- impossible iff G is a simple path -------------------------------
    if M == N - 1:
        mx = 0
        for i in range(1, N + 1):
            if deg[i] > mx:
                mx = deg[i]
        if mx <= 2:
            return -1

    dS, orderS = bfs(N, start, adj, S)
    dT, orderT = bfs(N, start, adj, T)
    d = dS[T]

    # ---- reconstruct one shortest S-T path, test its uniqueness ----------
    path = [T]
    cur = T
    while cur != S:
        dv = dS[cur] - 1
        for u in adj[start[cur]:start[cur + 1]]:
            if dS[u] == dv:
                cur = u
                break
        path.append(cur)
    path.reverse()

    uniq = True
    for i in range(1, len(path)):
        v = path[i]
        dv = dS[v] - 1
        c = 0
        for u in adj[start[v]:start[v + 1]]:
            if dS[u] == dv:
                c += 1
                if c > 1:
                    break
        if c > 1:
            uniq = False
            break
    if not uniq:
        # two distinct shortest paths  ->  rotate along them; 2d is also the
        # trivial lower bound (A walks >= d, B walks >= d)
        return 2 * d

    best = BIG

    # ---- R = d + (shortest simple S-T path different from P*) ------------
    if M > N - 1:                       # a tree has no second simple path
        pidx = [-1] * (N + 1)
        for i, v in enumerate(path):
            pidx[v] = i
        HUGE = 1 << 30
        anc = [0] * (N + 1)             # min over shortest S->v paths of deepest P*-index
        for v in orderS:
            p = pidx[v]
            if p >= 0:
                anc[v] = p
            else:
                b = HUGE
                dv = dS[v] - 1
                for u in adj[start[v]:start[v + 1]]:
                    if dS[u] == dv:
                        a = anc[u]
                        if a < b:
                            b = a
                anc[v] = b
        dnc = [0] * (N + 1)             # max over shortest v->T paths of shallowest P*-index
        for v in orderT:
            p = pidx[v]
            if p >= 0:
                dnc[v] = p
            else:
                b = -1
                dv = dT[v] - 1
                for u in adj[start[v]:start[v + 1]]:
                    if dT[u] == dv:
                        a = dnc[u]
                        if a > b:
                            b = a
                dnc[v] = b

        bc = BIG
        for u, v in zip(us, vs):
            if pidx[u] >= 0 and pidx[v] >= 0:
                continue                # edge of P* (no chords can exist)
            if anc[u] < dnc[v]:
                c = dS[u] + 1 + dT[v]
                if c < bc:
                    bc = c
            if anc[v] < dnc[u]:
                c = dS[v] + 1 + dT[u]
                if c < bc:
                    bc = c
        if bc < BIG:
            best = d + bc

    # X >= 2d+4 and Y >= 2d+2 always, so we may stop early
    if best <= 2 * d + 2:
        return best

    # ---- dodge candidates ------------------------------------------------
    dS2, _ = bfs(N, start, adj, S, T)   # distances from S avoiding T
    dT2, _ = bfs(N, start, adj, T, S)   # distances from T avoiding S
    minf = BIG
    ming = BIG
    for v in range(1, N + 1):
        if deg[v] >= 3:
            fv = dS[v] + dT[v]
            if fv < minf:
                minf = fv
            a = dS2[v]
            b = dT2[v]
            if a >= 0 and b >= 0:
                g = a + b
                if g < ming:
                    ming = g
    if minf < BIG:
        c = 2 * minf + 4                # double dodge
        if c < best:
            best = c
    if ming < BIG:
        c = ming + d + 2                # single dodge
        if c < best:
            best = c
    return best if best < BIG else -1


# ---------------------------------------------------------------- brute force
def brute(N, start, adj, S, T):
    K = N + 1
    dist = [-1] * (K * K)
    st = S * K + T
    dist[st] = 0
    q = [st]
    qi = 0
    goal = T * K + S
    push = q.append
    while qi < len(q):
        c = q[qi]
        qi += 1
        if c == goal:
            return dist[c]
        nd = dist[c] + 1
        a, b = divmod(c, K)
        for na in adj[start[a]:start[a + 1]]:
            if na != b:
                s2 = na * K + b
                if dist[s2] < 0:
                    dist[s2] = nd
                    push(s2)
        aK = a * K
        for nb in adj[start[b]:start[b + 1]]:
            if nb != a:
                s2 = aK + nb
                if dist[s2] < 0:
                    dist[s2] = nd
                    push(s2)
    return -1


def solve(N, M, us, vs, S, T):
    deg, start, adj = build(N, us, vs)
    if N <= 50 and N * M <= 15000:
        return brute(N, start, adj, S, T)
    return formula(N, M, us, vs, S, T, deg, start, adj)


# ---------------------------------------------------------------- test harness
def _connected(n, edges):
    adjl = [[] for _ in range(n + 1)]
    for u, v in edges:
        adjl[u].append(v)
        adjl[v].append(u)
    seen = [False] * (n + 1)
    seen[1] = True
    st = [1]
    c = 1
    while st:
        u = st.pop()
        for w in adjl[u]:
            if not seen[w]:
                seen[w] = True
                c += 1
                st.append(w)
    return c == n


def gen_all_connected(n):
    alled = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    m = len(alled)
    for mask in range(1 << m):
        if bin(mask).count('1') < n - 1:
            continue
        edges = [alled[k] for k in range(m) if (mask >> k) & 1]
        if _connected(n, edges):
            yield edges


def gen_random_connected(n, rnd, extra):
    perm = list(range(1, n + 1))
    rnd.shuffle(perm)
    edges = set()
    for i in range(1, n):
        j = rnd.randrange(i)
        a, b = perm[i], perm[j]
        edges.add((min(a, b), max(a, b)))
    allp = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    rnd.shuffle(allp)
    for e in allp:
        if len(edges) >= n - 1 + extra:
            break
        edges.add(e)
    return sorted(edges)


def run_tests():
    import random
    ok = True

    def check(name, N, edges, S, T, expected=None):
        nonlocal ok
        us = [e[0] for e in edges]
        vs = [e[1] for e in edges]
        deg, start, adj = build(N, us, vs)
        b = brute(N, start, adj, S, T)
        fo = formula(N, len(edges), us, vs, S, T, deg, start, adj)
        if expected is not None and b != expected:
            print("BRUTE MISMATCH", name, "got", b, "want", expected)
            ok = False
        if b != fo:
            print("FORMULA MISMATCH", name, N, edges, S, T, "brute", b, "formula", fo)
            ok = False
        return b

    check("sample1", 4, [(2, 4), (1, 4), (3, 4), (2, 3)], 3, 4, 3)
    check("sample2", 2, [(1, 2)], 1, 2, -1)
    check("sample3", 5, [(1, 2), (2, 3), (1, 5), (2, 4), (1, 3), (2, 5)], 3, 5, 4)
    check("tri+tail", 5, [(1, 2), (2, 3), (1, 3), (1, 4), (4, 5)], 5, 4, 10)
    check("tree", 5, [(1, 2), (2, 3), (3, 4), (3, 5)], 1, 2, 10)
    check("C5", 5, [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)], 1, 2, 5)
    check("C6", 6, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 6)], 1, 2, 6)
    check("star", 4, [(1, 4), (2, 4), (3, 4)], 1, 2, 6)
    check("corridor", 6, [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)], 3, 1, 12)
    check("corr2", 6, [(5, 6), (6, 2), (2, 1), (1, 3), (1, 4)], 5, 6, 14)
    check("2tri", 5, [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (3, 5)], 1, 5, 5)
    for k in range(1, 4):
        n = 4 + 2 * k
        ed = [(1, 2), (2, 3), (3, 4), (1, 4)]
        prev = 1
        for t in range(k):
            ed.append((prev, 5 + t))
            prev = 5 + t
        s = prev
        prev = 3
        for t in range(k):
            ed.append((prev, 5 + k + t))
            prev = 5 + k + t
        check("C4tail%d" % k, n, ed, s, prev, 4 * k + 4)

    for n in (4, 5):
        for edges in gen_all_connected(n):
            us = [e[0] for e in edges]
            vs = [e[1] for e in edges]
            deg, start, adj = build(n, us, vs)
            for S in range(1, n + 1):
                for T in range(1, n + 1):
                    if S == T:
                        continue
                    a = brute(n, start, adj, S, T)
                    f = formula(n, len(edges), us, vs, S, T, deg, start, adj)
                    if a != f:
                        print("FORMULA MISMATCH exh", n, edges, S, T, a, f)
                        ok = False

    rnd = random.Random(12345)
    for it in range(3000):
        n = rnd.randint(4, 9)
        extra = rnd.randint(0, 4)
        edges = gen_random_connected(n, rnd, extra)
        S = rnd.randint(1, n)
        T = rnd.randint(1, n)
        while T == S:
            T = rnd.randint(1, n)
        check("rand%d" % it, n, edges, S, T)
    print("ALL OK" if ok else "FAILURES PRESENT")


# ---------------------------------------------------------------- main
def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_tests()
        return
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0]); M = int(data[1]); S = int(data[2]); T = int(data[3])
    us = list(map(int, data[4:4 + 2 * M:2]))
    vs = list(map(int, data[5:4 + 2 * M:2]))
    sys.stdout.write(str(solve(N, M, us, vs, S, T)) + "\n")


main()