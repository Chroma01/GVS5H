import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    MOD = 998244353

    results = []

    for _ in range(T):
        try:
            H = int(next(iterator))
            W = int(next(iterator))
            grid = []
            for r in range(H):
                grid.append(next(iterator))
        except StopIteration:
            break

        # We need to count valid vertical edge configurations (N_V)
        # and valid horizontal edge configurations (N_H).
        # The answer is N_V * N_H % MOD.

        # --- Count N_V ---
        # Constraints are on columns. For each column j, we have variables v[0..H-1].
        # v[i] is the vertical edge between row i and i+1 in column j.
        # For cell (i, j):
        #   Top port active <=> v[i-1] == 1 (indices mod H)
        #   Bottom port active <=> v[i] == 1
        #
        # Type B (TB): Top=1, Bottom=1 => v[i-1]=1, v[i]=1. Left/Right=0 (irrelevant for N_V).
        # Type B (LR): Top=0, Bottom=0 => v[i-1]=0, v[i]=0. Left/Right=1 (irrelevant for N_V).
        # Type A: One of Top/Bottom is 1, other is 0. => v[i-1] + v[i] = 1.
        
        def count_vertical_configs(grid, H, W):
            total_ways = 1
            
            for j in range(W):
                # We solve for the cycle v[0], v[1], ..., v[H-1]
                # Constraints from cells (0,j), (1,j), ..., (H-1,j)
                
                # State of each variable: -1 unknown, 0 fixed to 0, 1 fixed to 1
                val = [-1] * H
                
                possible = True
                
                # First pass: Apply hard constraints from Type B tiles
                for i in range(H):
                    cell_type = grid[i][j]
                    if cell_type == 'B':
                        # Check if it's TB or LR based on the string?
                        # Wait, the input gives 'A' or 'B'.
                        # But Type B has two orientations.
                        # The problem says: "Type B: ... connecting midpoints of two opposite edges."
                        # "There are two ways to rotate a Type-B tile."
                        # However, the input string S_ij only tells us the TYPE (A or B).
                        # It does NOT tell us the orientation.
                        # BUT, the orientation is part of the "placement".
                        # We are counting placements.
                        #
                        # Let's re-read carefully.
                        # "print the number ... of ways such that the line segments ... have no dead ends"
                        # "ways to place the tiles is 4^a * 2^b"
                        #
                        # My previous decomposition:
                        # We sum over all valid edge configurations.
                        # For a fixed edge configuration, how many tile placements are valid?
                        #
                        # For Type B tile at (i,j):
                        #   If the edge configuration requires v[i-1]=1, v[i]=1, h[...]=0, h[...]=0:
                        #     This matches Type B (TB) orientation. There is 1 such orientation.
                        #   If the edge configuration requires v[i-1]=0, v[i]=0, h[...]=1, h[...]=1:
                        #     This matches Type B (LR) orientation. There is 1 such orientation.
                        #   If the edge configuration requires something else (e.g. v[i-1]=1, v[i]=0):
                        #     Type B cannot satisfy this. Count = 0.
                        #
                        # For Type A tile at (i,j):
                        #   It requires v[i-1]+v[i]=1 and h[...]+h[...]=1.
                        #   If the edge configuration satisfies this, there is exactly 1 orientation of Type A that matches.
                        #   (e.g. if v[i-1]=1, v[i]=0, h[left]=0, h[right]=1 -> TR).
                        #
                        # So, for a fixed edge configuration (H_edges, V_edges):
                        #   If any cell's required edge states are not met by the global edge config, count is 0.
                        #   If all cells are satisfied, count is 1 (since each cell has exactly 1 valid orientation for that specific edge config).
                        #
                        # Therefore, the number of valid placements is exactly the number of valid edge configurations.
                        #
                        # Back to N_V calculation:
                        # We are counting valid V_edges configurations.
                        # The constraints on V_edges depend on the TYPE of the tile.
                        #
                        # If grid[i][j] == 'B':
                        #   The tile can be TB or LR.
                        #   If it is TB, it imposes v[i-1]=1, v[i]=1.
                        #   If it is LR, it imposes v[i-1]=0, v[i]=0.
                        #   Since we are summing over all placements, we must consider BOTH possibilities for Type B tiles?
                        #   NO. The edge configuration is global.
                        #   If the global V_edges has v[i-1]=1, v[i]=1, then the tile at (i,j) MUST be TB.
                        #   If the global V_edges has v[i-1]=0, v[i]=0, then the tile at (i,j) MUST be LR.
                        #   If the global V_edges has v[i-1]=1, v[i]=0, then NO orientation of Type B works.
                        #
                        # So, for a V_edges configuration to be valid:
                        #   For every cell (i,j) with Type B:
                        #     EITHER (v[i-1]=1 AND v[i]=1)
                        #     OR (v[i-1]=0 AND v[i]=0)
                        #   For every cell (i,j) with Type A:
                        #     v[i-1] + v[i] = 1
                        #
                        # This means Type B tiles do NOT fix the value to a specific constant globally.
                        # They just impose a constraint: v[i-1] == v[i].
                        # And Type A tiles impose: v[i-1] != v[i].
                        
                        # So:
                        # Type B: v[i-1] == v[i]
                        # Type A: v[i-1] != v[i]
                        
                        # Let's re-verify.
                        # Type B (TB): v[i-1]=1, v[i]=1. (Equal)
                        # Type B (LR): v[i-1]=0, v[i]=0. (Equal)
                        # Type A: One is 0, one is 1. (Not Equal)
                        
                        # Yes! The constraint for Type B is simply v[i-1] == v[i].
                        # The constraint for Type A is v[i-1] != v[i].
                        
                        # This simplifies the problem immensely.
                        pass

                # Re-implementing the solver with the simplified constraints:
                # For each column j:
                #   Variables v[0..H-1]
                #   For each i in 0..H-1:
                #     If grid[i][j] == 'B': v[i-1] == v[i]
                #     If grid[i][j] == 'A': v[i-1] != v[i]
                
                # This is a system of equations on a cycle.
                # We can determine the number of solutions by fixing v[0] and propagating.
                
                # Let's use an array to store the relationship.
                # v[i] = v[i-1] ^ diff[i]
                # If grid[i][j] == 'B', diff[i] = 0.
                # If grid[i][j] == 'A', diff[i] = 1.
                
                # Then v[i] = v[0] ^ (diff[1] ^ diff[2] ^ ... ^ diff[i])
                # Let prefix_xor[k] = diff[1] ^ ... ^ diff[k].
                # v[i] = v[0] ^ prefix_xor[i]
                
                # The cycle condition is v[H] == v[0].
                # v[H] is determined by the constraint at i=0?
                # The constraints are for i=0..H-1.
                # v[0] is constrained by i=0: v[-1] (which is v[H-1]) and v[0].
                # v[H-1] is constrained by i=H-1: v[H-2] and v[H-1].
                
                # Let's define diff[i] for the constraint between v[i-1] and v[i].
                # Constraint i: v[i-1] op_i v[i]
                # v[i] = v[i-1] ^ diff[i]
                
                # Then v[1] = v[0] ^ diff[1]
                # v[2] = v[1] ^ diff[2] = v[0] ^ diff[1] ^ diff[2]
                # ...
                # v[H] = v[0] ^ diff[1] ^ ... ^ diff[H]
                
                # But v[H] is v[0] (torus).
                # So we need: v[0] = v[0] ^ (diff[1] ^ ... ^ diff[H])
                # This implies: diff[1] ^ ... ^ diff[H] = 0.
                
                # If the XOR sum of all diffs in the column is 0, then any v[0] works (2 solutions).
                # If the XOR sum is 1, then no solution (0 solutions).
                
                xor_sum = 0
                for i in range(H):
                    # The constraint is for cell (i, j)
                    # It involves v[i-1] and v[i].
                    # Let's index diff for this constraint as d_i.
                    if grid[i][j] == 'B':
                        d_i = 0
                    else: # 'A'
                        d_i = 1
                    xor_sum ^= d_i
                
                if xor_sum == 0:
                    col_ways = 2
                else:
                    col_ways = 0
                
                total_ways = (total_ways * col_ways) % MOD

            return total_ways

        # --- Count N_H ---
        # Similarly for horizontal edges.
        # For each row i, variables h[0..W-1].
        # For each j in 0..W-1:
        #   If grid[i][j] == 'B': h[j-1] == h[j]
        #   If grid[i][j] == 'A': h[j-1] != h[j]
        
        def count_horizontal_configs(grid, H, W):
            total_ways = 1
            
            for i in range(H):
                xor_sum = 0
                for j in range(W):
                    if grid[i][j] == 'B':
                        d_j = 0
                    else: # 'A'
                        d_j = 1
                    xor_sum ^= d_j
                
                if xor_sum == 0:
                    row_ways = 2
                else:
                    row_ways = 0
                
                total_ways = (total_ways * row_ways) % MOD

            return total_ways

        n_v = count_vertical_configs(grid, H, W)
        n_h = count_horizontal_configs(grid, H, W)
        
        ans = (n_v * n_h) % MOD
        results.append(str(ans))

    print('\n'.join(results))

solve()