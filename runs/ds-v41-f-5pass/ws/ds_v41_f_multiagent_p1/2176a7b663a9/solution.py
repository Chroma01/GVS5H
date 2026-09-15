import sys
from bisect import bisect_left, bisect_right

INF = 1 << 60


def solve_all(N, W, L, R, queries):
    # fR(x) = min W_i with R_i < x : sort by R ascending, prefix minima
    orderR = sorted(range(N), key=lambda i: R[i])
    sR = [R[i] for i in orderR]
    prefW = [0] * N
    cur = INF
    for k in range(N):
        w = W[orderR[k]]
        if w < cur:
            cur = w
        prefW[k] = cur

    # fL(x) = min W_i with L_i > x : sort by L ascending, suffix minima
    orderL = sorted(range(N), key=lambda i: L[i])
    sL = [L[i] for i in orderL]
    suffW = [INF] * (N + 1)
    cur = INF
    for k in range(N - 1, -1, -1):
        w = W[orderL[k]]
        if w < cur:
            cur = w
        suffW[k] = cur

    # non-isolated detection via two smallest R and two largest L
    r1 = orderR[0]; r2 = orderR[1]
    l1 = orderL[-1]; l2 = orderL[-2]
    Rr1 = R[r1]; Rr2 = R[r2]; Ll1 = L[l1]; Ll2 = L[l2]
    noniso = [False] * N
    for v in range(N):
        oR = Rr2 if v == r1 else Rr1
        oL = Ll2 if v == l1 else Ll1
        noniso[v] = (oR < L[v]) or (R[v] < oL)

    out = []
    for (s, t) in queries:
        if (not noniso[s]) or (not noniso[t]):
            out.append(-1)
            continue
        Rs = R[s]; Rt = R[t]; Ls = L[s]; Lt = L[t]
        # direct edge: intervals disjoint
        if Rs < Lt or Rt < Ls:
            out.append(W[s] + W[t])
            continue
        # common neighbour: disjoint from both (s,t overlap here)
        minL = Ls if Ls < Lt else Lt
        maxR = Rs if Rs > Rt else Rt
        c = bisect_left(sR, minL)              # R_w < minL
        common = prefW[c - 1] if c > 0 else INF
        c = bisect_right(sL, maxR)             # L_w > maxR
        if c < N and suffW[c] < common:
            common = suffW[c]
        # X: a right of s, b left of t ; Y: a left of s, b right of t
        c = bisect_right(sL, Rs); flRs = suffW[c] if c < N else INF
        c = bisect_left(sR, Lt);  frLt = prefW[c - 1] if c > 0 else INF
        c = bisect_left(sR, Ls);  frLs = prefW[c - 1] if c > 0 else INF
        c = bisect_right(sL, Rt); flRt = suffW[c] if c < N else INF
        X = flRs + frLt
        Y = frLs + flRt
        best = common
        if X < best:
            best = X
        if Y < best:
            best = Y
        if best >= INF:
            out.append(-1)
        else:
            out.append(W[s] + W[t] + best)
    return out


def run_solution(tokens):
    pos = 0
    N = int(tokens[pos]); pos += 1
    W = [int(tokens[pos + i]) for i in range(N)]; pos += N
    L = [0] * N; R = [0] * N
    for i in range(N):
        L[i] = int(tokens[pos]); R[i] = int(tokens[pos + 1]); pos += 2
    Q = int(tokens[pos]); pos += 1
    queries = []
    for _ in range(Q):
        s = int(tokens[pos]) - 1; t = int(tokens[pos + 1]) - 1; pos += 2
        queries.append((s, t))
    out = solve_all(N, W, L, R, queries)
    sys.stdout.write("\n".join(str(x) for x in out) + "\n")


# ---------------------------------------------------------------------------
# Brute-force validator (runs only when stdin is empty)
# ---------------------------------------------------------------------------
import random
import heapq


def brute_all_pairs(N, W, L, R):
    adjl = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            if R[i] < L[j] or R[j] < L[i]:
                adjl[i].append(j)
                adjl[j].append(i)
    ans = {}
    for s in range(N):
        dist = [INF] * N
        dist[s] = W[s]
        pq = [(W[s], s)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v in adjl[u]:
                nd = d + W[v]
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        for t in range(N):
            if t != s:
                ans[(s, t)] = dist[t] if dist[t] < INF else -1
    return ans


def random_case(N):
    mode = random.randint(0, 2)
    hi = [2 * N, max(2, N), 6][mode]
    L = [0] * N; R = [0] * N
    for i in range(N):
        a = random.randint(1, hi)
        b = random.randint(1, hi)
        L[i] = min(a, b); R[i] = max(a, b)
    wm = random.randint(0, 3)
    if wm == 0:
        W = [random.randint(1, 3) for _ in range(N)]
    elif wm == 1:
        W = [random.randint(1, 10) for _ in range(N)]
    elif wm == 2:
        W = [random.randint(1, 1000000) for _ in range(N)]
    else:
        # few very heavy vertices, many light ones
        W = [1] * N
        for _ in range(random.randint(1, max(1, N // 2))):
            W[random.randrange(N)] = random.randint(500000, 1000000)
    return W, L, R


def run_validator():
    random.seed(987654321)
    trials = 60000
    for it in range(trials):
        N = random.randint(2, 8)
        W, L, R = random_case(N)
        queries = [(s, t) for s in range(N) for t in range(N) if s != t]
        exp = brute_all_pairs(N, W, L, R)
        got = solve_all(N, W, L, R, queries)
        for (s, t), g in zip(queries, got):
            e = exp[(s, t)]
            if e != g:
                print("COUNTEREXAMPLE at trial", it)
                print("N =", N)
                print("W =", W)
                print("L =", L)
                print("R =", R)
                print("s,t =", s, t, "(0-indexed)")
                print("true =", e, "computed =", g)
                return
    print("OK: no counterexamples in", trials, "trials")


def main():
    tokens = sys.stdin.buffer.read().split()
    if tokens:
        run_solution(tokens)
    else:
        run_validator()


main()