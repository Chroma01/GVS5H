import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1

    edges = []
    for _ in range(M):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2])
        idx += 3
        edges.append((w, u - 1, v - 1))

    cntA = [0] * N
    cntB = [0] * N
    for _ in range(K):
        a = int(data[idx]); idx += 1
        cntA[a - 1] += 1
    for _ in range(K):
        b = int(data[idx]); idx += 1
        cntB[b - 1] += 1

    parent = list(range(N))
    size = [1] * N

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    edges.sort()
    ans = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        # merge rv into ru
        totalA = cntA[ru] + cntA[rv]
        totalB = cntB[ru] + cntB[rv]
        matched = totalA if totalA < totalB else totalB
        if matched:
            ans += matched * w
            if totalA >= totalB:
                totalA -= totalB
                totalB = 0
            else:
                totalB -= totalA
                totalA = 0
        parent[rv] = ru
        size[ru] += size[rv]
        cntA[ru] = totalA
        cntB[ru] = totalB

    sys.stdout.write(str(ans) + "\n")

solve()