import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    grid = input_data[1:]
    
    # Build edge data structures
    # in_by_label[c][v] = list of u such that there is an edge u->v with label c
    in_by_label = [[[] for _ in range(N)] for _ in range(26)]
    # edge_exists[u][v] = True if there is an edge from u to v
    edge_exists = [[False]*N for _ in range(N)]
    
    idx = 0
    for i in range(N):
        row = grid[idx]
        idx += 1
        for j in range(N):
            ch = row[j]
            if ch != '-':
                c = ord(ch) - ord('a')
                in_by_label[c][j].append(i)
                edge_exists[i][j] = True
    
    INF = 10**9
    # dist_even[u*N + v] = shortest number of product-graph steps from (u,v) to some (x,x)
    dist_even = [INF] * (N * N)
    # dist_odd[u*N + v] = shortest number of product-graph steps from (u,v) to some (x,y) with edge x->y
    dist_odd = [INF] * (N * N)
    
    # Initialize BFS queues
    q_even = deque()
    q_odd = deque()
    
    # Even accepting states: (u,u)
    for u in range(N):
        node = u * N + u
        dist_even[node] = 0
        q_even.append(node)
    
    # Odd accepting states: (u,v) where edge u->v exists
    for u in range(N):
        for v in range(N):
            if edge_exists[u][v]:
                node = u * N + v
                dist_odd[node] = 0
                q_odd.append(node)
    
    # BFS for even accepting states
    while q_even:
        node = q_even.popleft()
        u = node // N
        v = node % N
        d = dist_even[node]
        for c in range(26):
            list_u = in_by_label[c][u]
            list_v = in_by_label[c][v]
            if not list_u or not list_v:
                continue
            for x in list_u:
                base = x * N
                for y in list_v:
                    new_node = base + y
                    if dist_even[new_node] == INF:
                        dist_even[new_node] = d + 1
                        q_even.append(new_node)
    
    # BFS for odd accepting states
    while q_odd:
        node = q_odd.popleft()
        u = node // N
        v = node % N
        d = dist_odd[node]
        for c in range(26):
            list_u = in_by_label[c][u]
            list_v = in_by_label[c][v]
            if not list_u or not list_v:
                continue
            for x in list_u:
                base = x * N
                for y in list_v:
                    new_node = base + y
                    if dist_odd[new_node] == INF:
                        dist_odd[new_node] = d + 1
                        q_odd.append(new_node)
    
    # Compute answers
    ans = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i == j:
                ans[i][j] = 0
                continue
            node = i * N + j
            best = INF
            if dist_even[node] != INF:
                best = min(best, 2 * dist_even[node])
            if dist_odd[node] != INF:
                best = min(best, 2 * dist_odd[node] + 1)
            ans[i][j] = -1 if best == INF else best
    
    out_lines = []
    for i in range(N):
        out_lines.append(' '.join(str(ans[i][j]) for j in range(N)))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()