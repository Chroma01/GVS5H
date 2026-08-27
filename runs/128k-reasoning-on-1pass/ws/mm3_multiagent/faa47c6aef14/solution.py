import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    X = int(next(it)) - 1  # 0‑based index of the target box

    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    P = [int(next(it)) - 1 for _ in range(N)]
    Q = [int(next(it)) - 1 for _ in range(N)]

    # Build reverse edges for both colours
    revP = [[] for _ in range(N)]
    revQ = [[] for _ in range(N)]
    for i in range(N):
        revP[P[i]].append(i)
        revQ[Q[i]].append(i)

    # ---------- backward reachable from X ----------
    def bfs_back(start, rev):
        visited = [False] * N
        dq = deque([start])
        visited[start] = True
        while dq:
            v = dq.popleft()
            for u in rev[v]:
                if not visited[u]:
                    visited[u] = True
                    dq.append(u)
        return visited

    back_red = bfs_back(X, revP)
    back_blue = bfs_back(X, revQ)

    # Feasibility: every ball must be able to reach X
    for i in range(N):
        if i == X:
            continue
        if A[i] == 1 and not back_red[i]:
            print(-1)
            return
        if B[i] == 1 and not back_blue[i]:
            print(-1)
            return

    # ---------- forward from sources (stop when reaching X) ----------
    def bfs_fwd(sources, nxt):
        visited = [False] * N
        dq = deque()
        for s in sources:
            visited[s] = True
            dq.append(s)
        while dq:
            v = dq.popleft()
            if v == X:
                continue                # do not explore beyond X
            w = nxt[v]
            if not visited[w]:
                visited[w] = True
                dq.append(w)
        return visited

    red_sources = [i for i in range(N) if A[i] == 1 and i != X]
    blue_sources = [i for i in range(N) if B[i] == 1 and i != X]

    fwd_red = bfs_fwd(red_sources, P)
    fwd_blue = bfs_fwd(blue_sources, Q)

    # ---------- count required boxes ----------
    ans = 0
    for i in range(N):
        if i == X:
            continue
        if (fwd_red[i] and back_red[i]) or (fwd_blue[i] and back_blue[i]):
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()