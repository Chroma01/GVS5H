import sys
import threading
import bisect

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    input = sys.stdin.readline
    
    N = int(input())
    W = list(map(int, input().split()))
    L = [0] * N
    R = [0] * N
    intervals = []
    for i in range(N):
        l, r = map(int, input().split())
        L[i] = l
        R[i] = r
        intervals.append((l, r, i))
    
    # Sort intervals by L, then by R
    intervals_by_L = sorted(intervals, key=lambda x: (x[0], x[1]))
    pos_in_L = [0] * N
    for idx, (l, r, i) in enumerate(intervals_by_L):
        pos_in_L[i] = idx
    
    # Sort intervals by R, then by L
    intervals_by_R = sorted(intervals, key=lambda x: (x[1], x[0]))
    pos_in_R = [0] * N
    for idx, (l, r, i) in enumerate(intervals_by_R):
        pos_in_R[i] = idx
    
    right_neighbor = [-1] * N
    left_neighbor = [-1] * N
    
    L_sorted_vals = [l for l, r, i in intervals_by_L]
    R_sorted_vals = [r for l, r, i in intervals_by_R]
    
    for i in range(N):
        idx = bisect.bisect_right(L_sorted_vals, R[i])
        if idx < N:
            right_neighbor[i] = intervals_by_L[idx][2]
        idx = bisect.bisect_left(R_sorted_vals, L[i]) - 1
        if idx >= 0:
            left_neighbor[i] = intervals_by_R[idx][2]
    
    adj = [[] for _ in range(N)]
    for i in range(N):
        if right_neighbor[i] != -1:
            j = right_neighbor[i]
            adj[i].append(j)
            adj[j].append(i)
        if left_neighbor[i] != -1:
            j = left_neighbor[i]
            adj[i].append(j)
            adj[j].append(i)
    
    parent = list(range(N))
    rank = [0] * N
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        x = find(x)
        y = find(y)
        if x == y:
            return
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1
    
    for i in range(N):
        if right_neighbor[i] != -1:
            union(i, right_neighbor[i])
        if left_neighbor[i] != -1:
            union(i, left_neighbor[i])
    
    LOG = (N).bit_length()
    up = [[-1] * N for _ in range(LOG)]
    depth = [0] * N
    sum_to_root = [0] * N
    visited = [False] * N
    
    def dfs(u, p, d, s):
        visited[u] = True
        up[0][u] = p if p != -1 else u
        depth[u] = d
        sum_to_root[u] = s
        for v in adj[u]:
            if v != p:
                dfs(v, u, d+1, s + W[v])
    
    for i in range(N):
        if not visited[i]:
            dfs(i, -1, 0, W[i])
    
    for k in range(1, LOG):
        for v in range(N):
            up[k][v] = up[k-1][up[k-1][v]]
    
    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        for k in range(LOG):
            if (diff >> k) & 1:
                u = up[k][u]
        if u == v:
            return u
        for k in range(LOG-1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]
        return up[0][u]
    
    def path_sum(u, v):
        w = lca(u, v)
        return sum_to_root[u] + sum_to_root[v] - 2 * sum_to_root[w] + W[w]
    
    Q = int(input())
    out = []
    for _ in range(Q):
        s, t = map(int, input().split())
        s -= 1
        t -= 1
        if find(s) != find(t):
            out.append("-1")
        else:
            out.append(str(path_sum(s, t)))
    print("\n".join(out))

if __name__ == "__main__":
    threading.Thread(target=main).start()