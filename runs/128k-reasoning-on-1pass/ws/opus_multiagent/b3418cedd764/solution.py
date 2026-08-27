import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = [int(x) - 1 for x in data[2:2 + n]]
    MOD = 998244353

    # ---- functional graph cycle detection (iterative, 3-state coloring) ----
    color = [0] * n          # 0 unvisited, 1 on current path, 2 finished
    on_cycle = [False] * n
    cycles = []
    for s in range(n):
        if color[s]:
            continue
        path = []
        v = s
        while color[v] == 0:
            color[v] = 1
            path.append(v)
            v = A[v]
        if color[v] == 1:
            # new cycle found, starting at v
            cyc = []
            u = v
            while True:
                cyc.append(u)
                on_cycle[u] = True
                u = A[u]
                if u == v:
                    break
            cycles.append(cyc)
        for u in path:
            color[u] = 2

    # ---- children lists (only non-cycle nodes hang as children) ----
    children = [[] for _ in range(n)]
    for i in range(n):
        if not on_cycle[i]:
            children[A[i]].append(i)

    # ---- bottom-up order (iterative DFS from cycle nodes' children) ----
    order = []
    stack = []
    for cyc in cycles:
        for u in cyc:
            ch = children[u]
            if ch:
                stack.extend(ch)
    while stack:
        v = stack.pop()
        order.append(v)
        ch = children[v]
        if ch:
            stack.extend(ch)

    try:
        import numpy as np
    except Exception:
        np = None

    ans = 1

    if np is not None:
        base = np.arange(1, m + 1, dtype=np.int64)   # cumsum of all-ones
        acc = [None] * n                             # None means "all ones"
        for v in reversed(order):
            a = acc[v]
            if a is None:
                p = base
            else:
                p = np.cumsum(a) % MOD
                acc[v] = None
            par = A[v]
            b = acc[par]
            if b is None:
                acc[par] = p
            else:
                acc[par] = b * p % MOD
        for cyc in cycles:
            g = None
            for u in cyc:
                au = acc[u]
                if au is not None:
                    g = au if g is None else g * au % MOD
            if g is None:
                comp = m % MOD
            else:
                comp = int(g.sum() % MOD)
            ans = ans * comp % MOD
    else:
        from itertools import accumulate
        base = list(range(1, m + 1))
        acc = [None] * n
        for v in reversed(order):
            a = acc[v]
            if a is None:
                p = base
            else:
                p = [x % MOD for x in accumulate(a)]
                acc[v] = None
            par = A[v]
            b = acc[par]
            if b is None:
                acc[par] = p
            else:
                acc[par] = [x * y % MOD for x, y in zip(b, p)]
        for cyc in cycles:
            g = None
            for u in cyc:
                au = acc[u]
                if au is not None:
                    g = au if g is None else [x * y % MOD for x, y in zip(g, au)]
            if g is None:
                comp = m % MOD
            else:
                comp = sum(g) % MOD
            ans = ans * comp % MOD

    sys.stdout.write(str(ans % MOD) + "\n")

main()