import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
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

    # Build adjacency list
    # Vertices are 1-indexed
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # BFS Initialization
    # State is (pos_A, pos_B)
    # Start state: (S, T)
    # Target state: (T, S)
    
    start_state = (S, T)
    target_state = (T, S)
    
    # If start is already target (though problem says S != T, good to be safe)
    if start_state == target_state:
        print(0)
        return

    # Distance map: state -> distance
    # Using a dictionary for sparse storage to handle large N
    dist = {start_state: 0}
    queue = deque([start_state])
    
    found = False
    result = -1
    
    while queue:
        u, v = queue.popleft()
        current_dist = dist[(u, v)]
        
        # Try moving piece A
        for neighbor in adj[u]:
            if neighbor != v: # Cannot move to occupied vertex
                new_state = (neighbor, v)
                if new_state == target_state:
                    print(current_dist + 1)
                    return
                if new_state not in dist:
                    dist[new_state] = current_dist + 1
                    queue.append(new_state)
        
        # Try moving piece B
        for neighbor in adj[v]:
            if neighbor != u: # Cannot move to occupied vertex
                new_state = (u, neighbor)
                if new_state == target_state:
                    print(current_dist + 1)
                    return
                if new_state not in dist:
                    dist[new_state] = current_dist + 1
                    queue.append(new_state)
    
    # If queue is empty and target not reached
    print(-1)

if __name__ == '__main__':
    solve()