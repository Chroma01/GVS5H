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

    # Read the graph
    # C[i][j] is the label of edge from i to j (0-indexed)
    # '-' means no edge
    graph = []
    for i in range(N):
        row_str = next(iterator)
        row = []
        for j in range(N):
            row.append(row_str[j])
        graph.append(row)

    # Initialize distances
    # dist[i][j] = shortest palindrome path length from i to j
    # Initialize with infinity
    INF = float('inf')
    dist = [[INF] * N for _ in range(N)]

    # Queue for BFS
    queue = deque()

    # Base case 1: Length 0 palindromes (i to i)
    for i in range(N):
        dist[i][i] = 0
        queue.append((i, i, 0))

    # Base case 2: Length 1 palindromes (edges)
    # An edge i -> j with any label is a palindrome of length 1
    for i in range(N):
        for j in range(N):
            if graph[i][j] != '-':
                if dist[i][j] > 1:
                    dist[i][j] = 1
                    queue.append((i, j, 1))

    # Precompute adjacency lists for incoming and outgoing edges grouped by character
    # incoming[u][c] = list of x such that x -> u has label c
    # outgoing[v][c] = list of y such that v -> y has label c
    
    incoming = [[[] for _ in range(26)] for _ in range(N)]
    outgoing = [[[] for _ in range(26)] for _ in range(N)]
    
    for i in range(N):
        for j in range(N):
            c_char = graph[i][j]
            if c_char != '-':
                idx = ord(c_char) - ord('a')
                outgoing[i][idx].append(j)
                incoming[j][idx].append(i)

    # BFS to find longer palindromes
    # We expand from the center outwards.
    # State (u, v) means we have a palindrome path from some start S to some end E
    # such that the path from S to u is the reverse of the path from v to E.
    # The current length is dist[u][v].
    # To extend, we look for an edge x -> u with label c and an edge v -> y with label c.
    # This forms a new palindrome from x to y with length dist[u][v] + 2.
    
    while queue:
        u, v, d = queue.popleft()
        
        # Try to extend by adding a character c to the front (edge x->u)
        # and the same character c to the back (edge v->y)
        
        # Iterate over all possible characters
        for c_idx in range(26):
            # Get all x such that x -> u has label c
            incoming_edges = incoming[u][c_idx]
            if not incoming_edges:
                continue
                
            # Get all y such that v -> y has label c
            outgoing_edges = outgoing[v][c_idx]
            if not outgoing_edges:
                continue
            
            # For each pair (x, y), update distance
            new_dist = d + 2
            for x in incoming_edges:
                for y in outgoing_edges:
                    if dist[x][y] > new_dist:
                        dist[x][y] = new_dist
                        queue.append((x, y, new_dist))

    # Prepare output
    results = []
    for i in range(N):
        row_res = []
        for j in range(N):
            if dist[i][j] == INF:
                row_res.append("-1")
            else:
                row_res.append(str(dist[i][j]))
        results.append(" ".join(row_res))
    
    print("\n".join(results))

if __name__ == '__main__':
    solve()