import sys
from heapq import heappush, heappop


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, x = data[0], data[1], data[2]
    out_adj = [[] for _ in range(n + 1)]
    in_adj = [[] for _ in range(n + 1)]

    idx = 3
    for _ in range(m):
        u = data[idx]
        v = data[idx + 1]
        idx += 2
        out_adj[u].append(v)
        in_adj[v].append(u)

    INF = 1 << 62
    dist0 = [INF] * (n + 1)  # original orientation
    dist1 = [INF] * (n + 1)  # reversed orientation
    dist0[1] = 0

    pq = [(0, 1, 0)]  # (distance, vertex, parity)

    while pq:
        d, v, p = heappop(pq)

        if p == 0:
            if d != dist0[v]:
                continue

            nd = d + x
            if nd < dist1[v]:
                dist1[v] = nd
                heappush(pq, (nd, v, 1))

            nd = d + 1
            for to in out_adj[v]:
                if nd < dist0[to]:
                    dist0[to] = nd
                    heappush(pq, (nd, to, 0))
        else:
            if d != dist1[v]:
                continue

            nd = d + x
            if nd < dist0[v]:
                dist0[v] = nd
                heappush(pq, (nd, v, 0))

            nd = d + 1
            for to in in_adj[v]:
                if nd < dist1[to]:
                    dist1[to] = nd
                    heappush(pq, (nd, to, 1))

    ans = dist0[n] if dist0[n] < dist1[n] else dist1[n]
    sys.stdout.write(str(ans))


if __name__ == "__main__":
    main()