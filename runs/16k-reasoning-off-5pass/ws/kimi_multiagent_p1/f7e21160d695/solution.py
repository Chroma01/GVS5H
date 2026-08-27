import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1

    edges = []
    for _ in range(M):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        w = int(data[idx]); idx += 1
        edges.append((w, u, v))

    cntA = [0] * N
    cntB = [0] * N
    for _ in range(K):
        a = int(data[idx]) - 1; idx += 1
        cntA[a] += 1
    for _ in range(K):
        b = int(data[idx]) - 1; idx += 1
        cntB[b] += 1

    # Kruskal reconstruction tree (KRT):
    # nodes 0..N-1 are leaves (original vertices);
    # each successful union creates an internal node with weight = edge weight.
    # f(x, y) = weight of LCA(x, y) in this tree.
    total_nodes = 2 * N - 1
    parent_dsu = list(range(N))
    rep = list(range(N))  # rep[dsu_root] = KRT node id representing that component

    def find(x):
        while parent_dsu[x] != x:
            parent_dsu[x] = parent_dsu[parent_dsu[x]]
            x = parent_dsu[x]
        return x

    child1 = [0] * total_nodes
    child2 = [0] * total_nodes
    weight = [0] * total_nodes

    edges.sort()
    nxt = N
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        node = nxt
        nxt += 1
        weight[node] = w
        cu = rep[ru]
        cv = rep[rv]
        child1[node] = cu
        child2[node] = cv
        parent_dsu[rv] = ru
        rep[ru] = node

    root = nxt - 1  # graph is connected and N >= 2, so exactly N-1 internal nodes

    # Bottom-up DP over the KRT.
    # a[node] / b[node] = number of unmatched A's / B's in this subtree
    # after matching as many pairs as possible inside the subtree.
    a = [0] * total_nodes
    b = [0] * total_nodes
    for v in range(N):
        a[v] = cntA[v]
        b[v] = cntB[v]

    # Iterative post-order (children before parents).
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node >= N:
            stack.append(child1[node])
            stack.append(child2[node])

    ans = 0
    for node in reversed(order):
        if node < N:
            continue
        l = child1[node]
        r = child2[node]
        w = weight[node]
        # Pairs forced to cross at this node: A's from one side with B's from the other.
        cross = min(a[l], b[r]) + min(a[r], b[l])
        ans += w * cross
        a[node] = a[l] + a[r] - cross
        b[node] = b[l] + b[r] - cross

    sys.stdout.write(str(ans) + "\n")

main()