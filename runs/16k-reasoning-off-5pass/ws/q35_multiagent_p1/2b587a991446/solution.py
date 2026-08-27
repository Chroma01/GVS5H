import sys
from collections import deque

def solve():
    # Increase recursion depth just in case, though we use iterative BFS
    sys.setrecursionlimit(200005)
    
    # Read all input from stdin
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

    # Special case: if the graph is just a single edge between S and T
    # and there are no other nodes or edges, it's impossible.
    # More generally, if N=2 and M=1, it's impossible.
    if N == 2 and M == 1:
        print(-1)
        return

    # BFS on the product graph
    # State: (pos_A, pos_B)
    # Start: (S, T)
    # Target: (T, S)
    
    start_state = (S, T)
    target_state = (T, S)
    
    if start_state == target_state:
        print(0)
        return

    queue = deque()
    queue.append((start_state, 0))
    
    # Visited set to keep track of visited states
    # Using a set of tuples
    visited = set()
    visited.add(start_state)
    
    while queue:
        (u, v), dist = queue.popleft()
        
        # Try moving piece A
        for next_u in adj[u]:
            if next_u == v:
                continue # Cannot land on the same vertex as B
            
            new_state = (next_u, v)
            if new_state == target_state:
                print(dist + 1)
                return
            
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, dist + 1))
        
        # Try moving piece B
        for next_v in adj[v]:
            if next_v == u:
                continue # Cannot land on the same vertex as A
            
            new_state = (u, next_v)
            if new_state == target_state:
                print(dist + 1)
                return
            
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, dist + 1))
                
    # If queue is empty and target not reached
    print(-1)

if __name__ == '__main__':
    solve()