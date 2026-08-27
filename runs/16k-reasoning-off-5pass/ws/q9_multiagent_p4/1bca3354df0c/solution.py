import sys

# Increase recursion depth just in case, though iterative BFS is used below
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Build an adjacency list representation of the graph
    # Vertices are 1-indexed, so we use size N + 1
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Array to store the color (partition side) of each vertex
    # 0: unvisited, 1: left side, 2: right side
    color = [0] * (N + 1)
    
    total_max_edges = 0
    
    # Iterate over all vertices to handle disconnected components
    for i in range(1, N + 1):
        if color[i] == 0:
            # Start BFS for the current component
            queue = [i]
            color[i] = 1
            left_count = 0
            right_count = 0
            
            # Using a list as a queue for BFS
            head = 0
            while head < len(queue):
                u = queue[head]
                head += 1
                
                if color[u] == 1:
                    left_count += 1
                else:
                    right_count += 1
                
                for v in adj[u]:
                    if color[v] == 0:
                        color[v] = 3 - color[u] # Flip color: 1->2, 2->1
                        queue.append(v)
                    # If color[v] is already set, it must be different from color[u]
                    # because the problem guarantees no odd cycles initially.
                    # We don't need to check for conflicts.
            
            # The maximum number of edges in a bipartite graph with partitions of size L and R is L * R
            total_max_edges += left_count * right_count

    # The total number of moves available is the difference between max possible edges and current edges
    moves_available = total_max_edges - M
    
    # If moves_available is odd, the first player (Aoki) wins.
    # If moves_available is even, the second player (Takahashi) wins.
    if moves_available % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == '__main__':
    solve()