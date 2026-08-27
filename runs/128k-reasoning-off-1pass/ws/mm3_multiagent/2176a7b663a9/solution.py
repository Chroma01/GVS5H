import sys
import threading
import bisect

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    input = sys.stdin.readline
    
    N = int(input())
    W = list(map(int, input().split()))
    intervals = []
    for _ in range(N):
        L, R = map(int, input().split())
        intervals.append((L, R))
    
    # Sort by L ascending (ties by R)
    order = sorted(range(N), key=lambda i: (intervals[i][0], intervals[i][1]))
    L_sorted = [intervals[order[k]][0] for k in range(N)]
    R_of = [intervals[i][1] for i in range(N)]
    
    # Build forest: connect each vertex to the next vertex in L-order with L_j > R_i
    adj = [[] for _ in range(N)]
    for idx, vertex in enumerate(order):
        pos = bisect.bisect_right(L_sorted, R_of[vertex], idx + 1, N)
        if pos < N:
            j = order[pos]
            adj[vertex].append(j)
            adj[j].append(vertex)
    
    # Preprocess forest for LCA
    LOG = (N).bit_length()
    parent = [[-1] * N for _ in range(LOG)]
    depth = [-1] * N
    prefix_sum = [0] * N
    
    # Iterative DFS for each tree
    for start in range(N):
        if depth[start] != -1:
            continue
        depth[start] = 0
        parent[0][start] = -1
        prefix_sum[start] = W[start]
        stack = [(start, -1)]
        while stack:
            v, p = stack.pop()
            for u in adj[v]:
                if u != p and depth[u] == -1:
                    depth[u] = depth[v] + 1
                    parent[0][u] = v
                    prefix_sum[u] = prefix_sum[v] + W[u]
                    stack.append((u, v))
    
    # Build binary lifting table
    for k in range(1, LOG):
        for v in range(N):
            if parent[k-1][v] != -1:
                parent[k][v] = parent[k-1][parent[k-1][v]]
            else:
                parent[k][v] = -1
    
    # LCA function
    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = parent[bit][u]
            diff >>= 1
            bit += 1
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if parent[k][u] != parent[k][v]:
                u = parent[k][u]
                v = parent[k][v]
        return parent[0][u]
    
    # Function to find root (to check if vertices are in the same tree)
    def find_root(v):
        root = v
        while parent[0][root] != -1:
            root = parent[0][root]
        return root
    
    # Answer queries
    Q = int(input())
    out = []
    for _ in range(Q):
        s, t = map(int, input().split())
        s -= 1
        t -= 1
        if depth[s] == -1 or depth[t] == -1:
            out.append("-1")
            continue
        if find_root(s) != find_root(t):
            out.append("-1")
            continue
        l = lca(s, t)
        ans = prefix_sum[s] + prefix_sum[t] - 2 * prefix_sum[l] + W[l]
        out.append(str(ans))
    
    sys.stdout.write("\n".join(out))

threading.Thread(target=solve).start()