import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))
    
    # adjacency lists: out[v] = list of u for edges v->u
    # inc[v] = list of u for edges u->v (incoming edges)
    out = [[] for _ in range(N + 1)]
    inc = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(next(it))
        v = int(next(it))
        out[u].append(v)
        inc[v].append(u)
    
    INF = 10**30
    # 2N states: state (v, 0) -> index 2*(v-1), state (v, 1) -> index 2*(v-1)+1
    dist = [INF] * (2 * N + 2)  # extra padding to avoid index issues
    # start: vertex 1, orientation 0 (original)
    start = 2 * (1 - 1)  # 0
    dist[start] = 0
    pq = [(0, start)]
    
    # helper to get vertex and orientation from state index
    # state = 2*(v-1) + orient  where orient 0 or 1
    while pq:
        d, state = heapq.heappop(pq)
        if d != dist[state]:
            continue
        v = state // 2 + 1
        orient = state % 2
        nd = d + 1
        if orient == 0:
            # move along original outgoing edges: v -> u, stay in orientation 0
            for u in out[v]:
                ns = 2 * (u - 1)
                if nd < dist[ns]:
                    dist[ns] = nd
                    heapq.heappush(pq, (nd, ns))
            # flip to orientation 1 at cost X
            f = d + X
            ns = state + 1  # same v, orient 1
            if f < dist[ns]:
                dist[ns] = f
                heapq.heappush(pq, (f, ns))
        else:
            # orientation 1: edges are reversed, so we move along original incoming edges
            # for each edge u -> v (original), in reversed graph we have v -> u
            for u in inc[v]:
                ns = 2 * (u - 1) + 1  # stay in orientation 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heapq.heappush(pq, (nd, ns))
            # flip back to orientation 0 at cost X
            f = d + X
            ns = state - 1  # same v, orient 0
            if f < dist[ns]:
                dist[ns] = f
                heapq.heappush(pq, (f, ns))
    
    ans = min(dist[2 * (N - 1)], dist[2 * (N - 1) + 1])
    print(ans)

if __name__ == "__main__":
    solve()