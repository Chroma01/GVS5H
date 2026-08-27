import sys
from collections import deque

def zero_one_bfs(adj, weights, N):
    dist = [float('inf')] * (N + 1)
    dist[1] = 0
    dq = deque([1])
    in_deq = [False] * (N + 1)
    in_deq[1] = True
    while dq:
        u = dq.popleft()
        in_deq[u] = False
        for v, ei in adj[u]:
            w = weights[ei]
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not in_deq[v]:
                    if w == 0:
                        dq.appendleft(v)
                    else:
                        dq.append(v)
                    in_deq[v] = True
    return dist[N]

def solve():
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    u = [0] * M
    v = [0] * M
    adj = [[] for _ in range(N + 1)]
    for i in range(M):
        u[i] = int(next(it))
        v[i] = int(next(it))
        adj[u[i]].append((v[i], i))
    
    # Meet-in-the-middle on edges
    mid = M // 2
    left_edges = list(range(mid))
    right_edges = list(range(mid, M))
    L = len(left_edges)
    R = len(right_edges)
    
    # For each left subset, compute distance and count
    left_best = [[-1] * (K + 1) for _ in range(1 << L)]  # too large, instead store per count
    # Actually, we only need for each count the max distance
    left_max = [-1] * (K + 1)
    for mask in range(1 << L):
        weights = [0] * M
        cnt = 0
        for i in range(L):
            if (mask >> i) & 1:
                weights[left_edges[i]] = 1
                cnt += 1
        if cnt > K:
            continue
        d = zero_one_bfs(adj, weights, N)
        if d > left_max[cnt]:
            left_max[cnt] = d
    
    # For right subsets
    right_max = [-1] * (K + 1)
    for mask in range(1 << R):
        weights = [0] * M
        cnt = 0
        for i in range(R):
            if (mask >> i) & 1:
                weights[right_edges[i]] = 1
                cnt += 1
        if cnt > K:
            continue
        d = zero_one_bfs(adj, weights, N)
        if d > right_max[cnt]:
            right_max[cnt] = d
    
    # Combine
    ans = 0
    for c in range(K + 1):
        if left_max[c] == -1 or right_max[K - c] == -1:
            continue
        total = left_max[c] + right_max[K - c]
        if total > ans:
            ans = total
    
    print(ans)

if __name__ == "__main__":
    solve()