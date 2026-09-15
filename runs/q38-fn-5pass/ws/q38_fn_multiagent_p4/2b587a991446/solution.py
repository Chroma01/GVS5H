import sys
from collections import deque


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, S, T = data[0], data[1], data[2] - 1, data[3] - 1
    adj = [[] for _ in range(N)]
    idx = 4
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    del data

    def bfs_count(start):
        dist = [-1] * N
        ways = [0] * N
        dq = deque([start])
        dist[start] = 0
        ways[start] = 1

        while dq:
            u = dq.popleft()
            nd = dist[u] + 1
            wu = ways[u]
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = nd
                    ways[v] = wu
                    dq.append(v)
                elif dist[v] == nd:
                    if ways[v] < 2:
                        ways[v] += wu
                        if ways[v] > 2:
                            ways[v] = 2
        return dist, ways

    distS, ways = bfs_count(S)
    D = distS[T]

    # If there are at least two shortest S-T paths, the pieces can pass
    # while both move exactly D times.
    if ways[T] >= 2:
        print(2 * D)
        return

    def bfs_dist(start):
        dist = [-1] * N
        dq = deque([start])
        dist[start] = 0
        while dq:
            u = dq.popleft()
            nd = dist[u] + 1
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = nd
                    dq.append(v)
        return dist

    distT = bfs_dist(T)

    # Vertices on the unique shortest path.
    onP = [False] * N
    for i in range(N):
        if distS[i] + distT[i] == D:
            onP[i] = True

    INF = 10**18

    # Branch passing place.
    # A vertex with enough incident directions can let the two pieces pass.
    branch_extra = INF
    for v in range(N):
        if len(adj[v]) < 3:
            continue

        slack = distS[v] + distT[v] - D
        dvS = distS[v]
        dvT = distT[v]

        ports = 0
        for u in adj[v]:
            if distS[u] + 1 == dvS or distT[u] + 1 == dvT:
                ports += 1
                if ports >= 3:
                    break

        spare = 3 - ports
        if spare < 0:
            spare = 0

        extra = 2 * (slack + spare)
        if extra < branch_extra:
            branch_extra = extra

    del distT, ways

    # One-piece detour.
    # One piece follows the unique shortest path, the other takes an S-T walk.
    # Edge weight w = 1 + distS[u] - distS[v] is 0, 1, or 2.
    # Sum of weights on an S-T walk equals (walk length - D).
    dist0 = [INF] * N  # no positive-weight edge used yet
    dist1 = [INF] * N  # at least one positive-weight edge used
    dist0[S] = 0

    # Dial buckets for weights 0, 1, 2.
    b0 = deque([(S, 0, 0)])
    b1 = deque()
    b2 = deque()
    cur = 0
    cycle_extra = INF

    adj_l = adj
    onP_l = onP
    dS = distS
    S_l = S
    T_l = T

    while b0 or b1 or b2:
        found = False

        while b0:
            u, used, du = b0.popleft()

            # Should not happen with the bucket rotation, but keep it safe.
            if du != cur:
                if du == cur + 1:
                    b1.append((u, used, du))
                elif du == cur + 2:
                    b2.append((u, used, du))
                continue

            if used:
                if du != dist1[u]:
                    continue
            else:
                if du != dist0[u]:
                    continue

            if u == T_l:
                if used:
                    cycle_extra = du
                    found = True
                    break
                # Do not leave T before the end.
                continue

            for v in adj_l[u]:
                # Do not enter S after the start.
                if v == S_l:
                    continue

                # Do not move backward along the unique shortest path.
                if onP_l[u] and onP_l[v] and dS[v] < dS[u]:
                    continue

                w = 1 + dS[u] - dS[v]
                nd = du + w
                nused = used | (1 if w else 0)

                if nused:
                    if nd < dist1[v]:
                        dist1[v] = nd
                        if nd == cur:
                            b0.append((v, 1, nd))
                        elif nd == cur + 1:
                            b1.append((v, 1, nd))
                        else:
                            b2.append((v, 1, nd))
                else:
                    if nd < dist0[v]:
                        dist0[v] = nd
                        if nd == cur:
                            b0.append((v, 0, nd))
                        elif nd == cur + 1:
                            b1.append((v, 0, nd))
                        else:
                            b2.append((v, 0, nd))

        if found:
            break

        cur += 1
        b0, b1, b2 = b1, b2, b0

    best = cycle_extra if cycle_extra < branch_extra else branch_extra

    if best >= INF:
        print(-1)
    else:
        print(2 * D + best)


if __name__ == "__main__":
    solve()