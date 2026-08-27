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

    # Parse the grid
    grid = []
    for _ in range(N):
        grid.append(next(iterator))

    # Precompute adjacency lists grouped by character
    # adj[char] will store list of (u, v) such that u -> v has label char
    # in_adj[char] will store list of (u, v) such that u -> v has label char (same structure)
    # We use this to quickly find incoming edges to a specific node with a specific label
    adj = {chr(ord('a') + i): [] for i in range(26)}
    in_adj = {chr(ord('a') + i): [] for i in range(26)}

    for i in range(N):
        for j in range(N):
            char = grid[i][j]
            if char != '-':
                adj[char].append((i, j))
                in_adj[char].append((i, j))

    # dist[i][j] stores the shortest palindrome path length from i to j
    # Initialize with -1 (representing infinity)
    dist = [[-1] * N for _ in range(N)]
    
    # Queue for BFS: stores tuples (u, v)
    q = deque()

    # Base Case 1: Empty palindrome (length 0)
    # Path from i to i is empty string, length 0
    for i in range(N):
        dist[i][i] = 0
        q.append((i, i))

    # Base Case 2: Single character palindromes (length 1)
    # Direct edges u -> v with label c
    for i in range(N):
        for j in range(N):
            if grid[i][j] != '-':
                # Only update if not already set (e.g., self-loop with length 1 is worse than 0)
                if dist[i][j] == -1:
                    dist[i][j] = 1
                    q.append((i, j))

    # BFS
    while q:
        u, v = q.popleft()
        current_len = dist[u][v]
        
        # Try to extend the palindrome
        # We need an edge x -> u with label c and v -> y with label c
        # Then we form a path x -> ... -> u -> ... -> v -> y
        # The new length is current_len + 2
        
        # Iterate over all possible characters
        for char_code in range(26):
            char = chr(ord('a') + char_code)
            
            # Find all x such that x -> u has label char
            # in_adj[char] contains (src, dest). We want src where dest == u
            incoming_to_u = [x for x, y in in_adj[char] if y == u]
            
            # Find all y such that v -> y has label char
            # adj[char] contains (src, dest). We want dest where src == v
            outgoing_from_v = [y for x, y in adj[char] if x == v]
            
            # If either list is empty, no extension possible for this char
            if not incoming_to_u or not outgoing_from_v:
                continue
                
            # Try all combinations
            for x in incoming_to_u:
                for y in outgoing_from_v:
                    if dist[x][y] == -1:
                        dist[x][y] = current_len + 2
                        q.append((x, y))

    # Output results
    output_lines = []
    for i in range(N):
        row_str = " ".join(map(str, dist[i]))
        output_lines.append(row_str)
    
    print("\n".join(output_lines))

if __name__ == '__main__':
    solve()