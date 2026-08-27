import sys
import threading

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    edges = []
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        w = int(next(it))
        edges.append((w, u, v))
    A = [int(next(it)) - 1 for _ in range(K)]
    B = [int(next(it)) - 1 for _ in range(K)]

    # 1. Build MST using Kruskal
    edges.sort()
    parent = list(range(N))
    rank = [0] * N
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        a = find(a); b = find(b)
        if a == b: return False
        if rank[a] < rank[b]:
            a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]:
            rank[a] += 1
        return True

    mst_edges = []
    for w, u, v in edges:
        if union(u, v):
            mst_edges.append((w, u, v))
            if len(mst_edges) == N - 1:
                break

    # 2. Count A and B at each node
    cntA = [0] * N
    cntB = [0] * N
    for a in A:
        cntA[a] += 1
    for b in B:
        cntB[b] += 1

    # 3. Initial matches at nodes (cost 0)
    ans = 0
    for i in range(N):
        m = min(cntA[i], cntB[i])
        cntA[i] -= m
        cntB[i] -= m
        # ans += 0

    # 4. DSU sweep on MST edges sorted by weight
    dsu_parent = list(range(N))
    dsu_rank = [0] * N
    comp_cntA = cntA[:]
    comp_cntB = cntB[:]

    def find2(x):
        while dsu_parent[x] != x:
            dsu_parent[x] = dsu_parent[dsu_parent[x]]
            x = dsu_parent[x]
        return x

    mst_edges.sort()  # sort by weight ascending

    for w, u, v in mst_edges:
        ru = find2(u)
        rv = find2(v)
        if ru == rv:
            continue
        # counts in each component
        aA = comp_cntA[ru]
        aB = comp_cntB[ru]
        bA = comp_cntA[rv]
        bB = comp_cntB[rv]
        # cross matches
        cross = min(aA, bB) + min(bA, aB)
        ans += cross * w
        # merge (union by rank)
        if dsu_rank[ru] < dsu_rank[rv]:
            ru, rv = rv, ru
            # swap counts accordingly
            aA, aB, bA, bB = bA, bB, aA, aB
        dsu_parent[rv] = ru
        if dsu_rank[ru] == dsu_rank[rv]:
            dsu_rank[ru] += 1
        # update merged component counts
        comp_cntA[ru] = aA + bA - cross
        comp_cntB[ru] = aB + bB - cross
        # rv counts are no longer used as root

    print(ans)

def main():
    solve()

threading.Thread(target=main).start()