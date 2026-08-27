import sys
from collections import defaultdict, deque
import bisect


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); M = int(data[p+1]); Q = int(data[p+2]); p += 3
    Lv = [0]*(M+1); Rv = [0]*(M+1); fw = [False]*(M+1)
    for i in range(1, M+1):
        s = int(data[p]); t = int(data[p+1]); p += 2
        a, b = s-1, t-1
        if a < b:
            Lv[i], Rv[i], fw[i] = a, b, True
        else:
            Lv[i], Rv[i], fw[i] = b, a, False
    queries = []
    for k in range(Q):
        l = int(data[p]); r = int(data[p+1]); p += 2
        queries.append((l, r, k))

    # ------------------------------------------------------------------
    # Feasibility criterion (proved):
    #   constraints  P[L_i] = P[R_i]  (equality, weight 0 both ways)
    #   forward  i:  P[k] >= P[L_i] + 1  for all k in (L_i, R_i)
    #   backward i:  P[k] <= P[L_i] - 1  for all k in (L_i, R_i)
    # All strict edges have weight +1, so after contracting equality
    # components the system is feasible  <=>  the component graph is
    # acyclic.  Component-graph edges (u,v components):
    #   (E1) u forward , endpoint of v strictly inside I_u : u -> v
    #   (E2) u forward , v backward, I_u ∩ I_v != empty    : u -> v
    #   (E3) u backward, endpoint of v strictly inside I_u : v -> u
    #   self-loop (component has a position strictly inside the
    #   interval of one of its own persons) => immediate infeasible.
    # ------------------------------------------------------------------

    class DSU:
        __slots__ = ('p', 'r')
        def __init__(self, n):
            self.p = list(range(n)); self.r = [0]*n
        def find(self, x):
            p = self.p
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            return x
        def union(self, a, b):
            a = self.find(a); b = self.find(b)
            if a == b:
                return
            pp, rr = self.p, self.r
            if rr[a] < rr[b]:
                a, b = b, a
            pp[b] = a
            if rr[a] == rr[b]:
                rr[a] += 1

    def feasible(ids):
        ids = list(ids)
        k = len(ids)
        if k <= 1:
            return True
        coords = sorted(set([c for i in ids for c in (Lv[i], Rv[i])]))
        cidx = {c: j for j, c in enumerate(coords)}
        n = len(coords)
        d = DSU(n)
        for i in ids:
            d.union(cidx[Lv[i]], cidx[Rv[i]])

        at = defaultdict(list)
        for i in ids:
            at[cidx[Lv[i]]].append(i)
            at[cidx[Rv[i]]].append(i)
        pos_ep = sorted(at.keys())

        edges = set()

        # E1 / E3: endpoint strictly inside interval
        for u in ids:
            lu = cidx[Lv[u]]; ru = cidx[Rv[u]]
            cu = d.find(lu)
            lo = bisect.bisect_right(pos_ep, lu)
            hi = bisect.bisect_left(pos_ep, ru)
            if fw[u]:
                for t in range(lo, hi):
                    cp = d.find(pos_ep[t])
                    if cp == cu:
                        return False
                    edges.add((cu, cp))
            else:
                for t in range(lo, hi):
                    cp = d.find(pos_ep[t])
                    if cp == cu:
                        return False
                    edges.add((cp, cu))

        # E2: forward u, backward v, open interiors overlap
        fwds = [u for u in ids if fw[u]]
        bwds = [v for v in ids if not fw[v]]
        if fwds and bwds:
            bwds_sorted = sorted(bwds, key=lambda v: Lv[v])
            bL = [Lv[v] for v in bwds_sorted]
            m = len(bwds_sorted)
            size = 1
            while size < m:
                size <<= 1
            NEG = -10**9
            maxR = [NEG]*(2*size)
            for idx, v in enumerate(bwds_sorted):
                maxR[size+idx] = Rv[v]
            for node in range(size-1, 0, -1):
                a = maxR[2*node]; b = maxR[2*node+1]
                maxR[node] = a if a > b else b

            sys.setrecursionlimit(1 << 25)

            def report(node, nl, nr, ql, thr, cu, seen):
                if ql < 0 or nl > ql or maxR[node] <= thr:
                    return False
                if node >= size:
                    idx = node - size
                    if idx < m:
                        v = bwds_sorted[idx]
                        if Rv[v] > thr:
                            cv = d.find(cidx[Lv[v]])
                            if cv == cu:
                                return True
                            if cv not in seen:
                                seen.add(cv)
                                edges.add((cu, cv))
                    return False
                mid = (nl+nr)//2
                if report(2*node, nl, mid, ql, thr, cu, seen):
                    return True
                return report(2*node+1, mid+1, nr, ql, thr, cu, seen)

            for u in fwds:
                ql = bisect.bisect_left(bL, Rv[u]) - 1
                if ql < 0:
                    continue
                cu = d.find(cidx[Lv[u]])
                if report(1, 0, size-1, ql, Lv[u], cu, set()):
                    return False

        if not edges:
            return True

        indeg = {}
        adj = defaultdict(list)
        for (a, b) in edges:
            adj[a].append(b)
            indeg[b] = indeg.get(b, 0) + 1
            if a not in indeg:
                indeg[a] = 0
        dq = deque([x for x in indeg if indeg[x] == 0])
        cnt = 0
        while dq:
            x = dq.popleft()
            cnt += 1
            for y in adj[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    dq.append(y)
        return cnt == len(indeg)

    # ------------------------------------------------------------------
    # Two-pointer schedule per L-block.
    # ------------------------------------------------------------------
    B = max(1, int(M**0.5) + 1)
    ans = [None]*Q

    blocks = defaultdict(list)
    for (l, r, k) in queries:
        blocks[(l-1)//B].append((l, r, k))

    for b, qs in blocks.items():
        bnd = min(M, (b+1)*B)
        small = [(l, r, k) for (l, r, k) in qs if r <= bnd]
        big = [(l, r, k) for (l, r, k) in qs if r > bnd]
        for (l, r, k) in small:
            ans[k] = "Yes" if feasible(range(l, r+1)) else "No"
        big.sort(key=lambda x: x[1])
        for (l, r, k) in big:
            ids = list(range(l, bnd+1)) + list(range(bnd+1, r+1))
            ans[k] = "Yes" if feasible(ids) else "No"

    sys.stdout.write("\n".join(ans) + "\n")


main()