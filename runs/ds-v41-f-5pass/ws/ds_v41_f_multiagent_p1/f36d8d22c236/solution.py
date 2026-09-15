import sys

def solve():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]

    # 1) Build the required mapping f from each distinct char of S.
    f = {}
    for a, b in zip(S, T):
        if a in f:
            if f[a] != b:
                print(-1)
                return
        else:
            f[a] = b

    # 2) Edges c -> f(c) for c with f(c) != c.  E = number of such edges.
    edges = {}
    E = 0
    for c, d in f.items():
        if c != d:
            edges[c] = d
            E += 1

    # indegree over these edges
    indeg = {}
    for c, d in edges.items():
        indeg[d] = indeg.get(d, 0) + 1

    # 3) Find cycles; a cycle is "pure" iff every node on it has indegree exactly 1.
    color = {}
    P = 0
    for s in edges:
        if color.get(s, 0) != 0:
            continue
        path = []
        node = s
        while node is not None and color.get(node, 0) == 0:
            color[node] = 1
            path.append(node)
            node = edges.get(node)
        if node is not None and color.get(node, 0) == 1:
            idx = path.index(node)
            cyc = path[idx:]
            if all(indeg.get(v, 0) == 1 for v in cyc):
                P += 1
        for v in path:
            color[v] = 2

    # 4) Impossibility: T uses all 26 letters (=> S too, f bijection) and a cycle exists.
    if len(set(T)) == 26 and P > 0:
        print(-1)
    else:
        print(E + P)

solve()