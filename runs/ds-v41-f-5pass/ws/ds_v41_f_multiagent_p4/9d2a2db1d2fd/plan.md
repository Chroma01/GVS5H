```python
import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = H * W
    F = [0] * N
    for i in range(N):
        F[i] = int(next(it))
    Q = int(next(it))
    queries = []
    for _ in range(Q):
        A = int(next(it)); B = int(next(it)); Y = int(next(it))
        C = int(next(it)); D = int(next(it)); Z = int(next(it))
        queries.append((A, B, Y, C, D, Z))

    edges = []
    for i in range(H):
        row_start = i * W
        for j in range(W):
            idx = row_start + j
            if j + 1 < W:
                w = F[idx] if F[idx] < F[idx+1] else F[idx+1]
                edges.append((w, idx, idx+1))
            if i + 1 < H:
                w = F[idx] if F[idx] < F[idx+W] else F[idx+W]
                edges.append((w, idx, idx+W))
    edges.sort(key=lambda x: x[0], reverse=True)

    parent = list(range(N))
    rank = [0] * N
    comp_node = list(range(N))
    max_nodes = 2 * N - 1
    left = [-1] * max_nodes
    right = [-1] * max_nodes
    height = [0] * max_nodes
    for i in range(N):
        height[i] = F[i]
    next_node = N

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru != rv:
            node_u = comp_node[ru]
            node_v = comp_node[rv]
            new = next_node
            next_node += 1
            left[new] = node_u
            right[new] = node_v
            height[new] = w
            if rank[ru] < rank[rv]:
                parent[ru] = rv
                comp_node[rv] = new
            else:
                parent[rv] = ru
                comp_node[ru] = new
                if rank[ru] == rank[rv]:
                    rank[ru] += 1

    root = comp_node[find(0)]
    max_nodes = next_node

    LOG = (max_nodes).bit_length() + 1
    up = [0] * (LOG * max_nodes)
    depth = [0] * max_nodes
    queue = deque([root])
    up[0 * max_nodes + root] = root
    while queue:
        v = queue.popleft()
        for child in (left[v], right[v]):
            if child != -1:
                depth[child] = depth[v] + 1
                up[0 * max_nodes + child] = v
                queue.append(child)

    for k in range(1, LOG):
        prev_offset = (k-1) * max_nodes
        cur_offset = k * max_nodes
        for v in range(max_nodes):
            up[cur_offset + v] = up[prev_offset + up[prev_offset + v]]

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        for k in range(LOG):
            if diff & (1 << k):
                u = up[k * max_nodes + u]
        if u == v:
            return u
        for k in reversed(range(LOG)):
            if up[k * max_nodes + u] != up[k * max_nodes + v]:
                u = up[k * max_nodes + u]
                v = up[k * max_nodes + v]
        return up[0 * max_nodes + u]

    out = []
    for A, B, Y, C, D, Z in queries:
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)
        l = lca(u, v)
        m = height[l]
        ans = abs(Y - Z) + 2 * max(0, min(Y, Z) - m)
        out.append(str(ans))
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    solve()
```