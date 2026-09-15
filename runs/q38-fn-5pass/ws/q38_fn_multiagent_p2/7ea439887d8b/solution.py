import sys
from heapq import heappush, heappop

def main():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    try:
        N = next(it)
    except StopIteration:
        return
    M = next(it)
    X = next(it)

    adj = [[] for _ in range(N)]
    radj = [[] for _ in range(N)]

    for _ in range(M):
        u = next(it) - 1
        v = next(it) - 1
        adj[u].append(v)
        radj[v].append(u)

    del it

    INF = 10**30
    dist = [INF] * (2 * N)
    dist[0] = 0

    heap = [(0, 0)]
    target_start = 2 * (N - 1)

    adj_l = adj
    radj_l = radj
    dist_l = dist
    X_l = X
    push = heappush
    pop = heappop

    while heap:
        d, s = pop(heap)
        if d != dist_l[s]:
            continue

        # The two target states are the last two state indices.
        if s >= target_start:
            sys.stdout.write(str(d))
            return

        v = s >> 1
        nd = d + 1

        if s & 1:
            # Reversed graph: outgoing edges are original incoming edges.
            for to in radj_l[v]:
                ns = (to << 1) | 1
                if nd < dist_l[ns]:
                    dist_l[ns] = nd
                    push(heap, (nd, ns))
        else:
            # Original graph.
            for to in adj_l[v]:
                ns = to << 1
                if nd < dist_l[ns]:
                    dist_l[ns] = nd
                    push(heap, (nd, ns))

        # Reverse all edges, toggling parity at the same vertex.
        ns = s ^ 1
        nd = d + X_l
        if nd < dist_l[ns]:
            dist_l[ns] = nd
            push(heap, (nd, ns))

    ans = dist_l[target_start]
    if dist_l[target_start + 1] < ans:
        ans = dist_l[target_start + 1]
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()