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
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    MOD = 998244353

    # Build the reversed graph (children)
    # In the original graph, edges are i -> A[i]-1 (0-indexed).
    # The constraint is x[i] <= x[A[i]-1].
    # In the reversed graph R, edges are A[i]-1 -> i.
    # R_adj[u] will contain all v such that A[v] == u+1.
    R_adj = [[] for _ in range(N)]
    out_degree_R = [0] * N
    
    for i in range(N):
        parent = A[i] - 1
        R_adj[parent].append(i)
        out_degree_R[parent] += 1
        
    # Initialize S[u][v]
    # S[u][v] represents the number of ways to assign values to the subtree rooted at u (in R)
    # such that x[u] <= v.
    # For leaves in R (nodes with no outgoing edges in R, i.e., not appearing in A),
    # the subtree is just the node itself. If x[u] = k, there is 1 way.
    # So S[u][v] = sum_{k=1}^v 1 = v.
    # For non-leaves, S[u][v] = product_{c in children(u)} S[c][v].
    
    # We initialize S[u] with 1s (identity for multiplication) and then set leaves.
    S = [[1] * (M + 1) for _ in range(N)]
    
    # Identify leaves in R (out_degree_R == 0)
    leaves = [i for i in range(N) if out_degree_R[i] == 0]
    
    # Set S for leaves
    for u in leaves:
        for v in range(1, M + 1):
            S[u][v] = v
            
    # Topological Sort (Kahn's algorithm) on R
    # Process nodes from leaves up to the cycle nodes.
    Q = leaves[:]
    
    # We need to track out_degree_R to know when a node becomes a leaf
    # Note: out_degree_R was computed in the first step.
    
    while Q:
        u = Q.pop()
        p = A[u] - 1  # Parent of u in R
        
        # Update S[p] by multiplying with S[u]
        # S[p][v] = S[p][v] * S[u][v]
        for v in range(1, M + 1):
            S[p][v] = (S[p][v] * S[u][v]) % MOD
            
        out_degree_R[p] -= 1
        if out_degree_R[p] == 0:
            Q.append(p)
            
    # After topological sort, nodes with out_degree_R > 0 are part of cycles.
    # In a functional graph, these form the cycles.
    # For a cycle node u, S[u][v] currently holds the product of S[c][v] for all 
    # tree children c (since cycle children were never processed).
    # This is exactly the number of ways to fill the tree attached to u given x[u] <= v.
    
    total_ans = 0
    visited_cycle = [False] * N
    
    for i in range(N):
        if out_degree_R[i] > 0 and not visited_cycle[i]:
            # Found a new cycle component
            cycle_nodes = []
            curr = i
            
            # Traverse the cycle
            while not visited_cycle[curr]:
                visited_cycle[curr] = True
                cycle_nodes.append(curr)
                curr = A[curr] - 1
                if curr == i:
                    break
            
            # Calculate the product of S[u][v] for all u in the cycle
            # P[v] = product_{u in cycle} S[u][v]
            P = [1] * (M + 1)
            for u in cycle_nodes:
                for v in range(1, M + 1):
                    P[v] = (P[v] * S[u][v]) % MOD
            
            # Sum P[v] for v from 1 to M
            comp_ans = sum(P[1:]) % MOD
            total_ans = (total_ans + comp_ans) % MOD

    print(total_ans)

if __name__ == '__main__':
    solve()