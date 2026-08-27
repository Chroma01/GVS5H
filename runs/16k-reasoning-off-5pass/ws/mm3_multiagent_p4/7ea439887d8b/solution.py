import sys
import heapq

def solve():
    import sys
    input = sys.stdin.readline
    N, M, X = map(int, input().split())
    adj_orig = [[] for _ in range(N+1)]
    adj_rev = [[] for _ in range(N+1)]
    for _ in range(M):
        u, v = map(int, input().split())
        adj_orig[u].append(v)
        adj_rev[v].append(u)
    
    INF = 10**30
    dist = [[INF, INF] for _ in range(N+1)]
    dist[1][0] = 0
    pq = [(0, 1, 0)]  # (cost, vertex, parity)
    while pq:
        d, v, p = heapq.heappop(pq)
        if d != dist[v][p]:
            continue
        # toggle operation
        np = 1 - p
        nd = d + X
        if nd < dist[v][np]:
            dist[v][np] = nd
            heapq.heappush(pq, (nd, v, np))
        # move operation
        if p == 0:
            # original orientation, move via adj_orig
            for to in adj_orig[v]:
                nd = d + 1
                if nd < dist[to][0]:
                    dist[to][0] = nd
                    heapq.heappush(pq, (nd, to, 0))
        else:
            # reversed orientation, move via adj_rev
            for to in adj_rev[v]:
                nd = d + 1
                if nd < dist[to][1]:
                    dist[to][1] = nd
                    heapq.heappush(pq, (nd, to, 1))
    
    ans = min(dist[N][0], dist[N][1])
    print(ans)

if __name__ == "__main__":
    solve()