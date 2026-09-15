import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    M = int(data[pos]); pos += 1
    K = int(data[pos]); pos += 1

    edges = []
    for _ in range(M):
        u = int(data[pos]); pos += 1
        v = int(data[pos]); pos += 1
        w = int(data[pos]); pos += 1
        # store 0-indexed
        edges.append((w, u - 1, v - 1))
    edges.sort(key=lambda e: e[0])

    A = data[pos:pos + K]; pos += K
    B = data[pos:pos + K]; pos += K

    # DSU arrays
    parent = list(range(N))
    sA = [0] * N
    sB = [0] * N

    for x in A:
        sA[int(x) - 1] += 1
    for x in B:
        sB[int(x) - 1] += 1

    # iterative find with path compression
    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    total = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        aL = sA[ru]; bL = sB[ru]
        aR = sA[rv]; bR = sB[rv]
        # pairs formed at this merge weight
        p1 = aL if aL < bR else bR
        p2 = aR if aR < bL else bL
        pairs = p1 + p2
        total += w * pairs

        # union: attach rv under ru (union by size optional; sizes simple)
        # choose larger component as new root to keep find shallow
        if (aR + bR) > (aL + bL):
            ru, rv = rv, ru
            aL, bL, aR, bR = aR, bR, aL, bL
        parent[rv] = ru
        sA[ru] = aL + aR - pairs
        sB[ru] = bL + bR - pairs

    print(total)

main()