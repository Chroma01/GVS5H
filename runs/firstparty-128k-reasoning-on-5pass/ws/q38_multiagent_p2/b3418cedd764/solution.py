import sys
from collections import deque
from array import array

MOD = 998244353


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = [x - 1 for x in data[2:2 + n]]

    # Detect cycle nodes by indegree pruning.
    indeg = [0] * n
    for p in a:
        indeg[p] += 1

    q = deque(i for i in range(n) if indeg[i] == 0)
    while q:
        v = q.popleft()
        p = a[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    in_cycle = [d > 0 for d in indeg]

    # Build children lists using only non-cycle nodes.
    children = [[] for _ in range(n)]
    child_count = [0] * n
    for u in range(n):
        if not in_cycle[u]:
            p = a[u]
            children[p].append(u)
            child_count[p] += 1

    # Leaf-to-root topological order for non-cycle nodes.
    q = deque(i for i in range(n) if not in_cycle[i] and child_count[i] == 0)
    order = []
    while q:
        v = q.popleft()
        order.append(v)
        p = a[v]
        if not in_cycle[p]:
            child_count[p] -= 1
            if child_count[p] == 0:
                q.append(p)

    # Explicit prefix arrays P[v][c] for non-cycle nodes, c = 0..M.
    P = [None] * n
    leaf_template = array('I', range(m + 1))
    zero_template = array('I', [0]) * (m + 1)
    rng = range(1, m + 1)
    mod = MOD

    for v in order:
        ch = children[v]

        # Leaf: f_v[c] = 1, so P_v[c] = c.
        if not ch:
            P[v] = leaf_template[:]
            continue

        row = zero_template[:]

        # One child: P_v[c] = P_v[c-1] + P_child[c].
        if len(ch) == 1:
            child = P[ch[0]]
            prev = 0
            for c in rng:
                val = prev + child[c]
                if val >= mod:
                    val -= mod
                row[c] = val
                prev = val

        # Two children: avoid an inner loop.
        elif len(ch) == 2:
            r1 = P[ch[0]]
            r2 = P[ch[1]]
            prev = 0
            for c in rng:
                prod = (r1[c] * r2[c]) % mod
                val = prev + prod
                if val >= mod:
                    val -= mod
                row[c] = val
                prev = val

        # General case: f_v[c] = product of children's prefix values.
        else:
            child_rows = [P[u] for u in ch]
            prev = 0
            for c in rng:
                prod = 1
                for cr in child_rows:
                    prod = (prod * cr[c]) % mod
                val = prev + prod
                if val >= mod:
                    val -= mod
                row[c] = val
                prev = val

        P[v] = row

    # Process each cycle component.
    visited = [False] * n
    ans = 1

    for i in range(n):
        if in_cycle[i] and not visited[i]:
            v = i
            boundary = []

            # Traverse the cycle and collect immediate non-cycle children.
            while not visited[v]:
                visited[v] = True
                boundary.extend(children[v])
                v = a[v]

            # Contribution of this component:
            # sum over common cycle value c of product over boundary P[u][c].
            if not boundary:
                s = m % mod
            else:
                rows = [P[u] for u in boundary]
                s = 0

                if len(rows) == 1:
                    row = rows[0]
                    for c in rng:
                        s += row[c]
                        if s >= mod:
                            s -= mod

                elif len(rows) == 2:
                    r1 = rows[0]
                    r2 = rows[1]
                    for c in rng:
                        prod = (r1[c] * r2[c]) % mod
                        s += prod
                        if s >= mod:
                            s -= mod

                else:
                    for c in rng:
                        prod = 1
                        for cr in rows:
                            prod = (prod * cr[c]) % mod
                        s += prod
                        if s >= mod:
                            s -= mod

            ans = (ans * s) % mod

    print(ans)


if __name__ == "__main__":
    main()