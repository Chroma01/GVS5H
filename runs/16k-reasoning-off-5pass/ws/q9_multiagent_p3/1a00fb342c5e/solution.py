import sys

# Increase recursion depth just in case, though we use iterative BFS
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

    # Build adjacency list
    # adj[u] contains tuples (v, w) representing A[u] ^ A[v] = w
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        adj[u].append((v, w))
        adj[v].append((u, w))

    # Array to store the values of A. Initialize with -1 to indicate unvisited.
    # We use 1-based indexing for convenience to match problem statement.
    A = [-1] * (N + 1)
    
    # Iterate through all nodes to handle disconnected components
    for i in range(1, N + 1):
        if A[i] != -1:
            continue
        
        # Start BFS for the new component
        # We assume A[i] = 0 initially for this component to establish relative values
        A[i] = 0
        queue = [i]
        component_nodes = []
        
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            component_nodes.append(u)
            
            for v, w in adj[u]:
                if A[v] == -1:
                    A[v] = A[u] ^ w
                    queue.append(v)
                else:
                    # Check consistency
                    if A[u] ^ A[v] != w:
                        print("-1")
                        return
        
        # Optimization step: Minimize sum for this component
        # We can flip the k-th bit for all nodes in the component if it reduces the count of 1s.
        # Since constraints are linear (XOR), flipping a bit for all nodes preserves A[u]^A[v].
        
        # Determine max bits needed. Z_i <= 10^9 < 2^30.
        # So bits 0 to 29 are sufficient.
        for bit in range(30):
            mask = 1 << bit
            count_set = 0
            for node in component_nodes:
                if (A[node] & mask):
                    count_set += 1
            
            total_nodes = len(component_nodes)
            # If more than half have the bit set, flip it for everyone
            if count_set > total_nodes - count_set:
                for node in component_nodes:
                    A[node] ^= mask

    # Output the result
    # A[1] to A[N]
    print(*(A[1:]))

if __name__ == '__main__':
    solve()