import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(2000)

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
    # grid[i][j] is the character for edge i+1 -> j+1
    # We will use 0-based indexing internally
    grid = []
    for _ in range(N):
        grid.append(next(iterator))

    # Precompute adjacency lists for efficient lookups
    # adj[u][char] = list of v such that u -> v has label char
    # rev_adj[v][char] = list of u such that u -> v has label char
    # Since N is small (100), we can use a dictionary or list of lists.
    # Let's use lists of lists for 'a'-'z'.
    
    adj = [[[] for _ in range(26)] for _ in range(N)]
    rev_adj = [[[] for _ in range(26)] for _ in range(N)]

    for r in range(N):
        for c_idx, char in enumerate(grid[r]):
            if char != '-':
                u = r
                v = c_idx
                char_code = ord(char) - ord('a')
                adj[u][char_code].append(v)
                rev_adj[v][char_code].append(u)

    # Initialize distances
    # dist[u][v] stores the shortest palindrome path length from u to v
    # Initialize with infinity
    INF = float('inf')
    dist = [[INF] * N for _ in range(N)]

    # BFS Queue: stores (u, v, current_length)
    queue = deque()

    # 1. Odd length palindromes: Center is a vertex k.
    # Initial state: path k -> k with length 0.
    for i in range(N):
        dist[i][i] = 0
        queue.append((i, i, 0))

    # 2. Even length palindromes: Center is an edge u -> v with label c.
    # Initial state: path u -> v with length 1.
    for u in range(N):
        for c_idx, char in enumerate(grid[u]):
            if char != '-':
                v = c_idx
                # Check if we already found a shorter path (though 1 is minimal for non-zero)
                if dist[u][v] > 1:
                    dist[u][v] = 1
                    queue.append((u, v, 1))

    # BFS Execution
    while queue:
        u, v, d = queue.popleft()

        # Try to extend the palindrome by 2 characters
        # We need to find u' such that u' -> u has label c
        # And v' such that v -> v' has label c
        # Then new state is (u', v') with length d + 2
        
        # Optimization: Iterate over characters present in incoming edges to u
        # and outgoing edges from v.
        
        # Get possible characters for incoming to u
        incoming_chars = set()
        for c_idx in range(26):
            if rev_adj[u][c_idx]:
                incoming_chars.add(c_idx)
        
        # Get possible characters for outgoing from v
        outgoing_chars = set()
        for c_idx in range(26):
            if adj[v][c_idx]:
                outgoing_chars.add(c_idx)
        
        # Intersection of characters
        common_chars = incoming_chars & outgoing_chars
        
        for c_idx in common_chars:
            # Find u' such that u' -> u has char c_idx
            # Find v' such that v -> v' has char c_idx
            
            # We need to pick one u' and one v'.
            # To find the shortest path, we just need *any* valid u' and v'.
            # Wait, does the choice of u' and v' matter for the length?
            # The length is always d + 2 regardless of which specific edges we pick,
            # as long as they match the character.
            # However, we want to reach (u', v') with minimal d.
            # Since BFS guarantees minimal d for the current state (u, v),
            # any extension (u', v') will have length d+2.
            # We should update dist[u'][v'] if d+2 is smaller.
            
            # Get lists of candidates
            candidates_u = rev_adj[u][c_idx]
            candidates_v = adj[v][c_idx]
            
            # We need to update dist[u'][v'] for all combinations?
            # Yes, because different pairs (u', v') might be reached.
            # However, iterating all pairs might be O(N^2) per state, leading to O(N^4).
            # Is it necessary to iterate all pairs?
            # The state is (u', v'). We need to update dist[u'][v'].
            # If we have multiple u' and multiple v', we generate multiple states.
            # This is correct.
            
            for u_next in candidates_u:
                for v_next in candidates_v:
                    if dist[u_next][v_next] > d + 2:
                        dist[u_next][v_next] = d + 2
                        queue.append((u_next, v_next, d + 2))

    # Prepare output
    # Format: N lines, each with N integers separated by space
    output_lines = []
    for i in range(N):
        row_str = []
        for j in range(N):
            if dist[i][j] == INF:
                row_str.append("-1")
            else:
                row_str.append(str(dist[i][j]))
        output_lines.append(" ".join(row_str))
    
    print("\n".join(output_lines))

if __name__ == '__main__':
    solve()