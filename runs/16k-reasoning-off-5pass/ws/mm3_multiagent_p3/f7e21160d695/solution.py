import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    input = sys.stdin.readline

    N, M, K = map(int, input().split())
    edges = []
    for _ in range(M):
        u, v, w = map(int, input().split())
        edges.append((w, u, v))

    # ---------- Build MST with Kruskal ----------
    edges.sort()                     # by weight
    parent = list(range(N + 1))
    size = [1] * (N + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        x = find(x)
        y = find(y)
        if x == y:
            return False
        if size[x] < size[y]:
            x, y = y, x
        parent[y] = x
        size[x] += size[y]
        return True

    mst_edges = []                   # (u, v, w)
    for w, u, v in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            if len(mst_edges) == N - 1:
                break

    # ---------- Count A and B occurrences ----------
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)

    A_list = list(map(int, input().split()))
    B_list = list(map(int, input().split()))
    for a in A_list:
        cntA[a] += 1
    for b in B_list:
        cntB[b] += 1

    # ---------- DSU for greedy matching on the MST ----------
    parent = list(range(N + 1))
    size = [1] * (N + 1)
    a = cntA[:]          # number of unmatched A in the component
    b = cntB[:]          # number of unmatched B in the component

    def find2(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    ans = 0
    # Process MST edges in increasing weight order
    mst_edges.sort(key=lambda x: x[2])

    for u, v, w in mst_edges:
        ru = find2(u)
        rv = find2(v)
        if ru == rv:
            continue
        # match A from ru with B from rv
        t1 = min(a[ru], b[rv])
        # match A from rv with B from ru
        t2 = min(a[rv], b[ru])
        matched = t1 + t2
        if matched:
            ans += matched * w
            a[ru] = a[ru] + a[rv] - matched
            b[ru] = b[ru] + b[rv] - matched
        else:
            a[ru] = a[ru] + a[rv]
            b[ru] = b[ru] + b[rv]
        # union by size
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]

    print(ans)

if __name__ == "__main__":
    solve()