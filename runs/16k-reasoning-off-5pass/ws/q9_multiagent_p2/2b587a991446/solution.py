import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        S = int(next(iterator))
        T = int(next(iterator))
    except StopIteration:
        return

    # Adjacency list
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Check if the graph is a tree
    # A connected graph with N vertices and N-1 edges is a tree.
    # The problem states the graph is connected.
    if M == N - 1:
        print("-1")
        return

    # If not a tree, we can always solve it.
    # Calculate shortest path distance between S and T using BFS
    dist = [-1] * (N + 1)
    dist[S] = 0
    queue = deque([S])
    
    while queue:
        u = queue.popleft()
        if u == T:
            break
        
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    d = dist[T]
    
    # Logic derived:
    # If S and T are adjacent (d == 1), we need 3 moves (move one aside, swap, move back).
    # If they are not adjacent (d > 1), we need 2 * d moves.
    # Note: If d == 1 and graph is not a tree, it's always possible in 3 moves.
    
    if d == 1:
        print(3)
    else:
        print(2 * d)

if __name__ == '__main__':
    solve()