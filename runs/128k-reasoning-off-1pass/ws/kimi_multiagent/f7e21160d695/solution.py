import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1

    edges = []
    for _ in range(M):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2])
        idx += 3
        edges.append((w, u, v))

    A = [int(x) for x in data[idx:idx+K]]
    idx += K
    B = [int(x) for x in data[idx:idx+K]]
    idx += K

    # Kruskal reconstruction tree
    # Nodes 1..N are leaves (original vertices); internal nodes N+1..2N-1.
    size = 2 * N  # index up to 2N-1
    parent = list(range(size))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    child1 = [0] * size
    child2 = [0] * size
    weight = [0] * size

    edges.sort()
    cur = N
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru != rv:
            cur += 1
            child1[cur] = ru
            child2[cur] = rv
            weight[cur] = w
            parent[ru] = cur
            parent[rv] = cur
            parent[cur] = cur

    # Leaf counts
    sA = [0] * size
    sB = [0] * size
    for a in A:
        sA[a] += 1
    for b in B:
        sB[b] += 1

    # Process internal nodes in creation order (children have smaller ids,
    # weights nondecreasing upward).
    ans = 0
    for v in range(N + 1, cur + 1):
        c1 = child1[v]
        c2 = child2[v]
        a1 = sA[c1]; b1 = sB[c1]
        a2 = sA[c2]; b2 = sB[c2]
        m = (a1 if a1 < b2 else b2) + (a2 if a2 < b1 else b1)
        if m:
            ans += m * weight[v]
        sA[v] = a1 + a2 - m
        sB[v] = b1 + b2 - m

    sys.stdout.write(str(ans) + "\n")

main()