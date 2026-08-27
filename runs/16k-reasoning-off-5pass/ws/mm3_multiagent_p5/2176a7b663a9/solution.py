import sys
import random
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def solve_brute(N, W, intervals, queries):
    # Build G
    adj = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i+1, N):
            Li, Ri = intervals[i]
            Lj, Rj = intervals[j]
            if Ri < Lj or Rj < Li:
                adj[i].append(j)
                adj[j].append(i)
    # Dijkstra for each query
    out = []
    import heapq
    for s, t in queries:
        s -= 1
        t -= 1
        if s == t:
            out.append(W[s])
            continue
        dist = [float('inf')] * N
        dist[s] = W[s]
        pq = [(W[s], s)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == t:
                break
            for v in adj[u]:
                nd = d + W[v]
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        out.append(int(dist[t]) if dist[t] != float('inf') else -1)
    return out

def solve_fast(N, W, intervals, queries):
    size = 2 * N + 2
    seg = [[] for _ in range(4 * size)]
    
    def insert(node, l, r, ql, qr, idx):
        if ql <= l and r <= qr:
            seg[node].append(idx)
            return
        mid = (l + r) // 2
        if ql <= mid:
            insert(node*2, l, mid, ql, qr, idx)
        if qr > mid:
            insert(node*2+1, mid+1, r, ql, qr, idx)
    
    for i, (L, R) in enumerate(intervals):
        insert(1, 1, size, L, R, i)
    
    parent = list(range(N))
    rank = [0] * N
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
    
    def traverse(node, l, r):
        if seg[node]:
            first = seg[node][0]
            for idx in seg[node][1:]:
                union(first, idx)
        if l == r:
            return
        mid = (l + r) // 2
        traverse(node*2, l, mid)
        traverse(node*2+1, mid+1, r)
    
    traverse(1, 1, size)
    
    h_comp = [find(i) for i in range(N)]
    comp_map = {}
    for c in h_comp:
        comp_map[c] = True
    num_h_comps = len(comp_map)
    
    comp_vertices = {}
    for i in range(N):
        c = h_comp[i]
        if c not in comp_vertices:
            comp_vertices[c] = []
        comp_vertices[c].append(i)
    
    if num_h_comps >= 2:
        comp_min = {}
        for c, verts in comp_vertices.items():
            comp_min[c] = min(W[v] for v in verts)
        
        out = []
        for s, t in queries:
            s -= 1
            t -= 1
            cs = h_comp[s]
            ct = h_comp[t]
            if cs != ct:
                out.append(W[s] + W[t])
            else:
                min_other = float('inf')
                for c, m in comp_min.items():
                    if c != cs:
                        min_other = min(min_other, m)
                out.append(W[s] + W[t] + int(min_other))
        return out
    
    left_neighbor = [-1] * N
    right_neighbor = [-1] * N
    
    R_size = 2 * N + 2
    
    seg_left = [(-1, -1)] * (4 * R_size)
    
    def seg_update(node, l, r, pos, idx, R_val):
        if l == r:
            if R_val > seg_left[node][0]:
                seg_left[node] = (R_val, idx)
            return
        mid = (l + r) // 2
        if pos <= mid:
            seg_update(node*2, l, mid, pos, idx, R_val)
        else:
            seg_update(node*2+1, mid+1, r, pos, idx, R_val)
        if seg_left[node*2][0] > seg_left[node*2+1][0]:
            seg_left[node] = seg_left[node*2]
        else:
            seg_left[node] = seg_left[node*2+1]
    
    def seg_query(node, l, r, ql, qr):
        if ql > r or qr < l:
            return (-1, -1)
        if ql <= l and r <= qr:
            return seg_left[node]
        mid = (l + r) // 2
        left = seg_query(node*2, l, mid, ql, qr)
        right = seg_query(node*2+1, mid+1, r, ql, qr)
        if left[0] > right[0]:
            return left
        return right
    
    intervals_by_L = {}
    for i, (L, R) in enumerate(intervals):
        if L not in intervals_by_L:
            intervals_by_L[L] = []
        intervals_by_L[L].append(i)
    
    for L_val in range(1, R_size):
        if L_val in intervals_by_L:
            for i in intervals_by_L[L_val]:
                res = seg_query(1, 1, R_size-1, 1, L_val-1)
                if res[1] != -1:
                    left_neighbor[i] = res[1]
        if L_val in intervals_by_L:
            for i in intervals_by_L[L_val]:
                _, R = intervals[i]
                seg_update(1, 1, R_size-1, R, i, R)
    
    seg_right = [(10**9, -1)] * (4 * R_size)
    
    def seg_update2(node, l, r, pos, idx, L_val):
        if l == r:
            if L_val < seg_right[node][0]:
                seg_right[node] = (L_val, idx)
            return
        mid = (l + r) // 2
        if pos <= mid:
            seg_update2(node*2, l, mid, pos, idx, L_val)
        else:
            seg_update2(node*2+1, mid+1, r, pos, idx, L_val)
        if seg_right[node*2][0] < seg_right[node*2+1][0]:
            seg_right[node] = seg_right[node*2]
        else:
            seg_right[node] = seg_right[node*2+1]
    
    def seg_query2(node, l, r, ql, qr):
        if ql > r or qr < l:
            return (10**9, -1)
        if ql <= l and r <= qr:
            return seg_right[node]
        mid = (l + r) // 2
        left = seg_query2(node*2, l, mid, ql, qr)
        right = seg_query2(node*2+1, mid+1, r, ql, qr)
        if left[0] < right[0]:
            return left
        return right
    
    intervals_by_R = {}
    for i, (L, R) in enumerate(intervals):
        if R not in intervals_by_R:
            intervals_by_R[R] = []
        intervals_by_R[R].append(i)
    
    for R_val in range(R_size-1, 0, -1):
        if R_val in intervals_by_R:
            for i in intervals_by_R[R_val]:
                res = seg_query2(1, 1, R_size-1, R_val+1, R_size-1)
                if res[1] != -1:
                    right_neighbor[i] = res[1]
        if R_val in intervals_by_R:
            for i in intervals_by_R[R_val]:
                L, _ = intervals[i]
                seg_update2(1, 1, R_size-1, L, i, L)
    
    parent_g = list(range(N))
    rank_g = [0] * N
    
    def find_g(x):
        while parent_g[x] != x:
            parent_g[x] = parent_g[parent_g[x]]
            x = parent_g[x]
        return x
    
    def union_g(x, y):
        px, py = find_g(x), find_g(y)
        if px == py:
            return
        if rank_g[px] < rank_g[py]:
            px, py = py, px
        parent_g[py] = px
        if rank_g[px] == rank_g[py]:
            rank_g[px] += 1
    
    for i in range(N):
        if left_neighbor[i] != -1:
            union_g(i, left_neighbor[i])
        if right_neighbor[i] != -1:
            union_g(i, right_neighbor[i])
    
    INF = 10**18
    best_left = [INF] * (2*N + 3)
    for i in range(N):
        L, R = intervals[i]
        if W[i] < best_left[R]:
            best_left[R] = W[i]
    for x in range(1, 2*N+2):
        if best_left[x-1] < best_left[x]:
            best_left[x] = best_left[x-1]
    
    def get_left_min(x):
        if x <= 1:
            return INF
        return best_left[x-1]
    
    best_right = [INF] * (2*N + 3)
    for i in range(N):
        L, R = intervals[i]
        if W[i] < best_right[L]:
            best_right[L] = W[i]
    for x in range(2*N, 0, -1):
        if best_right[x+1] < best_right[x]:
            best_right[x] = best_right[x+1]
    
    def get_right_min(x):
        if x >= 2*N:
            return INF
        return best_right[x+1]
    
    out = []
    for s, t in queries:
        s -= 1
        t -= 1
        if find_g(s) != find_g(t):
            out.append(-1)
            continue
        Ls, Rs = intervals[s]
        Lt, Rt = intervals[t]
        if Rs < Lt or Rt < Ls:
            out.append(W[s] + W[t])
        else:
            min_L = min(Ls, Lt)
            max_R = max(Rs, Rt)
            min_u = min(get_left_min(min_L), get_right_min(max_R))
            if min_u == INF:
                out.append(-1)
            else:
                out.append(W[s] + W[t] + min_u)
    return out

def test_random():
    for test_num in range(200):
        N = random.randint(2, 10)
        W = [random.randint(1, 20) for _ in range(N)]
        intervals = []
        for i in range(N):
            L = random.randint(1, 2*N)
            R = random.randint(L, 2*N)
            intervals.append((L, R))
        Q = random.randint(1, 15)
        queries = []
        for i in range(Q):
            s = random.randint(1, N)
            t = random.randint(1, N)
            while t == s:
                t = random.randint(1, N)
            queries.append((s, t))
        
        brute = solve_brute(N, W, intervals, queries)
        fast = solve_fast(N, W, intervals, queries)
        
        if brute != fast:
            print(f"MISMATCH on test {test_num}!")
            print("N=", N)
            print("W=", W)
            print("intervals=", intervals)
            print("queries=", queries)
            print("brute=", brute)
            print("fast=", fast)
            return False
    print("All tests passed!")
    return True

if __name__ == "__main__":
    # Read from stdin and solve
    N = int(input())
    W = list(map(int, input().split()))
    intervals = []
    for i in range(N):
        L, R = map(int, input().split())
        intervals.append((L, R))
    Q = int(input())
    queries = []
    for i in range(Q):
        s, t = map(int, input().split())
        queries.append((s, t))
    
    result = solve_fast(N, W, intervals, queries)
    for ans in result:
        print(ans)