import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300005)

def solve():
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
    degree = [0] * (N + 1)
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # BFS to find shortest path distance from S to all nodes
    dist_S = [-1] * (N + 1)
    dist_S[S] = 0
    queue = deque([S])
    
    while queue:
        u = queue.popleft()
        if u == T:
            break
        for v in adj[u]:
            if dist_S[v] == -1:
                dist_S[v] = dist_S[u] + 1
                queue.append(v)
    
    D = dist_S[T]
    
    # Since the graph is connected, D will not be -1 unless N=1 which is excluded by constraints (S!=T)
    if D == -1:
        print("-1")
        return

    # Case 1: D == 1 (Direct Edge)
    # If S and T are adjacent, the pieces block each other.
    # A swap is possible if and only if at least one of S or T has a neighbor other than the other piece.
    # If both are leaves connected only to each other, it's impossible.
    if D == 1:
        if degree[S] > 1 or degree[T] > 1:
            print(3)
        else:
            print("-1")
        return

    # Case 2: D > 1
    # If the shortest path distance is greater than 1, we can generally swap the pieces.
    # However, if the graph is effectively a simple line (path) between S and T with no side branches,
    # the pieces will block each other permanently.
    #
    # Conditions for possibility:
    # 1. S has degree > 1 (side branch at start)
    # 2. T has degree > 1 (side branch at end)
    # 3. There exists a node v on SOME shortest path with degree > 2 (side branch in middle)
    #
    # If none of these are true, the graph is a simple path between S and T, and it's impossible.
    
    possible = False
    
    # Check condition 1 and 2
    if degree[S] > 1 or degree[T] > 1:
        possible = True
    
    # Check condition 3 if not already possible
    if not possible:
        # We need to check if there is any node v with degree > 2 that lies on a shortest path.
        # A node v lies on a shortest path from S to T if dist_S[v] + dist_T[v] == D.
        # We need dist_T (distance from T).
        
        dist_T = [-1] * (N + 1)
        dist_T[T] = 0
        queue = deque([T])
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist_T[v] == -1:
                    dist_T[v] = dist_T[u] + 1
                    queue.append(v)
        
        for v in range(1, N + 1):
            if degree[v] > 2:
                if dist_S[v] != -1 and dist_T[v] != -1:
                    if dist_S[v] + dist_T[v] == D:
                        possible = True
                        break
    
    if possible:
        print(2 * D)
    else:
        print("-1")

if __name__ == '__main__':
    solve()