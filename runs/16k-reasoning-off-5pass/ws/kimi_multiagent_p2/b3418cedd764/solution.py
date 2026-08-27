import sys
from sys import setrecursionlimit

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it))

    # children lists (reversed edges)
    children = [[] for _ in range(N + 1)]
    indeg = [0] * (N + 1)  # number of children (in-degree in original graph)
    for i in range(1, N + 1):
        p = A[i]
        children[p].append(i)
        indeg[p] += 1

    # Kahn elimination: repeatedly remove nodes with in-degree 0 (original graph)
    # removed nodes are non-cycle; record order (leaves first)
    from collections import deque
    dq = deque()
    removed = [False] * (N + 1)
    for i in range(1, N + 1):
        if indeg[i] == 0:
            dq.append(i)
    order = []
    while dq:
        u = dq.popleft()
        removed[u] = True
        order.append(u)
        p = A[u]
        indeg[p] -= 1
        if indeg[p] == 0:
            dq.append(p)

    # f[u][v] for v = 0..M (index by value; use 1..M), computed for removed nodes
    # f_u(v) = product over children c of (sum_{w <= v} f_c(w))
    # Store as list of length M+1 per node.
    f = [None] * (N + 1)
    for u in order:
        fu = [0] * (M + 1)
        # initialize with 1s
        for v in range(1, M + 1):
            fu[v] = 1
        for c in children[u]:
            fc = f[c]
            # prefix sums of fc
            s = 0
            # multiply into fu on the fly
            for v in range(1, M + 1):
                s += fc[v]
                if s >= MOD:
                    s -= MOD
                fu[v] = (fu[v] * s) % MOD
        f[u] = fu

    # remaining nodes (removed == False) form the cycles; group them into components
    ans = 1
    seen = [False] * (N + 1)
    for i in range(1, N + 1):
        if removed[i] or seen[i]:
            continue
        # walk the cycle starting at i
        cyc = []
        j = i
        while not seen[j]:
            seen[j] = True
            cyc.append(j)
            j = A[j]
        # component count: sum over v of product over r in cyc of g_r(v)
        # where g_r(v) = product over non-cycle children c of r of (prefix sum of f_c at v)
        # For cycle node r, its children that are cycle nodes are excluded (they share value v).
        total = 0
        # precompute per cycle node the product over tree children prefix sums
        # g_r[v] for v in 1..M
        gs = []
        for r in cyc:
            gr = [1] * (M + 1)
            gr[0] = 0
            for c in children[r]:
                if removed[c]:
                    fc = f[c]
                    s = 0
                    for v in range(1, M + 1):
                        s += fc[v]
                        if s >= MOD:
                            s -= MOD
                        gr[v] = (gr[v] * s) % MOD
            gs.append(gr)
        for v in range(1, M + 1):
            prod = 1
            for gr in gs:
                prod = (prod * gr[v]) % MOD
            total += prod
            if total >= MOD:
                total -= MOD
        ans = (ans * total) % MOD

    print(ans % MOD)

main()