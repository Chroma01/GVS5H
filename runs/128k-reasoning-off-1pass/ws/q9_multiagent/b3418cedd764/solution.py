import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(3000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = [0] * (N + 1)
        for i in range(1, N + 1):
            A[i] = int(next(iterator))
    except StopIteration:
        return

    MOD = 998244353

    # Build the graph structure
    # Original graph: i -> A[i] with constraint x_i <= x_{A[i]}
    # Reversed graph: A[i] -> i. 
    # In the reversed graph, we process from "leaves" (nodes with in-degree 0) up to the cycles.
    # in_degree[i] here counts how many j exist such that A[j] = i (incoming edges in reversed graph).
    
    rev_adj = [[] for _ in range(N + 1)]
    in_degree = [0] * (N + 1)
    
    for i in range(1, N + 1):
        u = A[i]
        rev_adj[u].append(i)
        in_degree[i] += 1

    # partial_dp[u][v] stores the number of ways to assign values to the subtree rooted at u 
    # (in the reversed graph) such that x_u = v, considering only the processed children.
    # Initially, for any node, if no children are processed, the product is 1.
    partial_dp = [[1] * (M + 1) for _ in range(N + 1)]
    
    # Queue for Kahn's algorithm on the reversed graph
    queue = []
    for i in range(1, N + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Process nodes in topological order (leaves of reversed trees up to cycles)
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        
        # u is fully processed. Its partial_dp[u] is complete.
        # Now update its parent p = A[u] in the reversed graph.
        # The parent in reversed graph is the node that points to u in reversed graph,
        # which corresponds to A[u] in the original definition (since edge is A[u] -> u).
        p = A[u]
        
        # Calculate contribution of u to p.
        # If x_p = v, then x_u <= v.
        # The number of valid assignments for u given x_u <= v is sum_{k=1}^v partial_dp[u][k].
        # We update partial_dp[p][v] by multiplying this sum.
        
        current_sum = 0
        for v in range(1, M + 1):
            current_sum = (current_sum + partial_dp[u][v]) % MOD
            partial_dp[p][v] = (partial_dp[p][v] * current_sum) % MOD
        
        # Decrement in-degree of parent
        in_degree[p] -= 1
        if in_degree[p] == 0:
            queue.append(p)
            
    # Nodes with in_degree > 0 form disjoint cycles.
    # For a cycle, all nodes must have the same value v because x_i <= x_{A[i]} implies equality around the cycle.
    # The number of ways for a cycle is sum_{v=1}^M ( product_{u in cycle} partial_dp[u][v] ).
    
    visited = [False] * (N + 1)
    total_ways = 0
    
    for i in range(1, N + 1):
        if in_degree[i] > 0 and not visited[i]:
            # Found a new cycle
            cycle_nodes = []
            curr = i
            while not visited[curr]:
                visited[curr] = True
                cycle_nodes.append(curr)
                curr = A[curr]
            
            # Calculate ways for this cycle
            cycle_ways = 0
            for v in range(1, M + 1):
                prod = 1
                for u in cycle_nodes:
                    prod = (prod * partial_dp[u][v]) % MOD
                cycle_ways = (cycle_ways + prod) % MOD
            
            total_ways = (total_ways + cycle_ways) % MOD
            
    print(total_ways)

if __name__ == '__main__':
    solve()