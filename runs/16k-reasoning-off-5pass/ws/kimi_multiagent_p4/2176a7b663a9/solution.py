import sys
import bisect

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(data[pos]); pos += 1
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    for i in range(1, N + 1):
        L[i] = int(data[pos]); R[i] = int(data[pos + 1]); pos += 2
    Q = int(data[pos]); pos += 1
    queries = []
    for _ in range(Q):
        s = int(data[pos]); t = int(data[pos + 1]); pos += 2
        queries.append((s, t))

    INF = 1 << 62

    # ---------- Component labeling ----------
    # Vertex i is isolated iff it intersects every other interval:
    #   max_{j != i} L_j <= R_i  AND  min_{j != i} R_j >= L_i
    # All non-isolated vertices form a single connected component.
    maxL1, maxL1i = -1, -1
    maxL2 = -1
    for i in range(1, N + 1):
        if L[i] > maxL1:
            maxL2 = maxL1
            maxL1 = L[i]; maxL1i = i
        elif L[i] > maxL2:
            maxL2 = L[i]
    minR1, minR1i = 1 << 60, -1
    minR2 = 1 << 60
    for i in range(1, N + 1):
        if R[i] < minR1:
            minR2 = minR1
            minR1 = R[i]; minR1i = i
        elif R[i] < minR2:
            minR2 = R[i]

    comp = [0] * (N + 1)
    nxt_comp = 1
    for i in range(1, N + 1):
        ml = maxL2 if maxL1i == i else maxL1
        mr = minR2 if minR1i == i else minR1
        if ml <= R[i] and mr >= L[i]:
            comp[i] = nxt_comp
            nxt_comp += 1
        else:
            comp[i] = 0

    # ---------- Precompute prefix/suffix minima ----------
    # bestL[x] = min W_i over i with R_i < x
    # bestR[x] = min W_i over i with L_i > x
    M = 2 * N + 2
    minW_at_R = [INF] * (M + 1)
    for i in range(1, N + 1):
        if W[i] < minW_at_R[R[i]]:
            minW_at_R[R[i]] = W[i]
    bestL = [INF] * (M + 1)
    run = INF
    for x in range(1, M + 1):
        if minW_at_R[x - 1] < run:
            run = minW_at_R[x - 1]
        bestL[x] = run

    minW_at_L = [INF] * (M + 1)
    for i in range(1, N + 1):
        if W[i] < minW_at_L[L[i]]:
            minW_at_L[L[i]] = W[i]
    bestR = [INF] * (M + 1)
    run = INF
    for x in range(M - 1, 0, -1):
        if minW_at_L[x + 1] < run:
            run = minW_at_L[x + 1]
        bestR[x] = run

    # Sorted orders for binary search
    orderR = sorted(range(1, N + 1), key=lambda i: R[i])
    orderL = sorted(range(1, N + 1), key=lambda i: L[i])
    Rsorted = [R[orderR[k]] for k in range(N)]
    Lsorted = [L[orderL[k]] for k in range(N)]

    # Prefix minima over sorted-by-R
    prefR = [INF] * (N + 1)
    prefR_arg = [-1] * (N + 1)
    for k in range(1, N + 1):
        if W[orderR[k - 1]] <= prefR[k - 1]:
            prefR[k] = W[orderR[k - 1]]
            prefR_arg[k] = orderR[k - 1]
        else:
            prefR[k] = prefR[k - 1]
            prefR_arg[k] = prefR_arg[k - 1]

    # Suffix minima over sorted-by-L
    suffL = [INF] * (N + 2)
    suffL_arg = [-1] * (N + 2)
    for k in range(N, 0, -1):
        if W[orderL[k - 1]] <= suffL[k + 1]:
            suffL[k] = W[orderL[k - 1]]
            suffL_arg[k] = orderL[k - 1]
        else:
            suffL[k] = suffL[k + 1]
            suffL_arg[k] = suffL_arg[k + 1]

    def minW_Rlt(x):
        # min W_i over i with R_i < x
        k = bisect.bisect_left(Rsorted, x)
        return prefR[k]

    def minW_Lgt(x):
        # min W_i over i with L_i > x
        k = bisect.bisect_right(Lsorted, x)
        return suffL[k + 1]

    def argminW_Rlt(x):
        k = bisect.bisect_left(Rsorted, x)
        return prefR_arg[k] if k > 0 else -1

    def argminW_Lgt(x):
        k = bisect.bisect_right(Lsorted, x)
        return suffL_arg[k + 1] if k + 1 <= N else -1

    def cheapest_neighbor(v):
        return min(minW_Rlt(L[v]), minW_Lgt(R[v]))

    # ---------- Build candidate edges for 3-hop/4-hop ----------
    # For each vertex v, find cheapest neighbor on each side
    le = [INF] * (N + 1)   # cheapest edge from v to someone with L > R_v
    re = [INF] * (N + 1)   # cheapest edge from v to someone with R < L_v
    leo = [-1] * (N + 1)
    reo = [-1] * (N + 1)
    for v in range(1, N + 1):
        b = argminW_Lgt(R[v])
        if b != -1:
            le[v] = W[v] + W[b]; leo[v] = b
        a = argminW_Rlt(L[v])
        if a != -1:
            re[v] = W[v] + W[a]; reo[v] = a

    # Collect all candidate edges, sort by weight, keep top K
    cand = []
    for v in range(1, N + 1):
        if le[v] < INF:
            cand.append((le[v], v, leo[v]))
        if re[v] < INF:
            cand.append((re[v], reo[v], v))
    cand.sort()
    K = 16
    top_edges = []
    seen = set()
    for w, a, b in cand:
        key = (a, b) if a < b else (b, a)
        if key in seen:
            continue
        seen.add(key)
        top_edges.append((w, a, b))
        if len(top_edges) >= K:
            break

    def disjoint(a, b):
        return R[a] < L[b] or R[b] < L[a]

    # ---------- Answer queries ----------
    out = []
    for s, t in queries:
        if comp[s] != comp[t]:
            out.append(-1)
            continue
        ans = INF
        base = W[s] + W[t]

        # Direct edge
        if disjoint(s, t):
            ans = base

        # 2-hop: s - k - t, k disjoint from both
        # k must have R_k < min(L_s, L_t) or L_k > max(R_s, R_t)
        c2 = min(minW_Rlt(min(L[s], L[t])), minW_Lgt(max(R[s], R[t])))
        if c2 < INF:
            ans = min(ans, base + c2)

        # 3-hop: s - a - b - t, a disjoint from s, b disjoint from t, a disjoint from b
        best3 = INF
        for w, a, b in top_edges:
            if (disjoint(a, s) and disjoint(b, t)) or (disjoint(b, s) and disjoint(a, t)):
                if w < best3:
                    best3 = w
        if best3 < INF:
            ans = min(ans, base + best3)

        # 4-hop: s - a - b - c - t
        # We try: a from top_edges, b from top_edges, c = cheapest common neighbor of b and t
        best4 = INF
        for w, a, b in top_edges:
            # Case: s - a - b - c - t, where c is common neighbor of b and t
            if disjoint(a, s):
                cb = min(minW_Rlt(min(L[b], L[t])), minW_Lgt(max(R[b], R[t])))
                if cb < INF:
                    best4 = min(best4, W[a] + W[b] + cb)
            # Case: s - b - a - c - t (swap roles)
            if disjoint(b, s):
                ca = min(minW_Rlt(min(L[a], L[t])), minW_Lgt(max(R[a], R[t])))
                if ca < INF:
                    best4 = min(best4, W[a] + W[b] + ca)
        if best4 < INF:
            ans = min(ans, base + best4)

        out.append(ans if ans < INF else -1)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()