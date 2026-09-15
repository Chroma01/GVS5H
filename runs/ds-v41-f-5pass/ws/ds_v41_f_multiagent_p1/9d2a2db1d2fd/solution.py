import sys
from array import array

def main():
    data = sys.stdin.buffer.read()
    idx = 0
    n = len(data)
    def next_int():
        nonlocal idx
        while idx < n and data[idx] <= 32:
            idx += 1
        num = 0
        while idx < n and data[idx] > 32:
            num = num * 10 + (data[idx] - 48)
            idx += 1
        return num

    H = next_int()
    W = next_int()
    V = H * W
    F = [0] * V
    for i in range(V):
        F[i] = next_int()

    N_max = 2 * V
    left = array('i', [-1]) * N_max
    right = array('i', [-1]) * N_max
    weight = array('i', [0]) * N_max
    for i in range(V):
        weight[i] = F[i]

    edges = []
    for i in range(H):
        base = i * W
        for j in range(W):
            u = base + j
            if j + 1 < W:
                v = u + 1
                w = F[u] if F[u] < F[v] else F[v]
                edges.append((w << 36) | (u << 18) | v)
            if i + 1 < H:
                v = u + W
                w = F[u] if F[u] < F[v] else F[v]
                edges.append((w << 36) | (u << 18) | v)
    del F
    edges.sort(reverse=True)

    dsu_parent = array('i', range(N_max))
    next_idx = V

    def find(x):
        while dsu_parent[x] != x:
            dsu_parent[x] = dsu_parent[dsu_parent[x]]
            x = dsu_parent[x]
        return x

    for key in edges:
        w = key >> 36
        u = (key >> 18) & 0x3FFFF
        v = key & 0x3FFFF
        ru = find(u)
        rv = find(v)
        if ru != rv:
            cur = next_idx
            next_idx += 1
            weight[cur] = w
            left[cur] = ru
            right[cur] = rv
            dsu_parent[ru] = cur
            dsu_parent[rv] = cur
            dsu_parent[cur] = cur

    del edges, dsu_parent

    N = next_idx
    root = N - 1 if V > 1 else 0

    Q = next_int()
    ans = [0] * Q
    head = array('i', [-1]) * N
    q_to = array('i', [0]) * (2 * Q)
    q_nxt = array('i', [0]) * (2 * Q)
    q_id = array('i', [0]) * (2 * Q)
    q_ptr = 0
    q_Y = []
    q_Z = []
    q_orig = []
    valid_qid = 0

    for i in range(Q):
        A = next_int()
        B = next_int()
        Y = next_int()
        C = next_int()
        D = next_int()
        Z = next_int()
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)
        if u == v:
            ans[i] = abs(Y - Z)
        else:
            q_Y.append(Y)
            q_Z.append(Z)
            q_orig.append(i)
            q_to[q_ptr] = v
            q_id[q_ptr] = valid_qid
            q_nxt[q_ptr] = head[u]
            head[u] = q_ptr
            q_ptr += 1
            q_to[q_ptr] = u
            q_id[q_ptr] = valid_qid
            q_nxt[q_ptr] = head[v]
            head[v] = q_ptr
            q_ptr += 1
            valid_qid += 1

    t_dsu = array('i', range(N))
    t_size = array('i', [1]) * N
    t_ancestor = array('i', range(N))
    visited = bytearray(N)

    def t_find(x):
        while t_dsu[x] != x:
            t_dsu[x] = t_dsu[t_dsu[x]]
            x = t_dsu[x]
        return x

    def t_union(u, v):
        ru = t_find(u)
        rv = t_find(v)
        if ru != rv:
            if t_size[ru] < t_size[rv]:
                ru, rv = rv, ru
            t_dsu[rv] = ru
            t_size[ru] += t_size[rv]
        t_ancestor[ru] = u

    stack = [(root, 0)]
    while stack:
        u, state = stack.pop()
        if state == 0:
            l = left[u]
            if l != -1:
                stack.append((u, 1))
                stack.append((l, 0))
            else:
                visited[u] = 1
                e = head[u]
                while e != -1:
                    v = q_to[e]
                    if visited[v]:
                        qi = q_id[e]
                        lca = t_ancestor[t_find(v)]
                        w = weight[lca]
                        Y = q_Y[qi]
                        Z = q_Z[qi]
                        if w >= (Y if Y < Z else Z):
                            ans[q_orig[qi]] = abs(Y - Z)
                        else:
                            ans[q_orig[qi]] = Y + Z - 2 * w
                    e = q_nxt[e]
        elif state == 1:
            l = left[u]
            r = right[u]
            t_union(u, l)
            stack.append((u, 2))
            stack.append((r, 0))
        else:
            r = right[u]
            t_union(u, r)
            visited[u] = 1
            e = head[u]
            while e != -1:
                v = q_to[e]
                if visited[v]:
                    qi = q_id[e]
                    lca = t_ancestor[t_find(v)]
                    w = weight[lca]
                    Y = q_Y[qi]
                    Z = q_Z[qi]
                    if w >= (Y if Y < Z else Z):
                        ans[q_orig[qi]] = abs(Y - Z)
                    else:
                        ans[q_orig[qi]] = Y + Z - 2 * w
                e = q_nxt[e]

    sys.stdout.write('\n'.join(map(str, ans)))

if __name__ == '__main__':
    main()