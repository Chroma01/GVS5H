import sys
import heapq

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, X = data[0], data[1], data[2]

    out = [[] for _ in range(N)]
    inc = [[] for _ in range(N)]

    idx = 3
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        out[u].append(v)
        inc[v].append(u)

    del data

    INF = 10**30
    dist = [INF] * (2 * N)
    dist[0] = 0

    heap = [(0, 0)]
    heappush = heapq.heappush
    heappop = heapq.heappop

    target = (N - 1) * 2

    while heap:
        d, s = heappop(heap)

        if d != dist[s]:
            continue

        if s >= target:
            print(d)
            return

        v = s >> 1

        if (s & 1) == 0:
            ns = s ^ 1
            nd = d + X
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))

            nd = d + 1
            for to in out[v]:
                ns = to << 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heappush(heap, (nd, ns))
        else:
            ns = s ^ 1
            nd = d + X
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))

            nd = d + 1
            for to in inc[v]:
                ns = (to << 1) | 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heappush(heap, (nd, ns))

    print(min(dist[target], dist[target + 1]))

if __name__ == "__main__":
    main()