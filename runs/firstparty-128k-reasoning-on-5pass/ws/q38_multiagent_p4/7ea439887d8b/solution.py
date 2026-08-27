import sys
from heapq import heappush, heappop

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, X = data[0], data[1], data[2]

    adj = [[] for _ in range(N)]
    radj = [[] for _ in range(N)]

    idx = 3
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        adj[u].append(v)
        radj[v].append(u)

    del data

    INF = 10 ** 30
    dist = [INF] * (2 * N)
    dist[0] = 0

    heap = [(0, 0)]
    target = N - 1

    while heap:
        d, s = heappop(heap)
        if d != dist[s]:
            continue

        v = s >> 1
        if v == target:
            sys.stdout.write(str(d) + "\n")
            return

        base = v << 1

        if (s & 1) == 0:
            nd = d + 1
            for to in adj[v]:
                ns = to << 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heappush(heap, (nd, ns))

            ns = base | 1
            nd = d + X
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))
        else:
            nd = d + 1
            for to in radj[v]:
                ns = (to << 1) | 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heappush(heap, (nd, ns))

            ns = base
            nd = d + X
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))

    ans = min(dist[target << 1], dist[(target << 1) | 1])
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()