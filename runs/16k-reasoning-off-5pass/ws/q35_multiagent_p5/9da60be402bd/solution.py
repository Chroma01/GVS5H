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

    # Adjacency lists:
    # outgoing[c][u] = list of v such that there is an edge u->v with label c
    # incoming[c][v] = list of u such that there is an edge u->v with label c
    # Labels are 'a' to 'z'. We'll map them to 0-25.
    outgoing = [[] for _ in range(26)]
    incoming = [[] for _ in range(26)]
    
    # Initialize outgoing and incoming as lists of lists for each vertex
    # Actually, let's make them: outgoing[c][u] is a list
    outgoing = [[[] for _ in range(N)] for _ in range(26)]
    incoming = [[[] for _ in range(N)] for _ in range(26)]
    
    # Read the graph
    for i in range(N):
        row_str = next(iterator)
        for j in range(N):
            c = row_str[j]
            if c != '-':
                u = i
                v = j
                label_idx = ord(c) - ord('a')
                outgoing[label_idx][u].append(v)
                incoming[label_idx][v].append(u)

    # dist[i][j] = shortest palindrome path length from i to j
    # Initialize with infinity
    INF = float('inf')
    dist = [[INF] * N for _ in range(N)]
    
    # Queue for BFS
    queue = deque()
    
    # Base case 1: Length 0 paths (i -> i)
    for i in range(N):
        dist[i][i] = 0
        queue.append((i, i))
        
    # Base case 2: Length 1 paths (i -> j with edge)
    for u in range(N):
        for v in range(N):
            if u == v:
                continue
            # Check if there is an edge u->v
            # We can iterate over all labels to find if any edge exists
            # Or better, we already have the graph structure.
            # Let's just check all labels for edge u->v
            for label_idx in range(26):
                if v in outgoing[label_idx][u]:
                    if dist[u][v] > 1:
                        dist[u][v] = 1
                        queue.append((u, v))
                    break # Found an edge, no need to check other labels for this pair

    # BFS
    while queue:
        u, v = queue.popleft()
        d = dist[u][v]
        
        # We want to extend the palindrome from (u, v) to (x, y)
        # such that there is an edge x->u with label c and v->y with label c.
        # The new path will be from x to y with length d + 2.
        
        # Iterate over all possible labels c
        for label_idx in range(26):
            # Find all x such that x -> u has label c
            # These are in incoming[label_idx][u]
            sources = incoming[label_idx][u]
            if not sources:
                continue
                
            # Find all y such that v -> y has label c
            # These are in outgoing[label_idx][v]
            destinations = outgoing[label_idx][v]
            if not destinations:
                continue
                
            new_d = d + 2
            for x in sources:
                for y in destinations:
                    if new_d < dist[x][y]:
                        dist[x][y] = new_d
                        queue.append((x, y))

    # Output the results
    output_lines = []
    for i in range(N):
        row = []
        for j in range(N):
            if dist[i][j] == INF:
                row.append("-1")
            else:
                row.append(str(dist[i][j]))
        output_lines.append(" ".join(row))
    
    print("\n".join(output_lines))

if __name__ == '__main__':
    solve()