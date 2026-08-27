import sys
from collections import deque

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    adj = [[] for _ in range(N)]
    # store edges to handle self-loops after building adjacency
    for _ in range(M):
        x = int(next(it)) - 1
        y = int(next(it)) - 1
        z = int(next(it))
        if x == y:
            if z != 0:
                print(-1)
                return
            # self-loop with z==0 gives no information, skip
            continue
        adj[x].append((y, z))
        adj[y].append((x, z))

    A = [0] * N
    visited = [False] * N
    MAX_BIT = 30  # because Z_i <= 1e9 < 2^30

    for start in range(N):
        if visited[start]:
            continue
        # BFS to collect component and compute two assignments
        comp = []
        q = deque([start])
        visited[start] = True
        # store values for each node in the component
        val0 = {start: 0}
        val1 = {start: (1 << MAX_BIT) - 1}  # all bits set to 1

        while q:
            u = q.popleft()
            comp.append(u)
            v0 = val0[u]
            v1 = val1[u]
            for (v, w) in adj[u]:
                w0 = v0 ^ w
                w1 = v1 ^ w
                if not visited[v]:
                    visited[v] = True
                    val0[v] = w0
                    val1[v] = w1
                    q.append(v)
                else:
                    if val0[v] != w0 or val1[v] != w1:
                        print(-1)
                        return

        # Determine which assignment gives smaller sum
        sum0 = 0
        sum1 = 0
        for node in comp:
            sum0 += val0[node]
            sum1 += val1[node]

        chosen = val0 if sum0 <= sum1 else val1
        for node in comp:
            A[node] = chosen[node]

    sys.stdout.write(' '.join(map(str, A)))

if __name__ == "__main__":
    solve()