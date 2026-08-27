import sys

# Increase recursion depth just in case, though iterative BFS is used
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
    except StopIteration:
        return

    # Adjacency list for the graph
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Array to store the color (partition) of each vertex: 0 or 1
    # -1 indicates unvisited
    color = [-1] * (N + 1)
    
    total_moves = 0
    
    # Iterate over all vertices to handle disconnected components
    for i in range(1, N + 1):
        if color[i] == -1:
            # Start BFS for the current component
            q = [i]
            color[i] = 0
            
            idx = 0
            while idx < len(q):
                u = q[idx]
                idx += 1
                for v in adj[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        q.append(v)
            
            # Now calculate partition sizes for this component
            # q contains all nodes in the component
            c0 = 0
            c1 = 0
            for u in q:
                if color[u] == 0:
                    c0 += 1
                else:
                    c1 += 1
            
            # Count edges in this component
            # Sum of degrees of nodes in this component / 2
            current_edges = 0
            for u in q:
                current_edges += len(adj[u])
            current_edges //= 2
            
            max_edges = c0 * c1
            total_moves += (max_edges - current_edges)

    # The game is impartial and finite. The winner is determined by the parity of the total number of moves.
    # If total_moves is odd, the first player (Aoki) wins.
    # If total_moves is even, the second player (Takahashi) wins.
    if total_moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == '__main__':
    solve()