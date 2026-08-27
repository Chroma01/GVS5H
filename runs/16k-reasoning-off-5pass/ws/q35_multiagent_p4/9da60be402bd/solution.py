import sys
from collections import deque

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    # Adjacency lists
    # out_edges[u] = list of (v, char)
    # in_edges[v] = list of (u, char)
    out_edges = [[] for _ in range(N)]
    in_edges = [[] for _ in range(N)]
    
    # Also store adjacency by label for faster lookup
    # out_by_label[u][char] = list of v
    # in_by_label[v][char] = list of u
    out_by_label = [{} for _ in range(N)]
    in_by_label = [{} for _ in range(N)]

    for i in range(N):
        row_str = next(iterator)
        for j in range(N):
            c = row_str[j]
            if c != '-':
                # Edge from i to j with label c
                # Note: Input is 1-indexed in problem, but we use 0-indexed
                out_edges[i].append((j, c))
                in_edges[j].append((i, c))
                
                if c not in out_by_label[i]:
                    out_by_label[i][c] = []
                out_by_label[i][c].append(j)
                
                if c not in in_by_label[j]:
                    in_by_label[j][c] = []
                in_by_label[j][c].append(i)

    # dist[i][j] stores the shortest palindrome path length from i to j
    # Initialize with infinity
    INF = 10**9
    dist = [[INF] * N for _ in range(N)]
    
    queue = deque()

    # Base case 1: Empty path (length 0) is a palindrome for (i, i)
    for i in range(N):
        dist[i][i] = 0
        queue.append((i, i))

    # Base case 2: Single edge (length 1) is a palindrome for (u, v)
    for i in range(N):
        for j in range(N):
            c = None
            # Check if there is an edge i->j
            # We can iterate out_edges[i] or just check the input again
            # Since we have out_by_label, we can reconstruct or just iterate
            # Let's iterate out_edges for simplicity to set dist
            pass
            
    # Re-iterate to set single edge distances
    for i in range(N):
        for j, c in out_edges[i]:
            if dist[i][j] > 1:
                dist[i][j] = 1
                queue.append((i, j))

    # BFS
    while queue:
        u, v = queue.popleft()
        d = dist[u][v]
        
        # We want to extend the palindrome by adding a character c to the front (via incoming edge to v)
        # and a character c to the back (via outgoing edge from u).
        # New state will be (u_next, v_next) with distance d + 2.
        
        # Get all outgoing edges from u grouped by label
        u_out_labels = out_by_label[u]
        # Get all incoming edges to v grouped by label
        v_in_labels = in_by_label[v]
        
        # Find common labels
        common_labels = set(u_out_labels.keys()) & set(v_in_labels.keys())
        
        for c in common_labels:
            # For each u_next such that u -> u_next has label c
            for u_next in u_out_labels[c]:
                # For each v_next such that v_next -> v has label c
                for v_next in v_in_labels[c]:
                    if dist[u_next][v_next] > d + 2:
                        dist[u_next][v_next] = d + 2
                        queue.append((u_next, v_next))

    # Output results
    results = []
    for i in range(N):
        row = []
        for j in range(N):
            if dist[i][j] == INF:
                row.append("-1")
            else:
                row.append(str(dist[i][j]))
        results.append(" ".join(row))
    
    print("\n".join(results))

if __name__ == '__main__':
    solve()