import sys
import heapq

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        S = int(next(iterator))
        T = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # If M == N - 1, it's a tree.
    # In a tree, the path between S and T is unique.
    # If there is a vertex on this path (exclusive of S and T) with degree >= 3,
    # then one piece can move into the branch to let the other pass.
    # The cost is 2 * dist(S, T) + 2.
    # Otherwise, it's impossible to swap.
    if M == N - 1:
        # BFS from S to find path to T
        parent = [-1] * (N + 1)
        dist = [-1] * (N + 1)
        queue = [S]
        dist[S] = 0
        idx = 0
        while idx < len(queue):
            u = queue[idx]
            idx += 1
            if u == T:
                break
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    queue.append(v)
        
        if dist[T] == -1:
            print(-1)
            return

        # Reconstruct path
        path = []
        curr = T
        while curr != -1:
            path.append(curr)
            if curr == S:
                break
            curr = parent[curr]
        
        # Check intermediate vertices
        # path is [T, ..., S]
        # Intermediate are path[1:-1]
        possible = False
        for i in range(1, len(path) - 1):
            if len(adj[path[i]]) >= 3:
                possible = True
                break
        
        if possible:
            print(2 * dist[T] + 2)
        else:
            print(-1)
        return

    # General case: M >= N (contains at least one cycle)
    # Run BFS from S and T to get distances for heuristic
    def bfs(start_node):
        d = [-1] * (N + 1)
        d[start_node] = 0
        q = [start_node]
        idx = 0
        while idx < len(q):
            u = q[idx]
            idx += 1
            for v in adj[u]:
                if d[v] == -1:
                    d[v] = d[u] + 1
                    q.append(v)
        return d

    dist_S = bfs(S)
    dist_T = bfs(T)
    
    # A* Search
    # State: (u, v) representing A at u, B at v
    # g: cost so far (number of moves)
    # h: heuristic = dist_T[u] + dist_S[v] (minimum remaining moves)
    # f: g + h
    
    start_state = (S, T)
    target_state = (T, S)
    
    # Initial heuristic
    h_start = dist_T[S] + dist_S[T]
    
    # Priority queue stores (f, g, u, v)
    pq = [(h_start, 0, S, T)]
    
    # Best g found for each state to avoid processing suboptimal paths
    best_g = {start_state: 0}
    
    while pq:
        f, g, u, v = heapq.heappop(pq)
        
        # If we found a better path to this state already, skip
        if g > best_g.get((u, v), float('inf')):
            continue
        
        # Check if target reached
        if u == T and v == S:
            print(g)
            return
        
        # Expand neighbors for A (u)
        for nu in adj[u]:
            if nu == v:
                continue
            ng = g + 1
            nh = dist_T[nu] + dist_S[v]
            nf = ng + nh
            
            state = (nu, v)
            if ng < best_g.get(state, float('inf')):
                best_g[state] = ng
                heapq.heappush(pq, (nf, ng, nu, v))
        
        # Expand neighbors for B (v)
        for nv in adj[v]:
            if nv == u:
                continue
            ng = g + 1
            nh = dist_T[u] + dist_S[nv]
            nf = ng + nh
            
            state = (u, nv)
            if ng < best_g.get(state, float('inf')):
                best_g[state] = ng
                heapq.heappush(pq, (nf, ng, u, nv))

    print(-1)

if __name__ == '__main__':
    solve()