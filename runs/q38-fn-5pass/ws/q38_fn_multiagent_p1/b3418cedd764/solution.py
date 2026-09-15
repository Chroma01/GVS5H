import sys

MOD = 998244353


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = [x - 1 for x in data[2:2 + N]]

    indeg = [0] * N
    for a in A:
        indeg[a] += 1

    # Remove all non-cycle nodes by indegree-zero queue.
    removed = [False] * N
    order = [i for i in range(N) if indeg[i] == 0]
    head = 0
    while head < len(order):
        v = order[head]
        head += 1
        removed[v] = True
        p = A[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            order.append(p)

    is_cycle = [not removed[i] for i in range(N)]

    # children[v] = non-cycle nodes u such that A[u] = v.
    children = [[] for _ in range(N)]
    for i, a in enumerate(A):
        if not is_cycle[i]:
            children[a].append(i)

    M1 = M + 1
    rng = range(1, M1)
    mod = MOD

    # Shared immutable DP array for leaves: f[c] = c.
    leaf = list(range(M1))
    f = [None] * N

    # Bottom-up DP for non-cycle nodes.
    # f[v][c] = number of assignments in v's attached subtree with x_v <= c.
    for v in order:
        exact = None
        for u in children[v]:
            fu = f[u]
            if exact is None:
                # Reuse child's array if it is private; copy the shared leaf array.
                exact = fu[:] if fu is leaf else fu
            else:
                for c in rng:
                    exact[c] = (exact[c] * fu[c]) % mod
            f[u] = None

        if exact is None:
            f[v] = leaf
        else:
            s = 0
            exact[0] = 0
            for c in rng:
                s += exact[c]
                if s >= mod:
                    s -= mod
                exact[c] = s
            f[v] = exact

    ans = 1
    visited = [False] * N

    # Process each directed cycle component.
    for i in range(N):
        if is_cycle[i] and not visited[i]:
            v = i
            prod = None

            while not visited[v]:
                visited[v] = True

                # exact[c] = product of attached-tree contributions of cycle node v
                # when the common cycle value is exactly c.
                exact = None
                for u in children[v]:
                    fu = f[u]
                    if exact is None:
                        exact = fu[:] if fu is leaf else fu
                    else:
                        for c in rng:
                            exact[c] = (exact[c] * fu[c]) % mod
                    f[u] = None

                if exact is not None:
                    if prod is None:
                        prod = exact
                    else:
                        for c in rng:
                            prod[c] = (prod[c] * exact[c]) % mod

                v = A[v]

            if prod is None:
                comp = M % mod
            else:
                comp = 0
                for c in rng:
                    comp += prod[c]
                    if comp >= mod:
                        comp -= mod

            ans = (ans * comp) % mod

    print(ans)


if __name__ == "__main__":
    solve()