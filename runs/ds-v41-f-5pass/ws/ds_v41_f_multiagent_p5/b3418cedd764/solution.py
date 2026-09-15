import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(data[1 + i])
    MOD = 998244353
    indeg = [0] * (N + 1)
    for i in range(1, N + 1):
        indeg[A[i]] += 1

    q = deque()
    for i in range(1, N + 1):
        if indeg[i] == 0:
            q.append(i)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    G = [None] * (N + 1)
    P = [None] * (N + 1)

    M1 = M + 1
    mod = MOD
    rng = range(1, M1)

    for u in order:
        arr = G[u]
        if arr is None:
            arr = [1] * M1
        s = 0
        for t in rng:
            s += arr[t]
            if s >= mod:
                s -= mod
            arr[t] = s
        p = A[u]
        if indeg[p] > 0:
            parr = P[p]
            if parr is None:
                P[p] = arr
            else:
                for t in rng:
                    parr[t] = (parr[t] * arr[t]) % mod
        else:
            garr = G[p]
            if garr is None:
                G[p] = arr
            else:
                for t in rng:
                    garr[t] = (garr[t] * arr[t]) % mod
        G[u] = None

    visited = [False] * (N + 1)
    ans = 1
    for i in range(1, N + 1):
        if indeg[i] > 0 and not visited[i]:
            cyc = []
            u = i
            while not visited[u]:
                visited[u] = True
                cyc.append(u)
                u = A[u]
            count = 0
            last_p = None
            for c in cyc:
                parr = P[c]
                if parr is not None:
                    count += 1
                    last_p = parr
            if count == 0:
                total = M
            elif count == 1:
                total = sum(last_p[1:]) % mod
            else:
                prod = [1] * M1
                for c in cyc:
                    parr = P[c]
                    if parr is not None:
                        for t in rng:
                            prod[t] = (prod[t] * parr[t]) % mod
                total = sum(prod[1:]) % mod
            ans = (ans * total) % mod

    print(ans)

if __name__ == '__main__':
    main()