import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))

    out_edges = [[] for _ in range(N)]
    in_edges = [[] for _ in range(N)]

    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        out_edges[u].append(v)
        in_edges[v].append(u)

    INF = 10**30
    dist = [INF] * (2 * N)

    # state id = 2 * vertex + parity
    # parity 0: original orientation
    # parity 1: reversed orientation
    start = 0
    dist[start] = 0
    heap = [(0, start)]

    heappush = heapq.heappush
    heappop = heapq.heappop
    target = N - 1

    while heap:
        d, state = heappop(heap)
        if d != dist[state]:
            continue

        v = state >> 1
        if v == target:
            sys.stdout.write(str(d) + "\n")
            return

        parity = state & 1

        # Reverse all edges at the current vertex.
        next_state = state ^ 1
        nd = d + X
        if nd < dist[next_state]:
            dist[next_state] = nd
            heappush(heap, (nd, next_state))

        # Move along one currently directed edge.
        nd = d + 1
        if parity == 0:
            for to in out_edges[v]:
                next_state = to << 1
                if nd < dist[next_state]:
                    dist[next_state] = nd
                    heappush(heap, (nd, next_state))
        else:
            for to in in_edges[v]:
                next_state = (to << 1) | 1
                if nd < dist[next_state]:
                    dist[next_state] = nd
                    heappush(heap, (nd, next_state))

    # The statement guarantees reachability, so this is only a fallback.
    ans = min(dist[target << 1], dist[(target << 1) | 1])
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()