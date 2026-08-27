import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    adj = [[] for _ in range(N)]
    edge_count = [0] * N
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
        edge_count[u] += 1
        edge_count[v] += 1
    color = [-1] * N
    components = []  # list of (A, B, edge_cnt)
    for i in range(N):
        if color[i] == -1:
            # BFS
            queue = deque([i])
            color[i] = 0
            cnt = [1, 0]  # counts for color 0 and 1
            edges = 0
            while queue:
                u = queue.popleft()
                for v in adj[u]:
                    edges += 1  # count each undirected edge once per endpoint
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        cnt[color[v]] += 1
                        queue.append(v)
                    # else: already colored, and graph is bipartite so no conflict
            # edges counted twice (once from each endpoint)
            edges //= 2
            A, B = cnt[0], cnt[1]
            components.append((A, B, edges))
    
    xor_sum = 0
    for A, B, e in components:
        missing = A * B - e
        xor_sum ^= missing
    
    if xor_sum != 0:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == "__main__":
    solve()