import sys
from array import array


def int_stream():
    data = sys.stdin.buffer.read()
    n = len(data)
    i = 0
    while i < n:
        while i < n and data[i] <= 32:
            i += 1
        if i >= n:
            return
        x = 0
        while i < n and data[i] > 32:
            x = x * 10 + data[i] - 48
            i += 1
        yield x


it = int_stream()
H = next(it)
W = next(it)
N = H * W

F = [next(it) for _ in range(N)]
order = sorted(range(N), key=F.__getitem__, reverse=True)

active = bytearray(N)
dsu = [-1] * N
component_node = list(range(N))

parent = [-1] * N
node_weight = [0] * N


def find(x):
    while dsu[x] >= 0:
        if dsu[dsu[x]] >= 0:
            dsu[x] = dsu[dsu[x]]
        x = dsu[x]
    return x


for v in order:
    active[v] = 1
    dsu[v] = -1

    r = v // W
    c = v - r * W
    neighbors = []

    if r > 0 and active[v - W]:
        neighbors.append(v - W)
    if r + 1 < H and active[v + W]:
        neighbors.append(v + W)
    if c > 0 and active[v - 1]:
        neighbors.append(v - 1)
    if c + 1 < W and active[v + 1]:
        neighbors.append(v + 1)

    for u in neighbors:
        a = find(v)
        b = find(u)
        if a == b:
            continue

        if dsu[a] > dsu[b]:
            a, b = b, a

        new_node = len(parent)
        parent.append(-1)
        node_weight.append(F[v])

        parent[component_node[a]] = new_node
        parent[component_node[b]] = new_node

        dsu[a] += dsu[b]
        dsu[b] = a
        component_node[a] = new_node

root_node = component_node[find(0)]
parent[root_node] = root_node
total_nodes = len(parent)

depth = array("i", [0]) * total_nodes
for v in range(total_nodes - 1, -1, -1):
    p = parent[v]
    if p != v:
        depth[v] = depth[p] + 1

log = total_nodes.bit_length()
up = [array("i", parent)]

for _ in range(1, log):
    prev = up[-1]
    up.append(array("i", (prev[prev[v]] for v in range(total_nodes))))


def lca(a, b):
    if depth[a] < depth[b]:
        a, b = b, a

    diff = depth[a] - depth[b]
    bit = 0
    while diff:
        if diff & 1:
            a = up[bit][a]
        diff >>= 1
        bit += 1

    if a == b:
        return a

    for k in range(log - 1, -1, -1):
        ua = up[k][a]
        ub = up[k][b]
        if ua != ub:
            a = ua
            b = ub

    return up[0][a]


Q = next(it)
answers = []

for _ in range(Q):
    a = next(it) - 1
    b = next(it) - 1
    y = next(it)
    c = next(it) - 1
    d = next(it) - 1
    z = next(it)

    s = a * W + b
    t = c * W + d

    if s == t:
        bottleneck = F[s]
    else:
        bottleneck = node_weight[lca(s, t)]

    extra = min(y, z) - bottleneck
    if extra < 0:
        extra = 0

    answers.append(str(abs(y - z) + 2 * extra))

sys.stdout.write("\n".join(answers))