import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    grid = data[1:]
    # Build adjacency lists per vertex with label index
    out_edges = [[] for _ in range(N)]
    in_edges = [[] for _ in range(N)]
    for i in range(N):
        row = grid[i]
        for j in range(N):
            ch = row[j]
            if ch != '-':
                idx = ord(ch) - ord('a')
                out_edges[i].append((j, idx))
                in_edges[j].append((i, idx))
    
    # Precompute per label: out_by_label[c][u] = list of v with edge u->v label c
    #                    in_by_label[c][v] = list of u with edge u->v label c
    out_by_label = [[[] for _ in range(N)] for _ in range(26)]
    in_by_label = [[[] for _ in range(N)] for _ in range(26)]
    for c in range(26):
        for u in range(N):
            for (v, lab) in out_edges[u]:
                if lab == c:
                    out_by_label[c][u].append(v)
            for (u2, lab) in in_edges[u]:
                if lab == c:
                    in_by_label[c][u].append(u2)
    
    # Precompute whether edge v->j exists (for odd target generation)
    has_edge_to = [[False]*N for _ in range(N)]
    for u in range(N):
        for (v, lab) in out_edges[u]:
            has_edge_to[u][v] = True
    
    result = [[-1]*N for _ in range(N)]
    for i in range(N):
        result[i][i] = 0
    
    # For each target vertex j, run BFS on the reverse product graph starting from S_j
    for j in range(N):
        visited = [False] * (N * N)
        q = deque()
        dist_even = [-1] * N  # distance from (i, j) to (j, j) in product graph
        dist_odd = [-1] * N   # distance from (i, j) to (v, j) with edge v->j in product graph
        
        # Add even target state (j, j)
        s_even = j * N + j
        visited[s_even] = True
        q.append((s_even, 0, 0))  # (state_id, distance, target_type) 0=even, 1=odd
        
        # Add odd target states (v, j) for all v with an edge v->j
        for v in range(N):
            if has_edge_to[v][j]:
                s_odd = v * N + j
                if not visited[s_odd]:
                    visited[s_odd] = True
                    q.append((s_odd, 0, 1))
        
        # BFS on the reverse product graph
        # In reverse, from state (a, b) we can go to predecessor (x, y) if there is
        # a label c with edge x->a (label c) and edge b->y (label c).
        while q:
            s, d, typ = q.popleft()
            a = s // N
            b = s % N
            # If this state corresponds to a source (i, j) (i.e., second coordinate == j),
            # record the distance according to target type.
            if b == j:
                if typ == 0 and dist_even[a] == -1:
                    dist_even[a] = d
                elif typ == 1 and dist_odd[a] == -1:
                    dist_odd[a] = d
            # Generate all predecessor states
            for c in range(26):
                list_x = in_by_label[c][a]   # x such that x->a with label c
                list_y = out_by_label[c][b]  # y such that b->y with label c
                if not list_x or not list_y:
                    continue
                for x in list_x:
                    base = x * N
                    for y in list_y:
                        ns = base + y
                        if not visited[ns]:
                            visited[ns] = True
                            q.append((ns, d+1, typ))
        
        # Fill results for column j (i.e., pairs (i, j))
        for i in range(N):
            if i == j:
                continue
            best = -1
            if dist_even[i] != -1:
                best = 2 * dist_even[i]
            if dist_odd[i] != -1:
                odd_len = 2 * dist_odd[i] + 1
                if best == -1 or odd_len < best:
                    best = odd_len
            if best != -1:
                result[i][j] = best
    
    out_lines = []
    for i in range(N):
        out_lines.append(' '.join(str(result[i][j]) for j in range(N)))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()