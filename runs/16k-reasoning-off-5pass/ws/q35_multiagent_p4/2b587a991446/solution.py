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

    # BFS on the product graph
    # State: (pos_A, pos_B)
    # Start: (S, T)
    # Target: (T, S)
    
    start_state = (S, T)
    target_state = (T, S)
    
    if start_state == target_state:
        print(0)
        return

    # Visited set to store (u, v)
    visited = set()
    visited.add(start_state)
    
    queue = deque()
    queue.append((S, T, 0))
    
    while queue:
        u, v, dist = queue.popleft()
        
        # Try moving piece A from u to neighbor u_next
        # Piece B stays at v
        for u_next in adj[u]:
            if u_next == v:
                continue
            new_state = (u_next, v)
            if new_state == target_state:
                print(dist + 1)
                return
            if new_state not in visited:
                visited.add(new_state)
                queue.append((u_next, v, dist + 1))
        
        # Try moving piece B from v to neighbor v_next
        # Piece A stays at u
        for v_next in adj[v]:
            if v_next == u:
                continue
            new_state = (u, v_next)
            if new_state == target_state:
                print(dist + 1)
                return
            if new_state not in visited:
                visited.add(new_state)
                queue.append((u, v_next, dist + 1))
                
    # If queue is exhausted and target not reached
    print(-1)

if __name__ == '__main__':
    solve()