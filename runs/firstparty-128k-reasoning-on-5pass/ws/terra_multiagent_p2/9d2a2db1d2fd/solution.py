import sys
from array import array

data = sys.stdin.buffer.read()
pos = 0
length = len(data)

def next_int():
    global pos
    while pos < length and data[pos] <= 32:
        pos += 1
    x = 0
    while pos < length and data[pos] > 32:
        x = x * 10 + (data[pos] - 48)
        pos += 1
    return x

H = next_int()
W = next_int()
N = H * W

F = [next_int() for _ in range(N)]

# Edge encoding:
# (weight << 19) | (u << 1) | direction
# direction 0: u -> u+1, direction 1: u -> u+W
SHIFT = 19
MASK = (1 << SHIFT) - 1
edges = []

for i in range(H):
    base = i * W
    for j in range(W):
        u = base + j
        if j + 1 < W:
            v = u + 1
            weight = F[u] if F[u] < F[v] else F[v]
            edges.append((weight << SHIFT) | (u << 1))
        if i + 1 < H:
            v = u + W
            weight = F[u] if F[u] < F[v] else F[v]
            edges.append((weight << SHIFT) | (u << 1) | 1)

edges.sort(reverse=True)

# DSU for Kruskal
dsu_parent = list(range(N))
dsu_size = [1] * N

def find(x):
    while dsu_parent[x] != x:
        dsu_parent[x] = dsu_parent[dsu_parent[x]]
        x = dsu_parent[x]
    return x

# Compact adjacency representation of the maximum spanning tree
head = array('i', [-1]) * N
to = array('i')
nxt = array('i')
edge_weight = array('i')

def add_edge(u, v, w):
    to.append(v)
    edge_weight.append(w)
    nxt.append(head[u])
    head[u] = len(to) - 1

used = 0
for code in edges:
    w = code >> SHIFT
    info = code & MASK
    u = info >> 1
    if info & 1:
        v = u + W
    else:
        v = u + 1

    ru = find(u)
    rv = find(v)
    if ru == rv:
        continue

    if dsu_size[ru] < dsu_size[rv]:
        ru, rv = rv, ru
    dsu_parent[rv] = ru
    dsu_size[ru] += dsu_size[rv]

    add_edge(u, v, w)
    add_edge(v, u, w)
    used += 1
    if used == N - 1:
        break

# Root the tree at vertex 0.
tree_parent = array('i', [-1]) * N
depth = array('i', [0]) * N
base_min = array('i', [0]) * N

INF = 1_000_000_001
tree_parent[0] = 0
base_min[0] = INF

stack = [0]
while stack:
    u = stack.pop()
    e = head[u]
    while e != -1:
        v = to[e]
        if tree_parent[v] == -1:
            tree_parent[v] = u
            depth[v] = depth[u] + 1
            base_min[v] = edge_weight[e]
            stack.append(v)
        e = nxt[e]

# Binary lifting tables.
LOG = N.bit_length()
up = [tree_parent]
minimum = [base_min]

for _ in range(1, LOG):
    prev_up = up[-1]
    prev_min = minimum[-1]
    cur_up = array('i', [0]) * N
    cur_min = array('i', [0]) * N
    for v in range(N):
        p = prev_up[v]
        cur_up[v] = prev_up[p]
        a = prev_min[v]
        b = prev_min[p]
        cur_min[v] = a if a < b else b
    up.append(cur_up)
    minimum.append(cur_min)

def bottleneck(a, b):
    if a == b:
        return INF

    result = INF

    if depth[a] < depth[b]:
        a, b = b, a

    diff = depth[a] - depth[b]
    bit = 0
    while diff:
        if diff & 1:
            val = minimum[bit][a]
            if val < result:
                result = val
            a = up[bit][a]
        diff >>= 1
        bit += 1

    if a == b:
        return result

    for k in range(LOG - 1, -1, -1):
        if up[k][a] != up[k][b]:
            va = minimum[k][a]
            vb = minimum[k][b]
            if va < result:
                result = va
            if vb < result:
                result = vb
            a = up[k][a]
            b = up[k][b]

    va = minimum[0][a]
    vb = minimum[0][b]
    if va < result:
        result = va
    if vb < result:
        result = vb
    return result

Q = next_int()
out = []

for _ in range(Q):
    A = next_int() - 1
    B = next_int() - 1
    Y = next_int()
    C = next_int() - 1
    D = next_int() - 1
    Z = next_int()

    u = A * W + B
    v = C * W + D

    if u == v:
        out.append(str(abs(Y - Z)))
        continue

    t = bottleneck(u, v)
    lower = Y if Y < Z else Z
    extra = lower - t
    if extra < 0:
        extra = 0
    out.append(str(abs(Y - Z) + 2 * extra))

sys.stdout.write("\n".join(out))