import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N, M, K = data[p], data[p+1], data[p+2]
    p += 3
    edges = []
    for _ in range(M):
        u, v, w = data[p], data[p+1], data[p+2]
        p += 3
        edges.append((w, u-1, v-1))
    A = [x-1 for x in data[p:p+K]]
    p += K
    B = [x-1 for x in data[p:p+K]]

    # Kruskal reconstruction tree (DSU tree)
    # nodes 0..N-1 are leaves (original vertices), N..2N-2 are internal nodes
    parent = list(range(2*N))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    children = [[] for _ in range(2*N)]
    weight = [0]*(2*N)
    node_cnt = N
    edges.sort()
    for w, u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        children[node_cnt].append(ru)
        children[node_cnt].append(rv)
        weight[node_cnt] = w
        parent[ru] = node_cnt
        parent[rv] = node_cnt
        parent[node_cnt] = node_cnt
        node_cnt += 1
        if node_cnt == 2*N - 1:
            break

    root = node_cnt - 1

    # multiset counts of A and B at leaves
    a_cnt = [0]*(2*N)
    b_cnt = [0]*(2*N)
    for x in A:
        a_cnt[x] += 1
    for x in B:
        b_cnt[x] += 1

    # iterative post-order traversal from root
    ans = 0
    order = []
    stack = [root]
    while stack:
        v = stack.pop()
        order.append(v)
        for c in children[v]:
            stack.append(c)
    # process children before parents
    for v in reversed(order):
        if v < N:
            continue  # leaf: counts already set
        ta = 0
        tb = 0
        for c in children[v]:
            ta += a_cnt[c]
            tb += b_cnt[c]
        m = ta if ta < tb else tb
        ans += m * weight[v]
        a_cnt[v] = ta - m
        b_cnt[v] = tb - m

    sys.stdout.write(str(ans) + "\n")

main()