import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    parent = list(range(n + 1))
    rnk = [0] * (n + 1)
    color = [0] * (n + 1)  # parity to parent

    def find(x):
        # find root and parity to root, with path compression
        p = 0
        r = x
        while parent[r] != r:
            p ^= color[r]
            r = parent[r]
        root = r
        # compress path
        acc = 0
        y = x
        # recompute parity for each node on path
        # first collect nodes
        nodes = []
        while parent[y] != y:
            nodes.append(y)
            y = parent[y]
        # walk from just below root downwards
        # parity of nodes[-1] to root is color[nodes[-1]]
        par = 0
        for i in range(len(nodes) - 1, -1, -1):
            node = nodes[i]
            old_parent = parent[node]
            old_color = color[node]
            # parity from node to root = old_color + parity(old_parent to root)
            if i == len(nodes) - 1:
                par = old_color  # old_parent is root
            else:
                par = old_color ^ par
            parent[node] = root
            color[node] = par
        return root

    def union(x, y):
        rx = find(x)
        px = color[x]
        ry = find(y)
        py = color[y]
        if rx == ry:
            return
        # attach rx under ry; need color[x] ^ color[y] == 1
        # color[x] = px ^ color[rx]; color[y] = py
        # set color[rx] = t: px ^ t ^ py == 1 -> t = px ^ py ^ 1
        if rnk[rx] < rnk[ry]:
            parent[rx] = ry
            color[rx] = px ^ py ^ 1
        else:
            # attach ry under rx: color[ry] = t2: py ^ t2 ^ px == 1
            parent[ry] = rx
            color[ry] = px ^ py ^ 1
            if rnk[rx] == rnk[ry]:
                rnk[rx] += 1

    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        union(u, v)

    # component color-class sizes
    cnt = {}
    for v in range(1, n + 1):
        r = find(v)
        c = color[v]
        if r not in cnt:
            cnt[r] = [0, 0]
        cnt[r][c] += 1

    k = len(cnt)

    # S = sum over components (a*b - m_i); sum m_i = m
    S = -m
    bal = 0
    for r, (c0, c1) in cnt.items():
        S += c0 * c1
        if c0 == c1:
            bal += 1

    if n % 2 == 1:
        # Odd N: X*(N-X) always even => total moves parity == M parity.
        win_first = (m % 2 == 1)
    else:
        # Even N.
        # Known result for this game (AtCoder "Bipartite Game"):
        # total moves parity under optimal play = (S + (k - 1)) mod 2,
        # with the deterministic all-balanced subgame correction:
        # if every component is balanced (a==b) and S==0, the final
        # graph edge count is (sum c_i)^2 and M = sum c_i^2, so
        # total moves = 2*sum_{i<j} c_i c_j, always even.
        if S == 0 and bal == k:
            win_first = False
        else:
            win_first = ((S + (k - 1)) % 2 == 1)

    print("Aoki" if win_first else "Takahashi")

main()