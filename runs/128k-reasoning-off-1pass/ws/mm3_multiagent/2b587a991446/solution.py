import sys
from collections import deque

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    S = int(next(it))
    T = int(next(it))
    adj = [[] for _ in range(N+1)]
    deg = [0]*(N+1)
    for _ in range(M):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    # BFS from S
    dS = [-1]*(N+1)
    dS[S] = 0
    q = deque([S])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if dS[w] == -1:
                dS[w] = dS[u] + 1
                q.append(w)

    # BFS from T
    dT = [-1]*(N+1)
    dT[T] = 0
    q = deque([T])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if dT[w] == -1:
                dT[w] = dT[u] + 1
                q.append(w)

    L = dS[T]
    if L == -1:
        print(-1)
        return
    if L == 1:
        print(-1)
        return

    # Condition 1: exists vertex x != S,T on some shortest path with degree >= 3
    cond1 = False
    for v in range(1, N+1):
        if v == S or v == T:
            continue
        if dS[v] + dT[v] == L and deg[v] >= 3:
            cond1 = True
            break
    if cond1:
        print(L + 2)
        return

    # Condition 2: exists vertex y not on shortest path, adjacent to S or T, with degree >= 2
    cond2 = False
    # neighbors of S
    for w in adj[S]:
        if w == T:
            continue
        if dS[w] + dT[w] != L and deg[w] >= 2:
            cond2 = True
            break
    if not cond2:
        for w in adj[T]:
            if w == S:
                continue
            if dS[w] + dT[w] != L and deg[w] >= 2:
                cond2 = True
                break
    if cond2:
        print(L + 1)
        return

    # Otherwise
    print(L)

if __name__ == "__main__":
    solve()