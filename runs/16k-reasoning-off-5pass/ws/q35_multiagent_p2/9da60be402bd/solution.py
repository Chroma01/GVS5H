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

    # Read the grid
    grid = []
    for _ in range(N):
        grid.append(next(iterator))

    # Precompute adjacency lists for incoming and outgoing edges by character
    # incoming[u][char] = list of vertices x such that x -> u has label char
    # outgoing[v][char] = list of vertices y such that v -> y has label char
    incoming = [[[] for _ in range(26)] for _ in range(N)]
    outgoing = [[[] for _ in range(26)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            c_char = grid[i][j]
            if c_char != '-':
                idx = ord(c_char) - ord('a')
                outgoing[i][idx].append(j)
                incoming[j][idx].append(i)

    # dist[i][j] stores the shortest palindrome path length from i to j
    # Initialize with infinity
    INF = float('inf')
    dist = [[INF] * N for _ in range(N)]
    
    queue = deque()

    # Base case 1: Length 0 paths (i -> i)
    for i in range(N):
        dist[i][i] = 0
        queue.append((i, i))

    # Base case 2: Length 1 paths (i -> j with single edge)
    for i in range(N):
        for j in range(N):
            c_char = grid[i][j]
            if c_char != '-':
                if dist[i][j] > 1:
                    dist[i][j] = 1
                    queue.append((i, j))

    # BFS Expansion
    # We expand from the center outwards.
    # If we have a palindrome path from u to v of length L,
    # we can form a palindrome path from x to y of length L+2
    # if there is an edge x->u with label c and v->y with label c.
    
    while queue:
        u, v = queue.popleft()
        current_dist = dist[u][v]
        next_dist = current_dist + 2
        
        # If next_dist is already worse than what we might find elsewhere, 
        # we can skip if we are not careful, but BFS guarantees minimal first visit.
        # However, we only process if we haven't visited (x,y) yet.
        
        # Iterate over all possible characters
        for char_idx in range(26):
            # Get incoming neighbors of u with this character
            x_list = incoming[u][char_idx]
            if not x_list:
                continue
            
            # Get outgoing neighbors of v with this character
            y_list = outgoing[v][char_idx]
            if not y_list:
                continue
            
            # For each pair (x, y), update distance
            for x in x_list:
                for y in y_list:
                    if dist[x][y] == INF:
                        dist[x][y] = next_dist
                        queue.append((x, y))

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