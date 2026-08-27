import sys

INF = 10**30


def build_pre(N, W, L, R, INF=INF):
    C = 2 * N + 5

    minL = [INF] * (C + 1)
    minR = [INF] * (C + 1)

    for i in range(N):
        w = W[i]
        li = L[i]
        ri = R[i]
        if w < minL[li]:
            minL[li] = w
        if w < minR[ri]:
            minR[ri] = w

    # suffL[x] = minimum weight among intervals with L >= x
    suffL = [INF] * (C + 2)
    cur = INF
    for c in range(C, 0, -1):
        v = minL[c]
        if v < cur:
            cur = v
        suffL[c] = cur

    # prefR[x] = minimum weight among intervals with R <= x
    prefR = [INF] * (C + 2)
    cur = INF
    for c in range(1, C + 1):
        v = minR[c]
        if v < cur:
            cur = v
        prefR[c] = cur

    return prefR, suffL


def answer_one(s, t, W, L, R, prefR, suffL, INF=INF):
    ws = W[s]
    wt = W[t]
    base = ws + wt

    ls = L[s]
    lt = L[t]
    rs = R[s]
    rt = R[t]

    # Direct edge: intervals are disjoint.
    if rs < lt or rt < ls:
        return base

    ans = INF

    # Two-edge path: one intermediate disjoint from both endpoints.
    # Since the endpoints overlap, such an interval must be left of both
    # or right of both.
    lb = ls if ls < lt else lt
    rb = rs if rs > rt else rt

    m = prefR[lb - 1]          # R < min(L_s, L_t)
    v = suffL[rb + 1]          # L > max(R_s, R_t)
    if v < m:
        m = v
    if m < INF:
        ans = base + m

    # Three-edge path.
    # Let u be the endpoint with smaller left endpoint, v the other.
    # A non-dominated 3-edge path has first intermediate x with L_x > R_u
    # and second intermediate y with R_y < L_v. Then x-y is automatic.
    if ls <= lt:
        ru = rs
        lv = lt
    else:
        ru = rt
        lv = ls

    m1 = suffL[ru + 1]         # L > R_u
    if m1 < INF:
        m2 = prefR[lv - 1]     # R < L_v
        if m2 < INF:
            val = base + m1 + m2
            if val < ans:
                ans = val

    return ans if ans < INF else -1


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))

    W = [0] * N
    for i in range(N):
        W[i] = int(next(it))

    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = int(next(it))
        R[i] = int(next(it))

    prefR, suffL = build_pre(N, W, L, R)

    Q = int(next(it))
    out = []
    for _ in range(Q):
        s = int(next(it)) - 1
        t = int(next(it)) - 1
        out.append(str(answer_one(s, t, W, L, R, prefR, suffL)))

    sys.stdout.write("\n".join(out))


def brute_force(N, W, L, R, queries, INF=INF):
    adj = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            if R[i] < L[j] or R[j] < L[i]:
                adj[i].append(j)
                adj[j].append(i)

    res = []
    for s, t in queries:
        dist = [INF] * N
        used = [False] * N
        dist[s] = W[s]

        for _ in range(N):
            u = -1
            best = INF
            for i in range(N):
                if not used[i] and dist[i] < best:
                    best = dist[i]
                    u = i

            if u == -1:
                break
            if u == t:
                break

            used[u] = True
            du = dist[u]
            for v in adj[u]:
                nd = du + W[v]
                if nd < dist[v]:
                    dist[v] = nd

        res.append(dist[t] if dist[t] < INF else -1)

    return res


def answer_all(N, W, L, R, queries):
    prefR, suffL = build_pre(N, W, L, R)
    return [answer_one(s, t, W, L, R, prefR, suffL) for s, t in queries]


def selftest():
    import random

    random.seed(1234567)

    for _ in range(2000):
        N = random.randint(2, 7)
        maxc = 2 * N

        W = [random.randint(1, 10) for _ in range(N)]
        L = []
        R = []
        for _ in range(N):
            l = random.randint(1, maxc)
            r = random.randint(l, maxc)
            L.append(l)
            R.append(r)

        queries = [(i, j) for i in range(N) for j in range(N) if i != j]

        expected = brute_force(N, W, L, R, queries)
        got = answer_all(N, W, L, R, queries)

        if expected != got:
            print("MISMATCH")
            print("N", N)
            print("W", W)
            print("L", L)
            print("R", R)
            print("queries", queries)
            print("expected", expected)
            print("got", got)
            return

    print("selftest ok")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    else:
        solve()