import sys
from heapq import heappush, heappop


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, X = data[0], data[1], data[2]

    adj = [[] for _ in range(N)]
    rev = [[] for _ in range(N)]

    idx = 3
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        adj[u].append(v)
        rev[v].append(u)

    del data

    target = 2 * (N - 1)
    INF = 10**18

    dist = [INF] * (2 * N)
    dist[0] = 0

    heap = [(0, 0)]
    push = heappush
    pop = heappop

    while heap:
        d, s = pop(heap)
        if d != dist[s]:
            continue

        # States for vertex N-1 are exactly 2*(N-1) and 2*(N-1)+1.
        if s >= target:
            sys.stdout.write(str(d) + "\n")
            return

        v = s >> 1
        nd = d + 1

        if s & 1:
            # Reversed orientation: can traverse original incoming edges.
            for to in rev[v]:
                ns = (to << 1) | 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    push(heap, (nd, ns))

            # Reverse all edges.
            ns = s ^ 1
            nd2 = d + X
            if nd2 < dist[ns]:
                dist[ns] = nd2
                push(heap, (nd2, ns))
        else:
            # Original orientation: can traverse original outgoing edges.
            for to in adj[v]:
                ns = to << 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    push(heap, (nd, ns))

            # Reverse all edges.
            ns = s ^ 1
            nd2 = d + X
            if nd2 < dist[ns]:
                dist[ns] = nd2
                push(heap, (nd2, ns))

    ans = dist[target] if dist[target] < dist[target + 1] else dist[target + 1]
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()