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

    # Target state: A at T, B at S
    target = (T, S)
    start = (S, T)

    if start == target:
        print(0)
        return

    # BFS on state space (u, v)
    # State: (pos_A, pos_B)
    # We cannot have pos_A == pos_B
    
    queue = deque()
    queue.append((start[0], start[1], 0))
    
    # Use a set for visited states to handle large N
    # Since N <= 2*10^5, N^2 is too big for array, but set is efficient enough
    # if the number of reachable states in shortest path is small.
    visited = set()
    visited.add(start)
    
    while queue:
        u, v, dist = queue.popleft()
        
        # Try moving piece A
        for next_u in adj[u]:
            if next_u == v:
                continue # Cannot land on same vertex as B
            
            new_state = (next_u, v)
            if new_state not in visited:
                if new_state == target:
                    print(dist + 1)
                    return
                visited.add(new_state)
                queue.append((next_u, v, dist + 1))
        
        # Try moving piece B
        for next_v in adj[v]:
            if next_v == u:
                continue # Cannot land on same vertex as A
            
            new_state = (u, next_v)
            if new_state not in visited:
                if new_state == target:
                    print(dist + 1)
                    return
                visited.add(new_state)
                queue.append((u, next_v, dist + 1))
                
    print(-1)

if __name__ == '__main__':
    solve()