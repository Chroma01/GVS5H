import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[1 + i])
    MOD = 998244353

    children = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(1, n + 1):
        a = A[i]
        children[a].append(i)
        indeg[a] += 1

    try:
        import numpy as np
        use_np = True
    except ImportError:
        use_np = False

    peeled = [False] * (n + 1)
    order = []
    q = deque([u for u in range(1, n + 1) if indeg[u] == 0])
    indeg_work = indeg[:]
    while q:
        u = q.popleft()
        peeled[u] = True
        order.append(u)
        p = A[u]
        indeg_work[p] -= 1
        if indeg_work[p] == 0:
            q.append(p)

    on_cycle = [False] * (n + 1)
    for u in range(1, n + 1):
        if not peeled[u]:
            on_cycle[u] = True

    if use_np:
        P = np.empty((n + 1, m), dtype=np.int64)
        ones = np.ones(m, dtype=np.int64)
        for u in order:
            row = ones.copy()
            for c in children[u]:
                row = row * P[c] % MOD
            P[u] = np.cumsum(row) % MOD

        ans = 1
        seen = [False] * (n + 1)
        for u in range(1, n + 1):
            if on_cycle[u] and not seen[u]:
                comp = ones.copy()
                v = u
                while not seen[v]:
                    seen[v] = True
                    for c in children[v]:
                        if not on_cycle[c]:
                            comp = comp * P[c] % MOD
                    v = A[v]
                ans = ans * int(comp.sum() % MOD) % MOD
        print(ans)
    else:
        # Pure-Python fallback
        P = [None] * (n + 1)
        for u in order:
            row = [1] * m
            for c in children[u]:
                pc = P[c]
                row = [(row[k] * pc[k]) % MOD for k in range(m)]
            s = 0
            pref = [0] * m
            for k in range(m):
                s += row[k]
                if s >= MOD:
                    s -= MOD
                pref[k] = s
            P[u] = pref

        ans = 1
        seen = [False] * (n + 1)
        for u in range(1, n + 1):
            if on_cycle[u] and not seen[u]:
                comp = [1] * m
                v = u
                while not seen[v]:
                    seen[v] = True
                    for c in children[v]:
                        if not on_cycle[c]:
                            pc = P[c]
                            comp = [(comp[k] * pc[k]) % MOD for k in range(m)]
                    v = A[v]
                ans = ans * (sum(comp) % MOD) % MOD
        print(ans)

solve()