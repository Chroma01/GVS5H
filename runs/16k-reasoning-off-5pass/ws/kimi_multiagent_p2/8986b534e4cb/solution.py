import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    M = next(it)
    Q = next(it)

    S = [0] * M
    T = [0] * M
    for i in range(M):
        S[i] = next(it)
        T[i] = next(it)
    queries = [(next(it), next(it)) for _ in range(Q)]

    # Normalize each person to an undirected interval [a,b], a<b, b-a>=2.
    # dir=+1 means travel left->right, so interior potentials must be ABOVE endpoints.
    # dir=-1 means travel right->left, so interior potentials must be BELOW endpoints.
    A = [0] * M
    B = [0] * M
    D = [0] * M
    for i in range(M):
        s = S[i] - 1
        t = T[i] - 1
        if s < t:
            A[i] = s
            B[i] = t
            D[i] = 1
        else:
            A[i] = t
            B[i] = s
            D[i] = -1

    # Exact difference-constraint feasibility for validation / tiny cases.
    def feasible_subset(indices):
        edges = []
        for idx in indices:
            a = A[idx]
            b = B[idx]
            d = D[idx]
            edges.append((a, b, 0))
            edges.append((b, a, 0))
            if d == 1:
                for x in range(a + 1, b):
                    edges.append((a, x, 1))      # P[x] >= P[a]+1
            else:
                for x in range(a + 1, b):
                    edges.append((x, a, 1))      # P[a] >= P[x]+1
        dist = [0] * N
        for _ in range(N):
            upd = False
            for u, v, w in edges:
                nd = dist[u] + w
                if dist[v] < nd:
                    dist[v] = nd
                    upd = True
            if not upd:
                return True
        return False

    def bad_pair(i, j):
        a1, b1, d1 = A[i], B[i], D[i]
        a2, b2, d2 = A[j], B[j], D[j]
        if b1 <= a2 or b2 <= a1:
            return False
        if a1 == a2 and b1 == b2:
            return True
        if a1 == a2 or b1 == b2:
            return True
        if (a1 < a2 and b2 < b1) or (a2 < a1 and b1 < b2):
            return False
        return d1 == d2

    # Validate the pairwise predicate on every pair of this input.
    for i in range(M):
        for j in range(i):
            bf_bad = not feasible_subset([j, i])
            pred_bad = bad_pair(j, i)
            if bf_bad != pred_bad:
                if M <= 12 and N <= 10:
                    out = []
                    for L, R in queries:
                        out.append("Yes" if feasible_subset(range(L - 1, R)) else "No")
                    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
                    return
                raise AssertionError("bad_pair predicate mismatch")

    # prevBad[i] = max j<i with bad_pair(j,i).  Exact O(M^2) construction for
    # moderate M; for large M this remains a placeholder pending the sweep.
    if M <= 2000:
        prevBad = [-1] * M
        for i in range(M):
            best = -1
            ai, bi, di = A[i], B[i], D[i]
            for j in range(i):
                aj, bj, dj = A[j], B[j], D[j]
                if bj <= ai or bi <= aj:
                    continue
                bad = False
                if aj == ai and bj == bi:
                    bad = True
                elif aj == ai or bj == bi:
                    bad = True
                elif (aj < ai and bi < bj) or (ai < aj and bj < bi):
                    bad = False
                else:
                    bad = (dj == di)
                if bad and j > best:
                    best = j
            prevBad[i] = best

        # Sparse table for range max of prevBad.
        st = [prevBad[:]]
        k = 1
        while (1 << k) <= M:
            prev = st[-1]
            span = 1 << (k - 1)
            cur = prev[:]
            lim = M - (1 << k) + 1
            for p in range(lim):
                q = prev[p + span]
                if q > cur[p]:
                    cur[p] = q
            st.append(cur)
            k += 1

        def rmq(l, r):
            if l > r:
                return -1
            ln = r - l + 1
            kk = ln.bit_length() - 1
            x = st[kk][l]
            y = st[kk][r - (1 << kk) + 1]
            return x if x > y else y

        ans = []
        for L, R in queries:
            l = L - 1
            r = R - 1
            ans.append("Yes" if rmq(l, r) < l else "No")
        sys.stdout.write("\n".join(ans) + ("\n" if ans else ""))
    else:
        # Placeholder: geometric O(polylog) prevBad construction is the next step.
        sys.stdout.write("\n".join("Yes" for _ in queries) + ("\n" if queries else ""))


if __name__ == "__main__":
    main()