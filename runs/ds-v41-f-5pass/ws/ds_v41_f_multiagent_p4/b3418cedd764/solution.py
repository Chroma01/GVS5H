import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[1 + i])
    MOD = 998244353

    # --- find cycle nodes by iterative indegree pruning ---
    indeg = [0] * (n + 1)
    for i in range(1, n + 1):
        indeg[A[i]] += 1

    on_cycle = [True] * (n + 1)
    on_cycle[0] = False
    dq = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    while dq:
        u = dq.popleft()
        on_cycle[u] = False
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            dq.append(v)

    # children[v] = non-cycle nodes u with A[u] == v (tree edges into v)
    children = [[] for _ in range(n + 1)]
    for u in range(1, n + 1):
        if not on_cycle[u]:
            children[A[u]].append(u)

    # BFS outward from cycle nodes -> parents before children
    order = []
    dq = deque(i for i in range(1, n + 1) if on_cycle[i])
    while dq:
        v = dq.popleft()
        for u in children[v]:
            order.append(u)
            dq.append(u)

    # P[v][i] for c=i+1 holds prefix sums of g_v; g_v(c)=prod over tree children of prefix
    ident = list(range(1, m + 1))   # shared array for leaves: prefix(c)=c
    rng = range(m)
    P = [None] * (n + 1)

    for v in reversed(order):       # leaves first
        cv = children[v]
        lc = len(cv)
        if lc == 0:
            P[v] = ident
            continue
        if lc == 1:
            pu = P[cv[0]]
            P[cv[0]] = None
            arr = [0] * m
            run = 0
            for i in rng:
                run += pu[i]
                if run >= MOD:
                    run -= MOD
                arr[i] = run
            P[v] = arr
            continue
        arr = [1] * m
        for u in cv:
            pu = P[u]
            P[u] = None
            arr = [(a * b) % MOD for a, b in zip(arr, pu)]
        run = 0
        for i in rng:
            run += arr[i]
            if run >= MOD:
                run -= MOD
            arr[i] = run
        P[v] = arr

    # --- combine each cycle ---
    visited = [False] * (n + 1)
    ans = 1
    for i in range(1, n + 1):
        if on_cycle[i] and not visited[i]:
            cyc = []
            j = i
            while not visited[j]:
                visited[j] = True
                cyc.append(j)
                j = A[j]
            comp = None
            for v in cyc:
                for u in children[v]:
                    pu = P[u]
                    P[u] = None
                    if comp is None:
                        comp = pu
                    else:
                        comp = [(a * b) % MOD for a, b in zip(comp, pu)]
            if comp is None:
                comp = [1] * m          # cycle with no attached trees -> M choices
            s = 0
            for x in comp:
                s += x
            ans = ans * (s % MOD) % MOD
    print(ans % MOD)

main()