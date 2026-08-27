```python
import sys
from collections import deque
from array import array

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M = data[0], data[1]
    A = [0] + data[2:2 + N]

    indeg = [0] * (N + 1)
    for a in A[1:]:
        indeg[a] += 1

    in_cycle = [True] * (N + 1)
    q = deque(i for i in range(1, N + 1) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        in_cycle[u] = False
        order.append(u)
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        p = A[i]
        if in_cycle[i] and in_cycle[p]:
            continue
        children[p].append(i)

    pref = [None] * (N + 1)  # pref[u][t] = sum_{s<=t} f_u(s)

    for u in order:
        ch = children[u]
        arr = array('i', [0]) * (M + 1)
        if not ch:
            for t in range(1, M + 1):
                arr[t] = t
        else:
            f = [1] * (M + 1)
            for w in ch:
                pw = pref[w]
                for t in range(1, M + 1):
                    f[t] = (f[t] * pw[t]) % MOD
            run = 0
            for t in range(1, M + 1):
                run += f[t]
                if run >= MOD:
                    run -= MOD
                arr[t] = run
        pref[u] = arr
        for w in ch:
            pref[w] = None

    seen = [False] * (N + 1)
    ans = 1
    for s in range(1, N + 1):
        if not in_cycle[s] or seen[s]:
            continue
        cyc = []
        v = s
        while not seen[v]:
            seen[v] = True
            cyc.append(v)
            v = A[v]

        comp = 0
        for c in range(1, M + 1):
            prod = 1
            for v in cyc:
                for w in children[v]:
                    prod = (prod * pref[w][c]) % MOD
            comp += prod
            if comp >= MOD:
                comp -= MOD
        ans = (ans * comp) % MOD

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()
```