import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    # Using sys.stdin.read().split() handles all whitespace (newlines, spaces) automatically
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    # Parse the grid
    # The grid consists of N strings. 
    # Note: split() splits by whitespace, so each row string is an element.
    grid = []
    for _ in range(N):
        try:
            row = next(iterator)
            grid.append(row)
        except StopIteration:
            break

    # Precompute adjacency lists
    # adj[u][char] = list of v such that u -> v has char
    # rev_adj[v][char] = list of u such that u -> v has char
    # Using ord(c) - ord('a') as index 0-25
    adj = [[[] for _ in range(26)] for _ in range(N)]
    rev_adj = [[[] for _ in range(26)] for _ in range(N)]

    for r in range(N):
        # Ensure row length is N, though problem constraints imply valid input
        row_str = grid[r]
        for c in range(N):
            char = row_str[c]
            if char != '-':
                u = r
                v = c
                idx = ord(char) - ord('a')
                adj[u][idx].append(v)
                rev_adj[v][idx].append(u)

    # Initialize distances
    # dist[i][j] stores the shortest palindrome length from i to j
    # Initialize with -1 (representing infinity/unvisited)
    dist = [[-1] * N for _ in range(N)]

    # Base cases
    # 1. Length 0: Path from i to i is empty string (palindrome)
    for i in range(N):
        dist[i][i] = 0

    # 2. Length 1: Direct edges
    # We will collect these in a queue for odd lengths
    odd_queue = []
    
    for r in range(N):
        for c in range(N):
            if grid[r][c] != '-':
                dist[r][c] = 1
                odd_queue.append((r, c))
    
    # Prepare queues
    # even_queue: list of (u, v) representing palindromes of even length
    even_queue = [(i, i) for i in range(N)]
    
    # BFS Loop
    # We alternate processing even and odd lengths.
    # Even length L -> generates Even length L+2
    # Odd length L -> generates Odd length L+2 (which is L+2, so still odd parity relative to start? No.)
    # Wait:
    # Start:
    #   Even: (i, i) len 0.
    #   Odd: (u, v) len 1.
    # Step 1:
    #   Process Even (len 0) -> add to Even (len 2)
    #   Process Odd (len 1) -> add to Odd (len 3)
    # Step 2:
    #   Process Even (len 2) -> add to Even (len 4)
    #   Process Odd (len 3) -> add to Odd (len 5)
    # So we maintain two queues and process them in rounds.
    
    while even_queue or odd_queue:
        # Process Even Queue
        if even_queue:
            next_even = []
            # All states in the current even_queue have the same length
            # We can get it from any element, e.g., dist[u][v]
            # However, to be safe and explicit, we can track it or just read it.
            # Since we only add if dist was -1, and we set it to current + 2, 
            # all elements in next_even will have same length.
            # But elements in current even_queue might have different lengths if we mixed them?
            # No, we process layer by layer.
            # Let's verify: initially all 0. Then all 2. Then all 4.
            # So yes, they are uniform.
            current_len = dist[even_queue[0][0]][even_queue[0][1]]
            
            for u, v in even_queue:
                # Try to extend with character c
                # We need incoming to u with c, and outgoing from v with c
                # Logic: We have palindrome P from u to v.
                # We want to form palindrome c + P + c from x to y.
                # So we need edge x -> u with char c, and edge v -> y with char c.
                # Then new state is (x, y) with length current_len + 2.
                
                for c_idx in range(26):
                    # Find x such that x -> u has char c_idx
                    for x in rev_adj[u][c_idx]:
                        # Find y such that v -> y has char c_idx
                        for y in adj[v][c_idx]:
                            if dist[x][y] == -1:
                                dist[x][y] = current_len + 2
                                next_even.append((x, y))
            
            even_queue = next_even

        # Process Odd Queue
        if odd_queue:
            next_odd = []
            current_len = dist[odd_queue[0][0]][odd_queue[0][1]]
            
            for u, v in odd_queue:
                for c_idx in range(26):
                    for x in rev_adj[u][c_idx]:
                        for y in adj[v][c_idx]:
                            if dist[x][y] == -1:
                                dist[x][y] = current_len + 2
                                next_odd.append((x, y))
            
            odd_queue = next_odd

    # Output results
    output_lines = []
    for i in range(N):
        line = " ".join(map(str, dist[i]))
        output_lines.append(line)
    
    print("\n".join(output_lines))

if __name__ == '__main__':
    solve()