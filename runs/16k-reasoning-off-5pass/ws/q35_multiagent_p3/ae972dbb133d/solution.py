import sys

# Increase recursion depth just in case, though we will use iterative BFS/DFS
sys.setrecursionlimit(2000000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        T = int(next(iterator))
    except StopIteration:
        return

    MOD = 998244353

    results = []

    for _ in range(T):
        try:
            H = int(next(iterator))
            W = int(next(iterator))
        except StopIteration:
            break
            
        grid = []
        for _ in range(H):
            grid.append(next(iterator))

        # Count A tiles and identify rows/cols with A
        count_A = 0
        row_has_A = [False] * H
        col_has_A = [False] * W

        for r in range(H):
            row_str = grid[r]
            for c in range(W):
                if row_str[c] == 'A':
                    count_A += 1
                    row_has_A[r] = True
                    col_has_A[c] = True

        # If no A tiles, then all are B.
        # If all are B, we need R_i != C_j for all i,j.
        # This implies R_i must be constant? No.
        # If all are B, then for any i, j: R_i != C_j.
        # This means if there is at least one B in row i, then C_j must be !R_i for all j.
        # This implies all C_j must be equal to !R_i.
        # So either (R_i=1 for all i, C_j=0 for all j) or (R_i=0 for all i, C_j=1 for all j).
        # But wait, if there are no A tiles, we still have the constraint that R_i is constant per row and C_j per col.
        # Let's stick to the general algorithm.

        I_A = [i for i in range(H) if row_has_A[i]]
        J_A = [j for j in range(W) if col_has_A[j]]
        
        U_R = [i for i in range(H) if not row_has_A[i]]
        U_C = [j for j in range(W) if not col_has_A[j]]

        # Check for B tiles in I_A x J_A
        # If any B exists there, return 0
        # We can check this efficiently by iterating over B tiles or checking grid
        # Since HW <= 10^6, we can iterate.
        
        # To optimize, let's collect B positions in I_A x J_A
        # Actually, we can just iterate through the grid once to build the graph and check constraints.
        
        # Step 1: Check for immediate contradictions
        # A B tile at (i, j) with i in I_A and j in J_A is invalid.
        for r in I_A:
            row_str = grid[r]
            for c in J_A:
                if row_str[c] == 'B':
                    results.append(0)
                    break
            else:
                continue
            break
        else:
            # No immediate contradiction from I_A x J_A
            # Step 2: Determine forced values for U_R and U_C
            
            # forced_C[j] = 0 if column j in U_C is forced to 0
            # forced_R[i] = 0 if row i in U_R is forced to 0
            
            forced_C = [False] * W
            forced_R = [False] * H
            
            # For each row i in I_A, look at B tiles in columns j in U_C.
            # If there is a B at (i, j) with j in U_C, then C_j must be 0.
            for r in I_A:
                row_str = grid[r]
                for c in U_C:
                    if row_str[c] == 'B':
                        forced_C[c] = True
            
            # For each col j in J_A, look at B tiles in rows i in U_R.
            # If there is a B at (i, j) with i in U_R, then R_i must be 0.
            for c in J_A:
                for r in U_R:
                    if grid[r][c] == 'B':
                        forced_R[r] = True
                        
            # Step 3: Build bipartite graph for remaining free variables
            # Nodes: U_R_free = U_R \ {r | forced_R[r]}
            #         U_C_free = U_C \ {c | forced_C[c]}
            
            U_R_free = [r for r in U_R if not forced_R[r]]
            U_C_free = [c for c in U_C if not forced_C[c]]
            
            # Map original indices to graph nodes if needed, or just use sets
            # We need to count connected components in a bipartite graph
            # Edges: (r, c) if grid[r][c] == 'B' and r in U_R_free and c in U_C_free
            
            # Create adjacency list for the bipartite graph
            # Nodes can be identified by (type, index). 
            # Let's use 0..len(U_R_free)-1 for rows and len(U_R_free)..len(U_R_free)+len(U_C_free)-1 for cols
            
            n_rows = len(U_R_free)
            n_cols = len(U_C_free)
            
            # Map original indices to local indices
            r_map = {r: i for i, r in enumerate(U_R_free)}
            c_map = {c: i for i, c in enumerate(U_C_free)}
            
            adj = [[] for _ in range(n_rows + n_cols)]
            
            # Add edges
            # Iterate over B tiles in U_R_free x U_C_free
            # To do this efficiently, we can iterate over rows in U_R_free and check columns in U_C_free
            # But checking all pairs is O(|U_R_free| * |U_C_free|) which can be O(HW).
            # Since sum of HW is 10^6, this is acceptable.
            
            for r in U_R_free:
                row_str = grid[r]
                for c in U_C_free:
                    if row_str[c] == 'B':
                        u = r_map[r]
                        v = n_rows + c_map[c]
                        adj[u].append(v)
                        adj[v].append(u)
                        
            # Count connected components and check for bipartiteness (though it's bipartite by construction)
            # Actually, since it's bipartite by definition (edges only between R and C sets),
            # we just need to count components. Each component has 2 valid colorings.
            
            visited = [False] * (n_rows + n_cols)
            num_components = 0
            
            for i in range(n_rows + n_cols):
                if not visited[i]:
                    num_components += 1
                    # BFS/DFS
                    stack = [i]
                    visited[i] = True
                    while stack:
                        node = stack.pop()
                        for neighbor in adj[node]:
                            if not visited[neighbor]:
                                visited[neighbor] = True
                                stack.append(neighbor)
            
            # Total ways = 4^count_A * 2^num_components
            ans = pow(4, count_A, MOD)
            ans = (ans * pow(2, num_components, MOD)) % MOD
            results.append(ans)

    for res in results:
        print(res)

solve()