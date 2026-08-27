import sys

def main():
    readline = sys.stdin.buffer.readline
    H, W = map(int, readline().split())
    N = H * W

    weight = [0] * N
    for i in range(H):
        weight[i * W:(i + 1) * W] = list(map(int, readline().split()))

    Q = int(readline())

    max_nodes = 2 * N - 1
    weight.extend([0] * (N - 1))
    left = [-1] * max_nodes
    right = [-1] * max_nodes
    parent = [-1] * max_nodes

    order = list(range(N))
    order.sort(key=weight.__getitem__, reverse=True)

    node_count = N

    def find(x, parent=parent):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    Wl = W
    N_minus_W = N - W
    parent_l = parent
    weight_l = weight
    left_l = left
    right_l = right

    for idx in order:
        h = weight_l[idx]
        parent_l[idx] = idx
        cur = idx

        if idx >= Wl:
            nb = idx - Wl
            if parent_l[nb] != -1:
                rb = find(nb)
                if rb != cur:
                    new = node_count
                    node_count += 1
                    weight_l[new] = h
                    left_l[new] = cur
                    right_l[new] = rb
                    parent_l[cur] = new
                    parent_l[rb] = new
                    parent_l[new] = new
                    cur = new

        if idx < N_minus_W:
            nb = idx + Wl
            if parent_l[nb] != -1:
                rb = find(nb)
                if rb != cur:
                    new = node_count
                    node_count += 1
                    weight_l[new] = h
                    left_l[new] = cur
                    right_l[new] = rb
                    parent_l[cur] = new
                    parent_l[rb] = new
                    parent_l[new] = new
                    cur = new

        col = idx % Wl
        if col:
            nb = idx - 1
            if parent_l[nb] != -1:
                rb = find(nb)
                if rb != cur:
                    new = node_count
                    node_count += 1
                    weight_l[new] = h
                    left_l[new] = cur
                    right_l[new] = rb
                    parent_l[cur] = new
                    parent_l[rb] = new
                    parent_l[new] = new
                    cur = new

        if col != Wl - 1:
            nb = idx + 1
            if parent_l[nb] != -1:
                rb = find(nb)
                if rb != cur:
                    new = node_count
                    node_count += 1
                    weight_l[new] = h
                    left_l[new] = cur
                    right_l[new] = rb
                    parent_l[cur] = new
                    parent_l[rb] = new
                    parent_l[new] = new
                    cur = new

    root = find(0)
    del order, parent, find, parent_l

    L = 2 * node_count - 1
    S = 1
    while S < L:
        S <<= 1

    seg = [0] * (2 * S)
    first = [-1] * N
    depth = [0] * node_count

    stack = [root << 2]
    pop = stack.pop
    push = stack.append
    pos = S
    N_l = N
    left_l = left
    right_l = right

    while stack:
        code = pop()
        v = code >> 2
        state = code & 3

        if state == 0:
            if v < N_l:
                first[v] = pos - S
            seg[pos] = v
            pos += 1

            lv = left_l[v]
            if lv != -1:
                dv = depth[v] + 1
                depth[lv] = dv
                rv = right_l[v]
                depth[rv] = dv

                push((v << 2) | 2)
                push((rv << 2) | 0)
                push((v << 2) | 1)
                push((lv << 2) | 0)
        else:
            seg[pos] = v
            pos += 1

    del left, right, left_l, right_l, stack, pop, push

    INF = 10 ** 9
    dummy = node_count
    depth.append(INF)
    weight.append(0)

    if S > L:
        seg[S + L:2 * S] = [dummy] * (S - L)

    depth_l = depth
    for i in range(S - 1, 0, -1):
        a = seg[i << 1]
        b = seg[i << 1 | 1]
        if depth_l[a] <= depth_l[b]:
            seg[i] = a
        else:
            seg[i] = b

    out = [None] * Q

    first_l = first
    depth_l = depth
    seg_l = seg
    weight_l = weight
    S_l = S
    S1 = S + 1
    W_l = W
    INF_l = INF

    int_ = int
    mp = map
    str_ = str

    for i in range(Q):
        a, b, y, c, d, z = mp(int_, readline().split())

        u = (a - 1) * W_l + b - 1
        v = (c - 1) * W_l + d - 1
        ys = y + z

        if u == v:
            M = weight_l[u]
        else:
            l = first_l[u]
            r = first_l[v]
            if l > r:
                l, r = r, l

            l += S_l
            r += S1

            best = -1
            bd = INF_l

            while l < r:
                if l & 1:
                    node = seg_l[l]
                    dn = depth_l[node]
                    if dn < bd:
                        bd = dn
                        best = node
                    l += 1

                if r & 1:
                    r -= 1
                    node = seg_l[r]
                    dn = depth_l[node]
                    if dn < bd:
                        bd = dn
                        best = node

                l >>= 1
                r >>= 1

            M = weight_l[best]

        ans = y - z
        if ans < 0:
            ans = -ans

        t = ys - (M << 1)
        if t > ans:
            ans = t

        out[i] = str_(ans)

    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()