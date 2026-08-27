import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1

    edges = []
    for i in range(M):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2])
        idx += 3
        edges.append((w, u - 1, v - 1))

    cntA = [0] * N
    cntB = [0] * N
    for i in range(K):
        a = int(data[idx]); idx += 1
        cntA[a - 1] += 1
    for i in range(K):
        b = int(data[idx]); idx += 1
        cntB[b - 1] += 1

    # Kruskal reconstruction tree
    parent = list(range(N))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    child1 = []
    child2 = []
    weight = []

    edges.sort()
    next_node = N
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        child1.append(ru)
        child2.append(rv)
        weight.append(w)
        parent.append(next_node)
        parent[ru] = next_node
        parent[rv] = next_node
        next_node += 1
        if next_node == 2 * N - 1:
            break

    total_nodes = next_node

    balance = [0] * total_nodes
    for v in range(N):
        balance[v] = cntA[v] - cntB[v]

    ans = 0
    # children always have smaller ids than their parent, so increasing id order
    # is a valid post-order
    for node in range(N, total_nodes):
        i = node - N
        b1 = balance[child1[i]]
        b2 = balance[child2[i]]
        a = (b1 if b1 > 0 else 0) + (b2 if b2 > 0 else 0)
        b = (-b1 if b1 < 0 else 0) + (-b2 if b2 < 0 else 0)
        m = a if a < b else b
        if m:
            ans += m * weight[i]
        balance[node] = a - b

    sys.stdout.write(str(ans) + "\n")

solve()