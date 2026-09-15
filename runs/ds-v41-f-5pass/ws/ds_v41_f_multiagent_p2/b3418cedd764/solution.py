import sys
from collections import deque

def main():
    MOD = 998244353
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M = data[0], data[1]
    A = [0] + data[2:2 + N]

    indeg = [0] * (N + 1)
    for i in range(1, N + 1):
        indeg[A[i]] += 1

    q = deque(i for i in range(1, N + 1) if indeg[i] == 0)
    removed = []
    is_cycle = [True] * (N + 1)

    while q:
        u = q.popleft()
        removed.append(u)
        is_cycle[u] = False
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    acc = [None] * (N + 1)

    for u in removed:
        arr = acc[u]
        p = A[u]
        ap = acc[p]

        if ap is None:
            if arr is None:
                acc[p] = list(range(M + 1))
            else:
                pref = [0] * (M + 1)
                s = 0
                for t in range(1, M + 1):
                    s += arr[t]
                    if s >= MOD:
                        s -= MOD
                    pref[t] = s
                acc[p] = pref
        else:
            if arr is None:
                for t in range(1, M + 1):
                    ap[t] = (ap[t] * t) % MOD
            else:
                s = 0
                for t in range(1, M + 1):
                    s += arr[t]
                    if s >= MOD:
                        s -= MOD
                    ap[t] = (ap[t] * s) % MOD

        acc[u] = None

    ans = 1
    visited = [False] * (N + 1)

    for i in range(1, N + 1):
        if is_cycle[i] and not visited[i]:
            cyc = []
            v = i
            while not visited[v]:
                visited[v] = True
                cyc.append(v)
                v = A[v]

            prod = None
            for v in cyc:
                arr = acc[v]
                if arr is not None:
                    if prod is None:
                        prod = arr
                        acc[v] = None
                    else:
                        for t in range(1, M + 1):
                            prod[t] = (prod[t] * arr[t]) % MOD
                        acc[v] = None

            if prod is None:
                cycle_sum = M % MOD
            else:
                cycle_sum = sum(prod[1:]) % MOD

            ans = (ans * cycle_sum) % MOD

    print(ans)

if __name__ == "__main__":
    main()