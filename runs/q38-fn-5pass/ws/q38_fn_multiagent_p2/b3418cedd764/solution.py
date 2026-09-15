import sys
from collections import deque

MOD = 998244353


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = [x - 1 for x in data[2:2 + N]]

    indeg = [0] * N
    for a in A:
        indeg[a] += 1

    q = deque(i for i in range(N) if indeg[i] == 0)

    m1 = M + 1
    rng = range(1, m1)
    mod = MOD

    # acc[u] stores the pointwise product of prefix-DP arrays of already
    # processed non-cycle children of u.
    acc = [None] * N

    # Leaf fixed-value array is 1 for every positive value, and its prefix
    # array is [0, 1, 2, ..., M].
    base = list(range(m1))

    # Peel non-cycle nodes.  When a node is popped, all its non-cycle children
    # have already contributed to acc[u].
    while q:
        u = q.popleft()
        p = A[u]
        g = acc[u]

        if g is None:
            # Leaf: F_u(v) = v.
            ap = acc[p]
            if ap is None:
                acc[p] = base.copy()
            else:
                for v in rng:
                    ap[v] = (ap[v] * v) % mod
        else:
            # Internal node: acc[u] is G_u(v) = product F_child(v).
            # Convert it in-place to F_u(v) = sum_{t=1}^v G_u(t).
            acc[u] = None
            s = 0
            for v in rng:
                s += g[v]
                if s >= mod:
                    s -= mod
                g[v] = s

            ap = acc[p]
            if ap is None:
                acc[p] = g
            else:
                for v in rng:
                    ap[v] = (ap[v] * g[v]) % mod

        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    ans = 1
    visited = [False] * N

    # Remaining nodes with indeg > 0 are exactly cycle nodes.
    for i in range(N):
        if indeg[i] > 0 and not visited[i]:
            prod = [1] * m1
            has_attached = False

            u = i
            while not visited[u]:
                visited[u] = True
                h = acc[u]
                if h is not None:
                    has_attached = True
                    for v in rng:
                        prod[v] = (prod[v] * h[v]) % mod
                    acc[u] = None
                u = A[u]

            if has_attached:
                # prod[0] is kept as 1 and is not part of the sum.
                comp = (sum(prod) - 1) % mod
            else:
                comp = M % mod

            ans = (ans * comp) % mod

    print(ans)


if __name__ == "__main__":
    main()