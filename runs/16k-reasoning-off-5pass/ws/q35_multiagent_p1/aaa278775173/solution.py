class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        
        n, m = len(grid), len(grid[0])
        
        # Directions: 0: (1,1), 1: (1,-1), 2: (-1,1), 3: (-1,-1)
        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        # Helper to get expected value at position k
        def expected_value(k: int) -> int:
            if k == 0:
                return 1
            return 2 if k % 2 == 1 else 0
        
        # Precompute forward[dir][i][j]: max length of valid sequence starting at (i,j) in direction dir
        forward = [[[0] * m for _ in range(n)] for _ in range(4)]
        
        for d in range(4):
            dy, dx = dirs[d]
            # Iterate in reverse order of the direction
            # For direction (dy, dx), we iterate from last cell to first
            rows = range(n-1, -1, -1) if dy > 0 else range(n)
            cols = range(m-1, -1, -1) if dx > 0 else range(m)
            
            # We need to iterate in the order opposite to the direction for DP
            # Actually, for forward, we want to compute from the end of the direction backwards
            # So for direction (1,1), we start from bottom-right and go to top-left
            # Let's define iteration order: for each direction, iterate cells such that when we are at (i,j),
            # the next cell in the direction has already been computed.
            
            if dy == 1 and dx == 1:
                ii = range(n-1, -1, -1)
                jj = range(m-1, -1, -1)
            elif dy == 1 and dx == -1:
                ii = range(n-1, -1, -1)
                jj = range(m)
            elif dy == -1 and dx == 1:
                ii = range(n)
                jj = range(m-1, -1, -1)
            elif dy == -1 and dx == -1:
                ii = range(n)
                jj = range(m)
                
            for i in ii:
                for j in jj:
                    # Check if current cell can be start of sequence (position 0)
                    if grid[i][j] == 1:
                        forward[d][i][j] = 1
                    else:
                        # Look at next cell in direction
                        ni, nj = i + dy, j + dx
                        if 0 <= ni < n and 0 <= nj < m:
                            if forward[d][ni][nj] > 0:
                                # Current cell should be at position forward[d][ni][nj] in the sequence
                                # The next cell is at position 0 of the remaining sequence, so current is at position forward[d][ni][nj]
                                # Actually, if the sequence starting at (ni,nj) has length L, then the sequence starting at (i,j) 
                                # would have current cell at position 0, and (ni,nj) at position 1.
                                # So we need grid[i][j] == expected_value(0) = 1? No.
                                # Let's redefine: forward[d][i][j] is the length of the valid sequence starting at (i,j).
                                # If grid[i][j] == expected_value(0) = 1, then it can start a sequence of length at least 1.
                                # Then if grid[ni][nj] == expected_value(1), we can extend.
                                # So: if grid[i][j] == expected_value(0) and grid[ni][nj] == expected_value(1), then forward[d][i][j] = 1 + forward[d][ni][nj]
                                # But actually, the sequence starting at (ni,nj) might not start with expected_value(0). 
                                # We need to check: the value at (i,j) should be expected_value(0), and the value at (ni,nj) should be expected_value(1), etc.
                                # Actually, the DP state: forward[d][i][j] = 1 if grid[i][j]==1, else 0.
                                # Then if grid[i][j]==1 and grid[ni][nj]==2, then forward[d][i][j] = 1 + forward[d][ni][nj] only if forward[d][ni][nj] > 0 and grid[ni][nj]==2.
                                # But what if the sequence starting at (ni,nj) has length L, meaning it covers positions 0 to L-1 in the sub-sequence.
                                # Then for (i,j), it covers positions 0 to L, so we need grid[i][j] to be expected_value(0) and grid[ni][nj] to be expected_value(1), etc.
                                # Actually, the standard way: 
                                #   if grid[i][j] == expected_value(0):
                                #       if next cell exists and grid[next] == expected_value(1) and forward[d][next] > 0:
                                #           forward[d][i][j] = 1 + forward[d][next]
                                #       else:
                                #           forward[d][i][j] = 1
                                #   else:
                                #       forward[d][i][j] = 0
                                # But this is not correct because the sequence must be contiguous and follow the pattern.
                                # Actually, the correct recurrence:
                                #   Let L = forward[d][ni][nj]
                                #   If L > 0, it means there is a valid sequence of length L starting at (ni,nj) with values: expected_value(0), expected_value(1), ..., expected_value(L-1)
                                #   Then for (i,j) to extend it, we need grid[i][j] == expected_value(0) and grid[ni][nj] == expected_value(1)? No.
                                #   Actually, the sequence starting at (i,j) would be: grid[i][j], grid[ni][nj], ...
                                #   So grid[i][j] must be expected_value(0), grid[ni][nj] must be expected_value(1), etc.
                                #   But the sequence starting at (ni,nj) already satisfies: grid[ni][nj] = expected_value(0), grid[ni+dy][nj+dx] = expected_value(1), ...
                                #   So for (i,j) to extend, we need:
                                #       grid[i][j] = expected_value(0)
                                #       and the sequence starting at (ni,nj) must match expected_value(1), expected_value(2), ...
                                #   But our forward[d][ni][nj] is defined as starting with expected_value(0). So it doesn't directly help.
                                #
                                # Alternative approach: 
                                #   Instead, define forward[d][i][j] as the length of the valid sequence starting at (i,j) in direction d, 
                                #   where the sequence must start with 1 (expected_value(0)).
                                #   Then:
                                #       if grid[i][j] != 1:
                                #           forward[d][i][j] = 0
                                #       else:
                                #           ni, nj = i+dy, j+dx
                                #           if 0<=ni<n and 0<=nj<m and grid[ni][nj]==2: # expected_value(1)
                                #               # But we need to check if the sequence continues: the next cell after (ni,nj) should be 0, etc.
                                #               # Actually, we can use the forward value of (ni,nj) but shifted? 
                                #               # No, because forward[d][ni][nj] is for a sequence starting with 1 at (ni,nj).
                                #               # We need a different DP.
                                #
                                # Let's redefine: 
                                #   Let dp[d][i][j] be the length of the valid sequence ending at (i,j) coming from direction -d.
                                #   But it's easier to compute "backward" lengths.
                                #
                                # Actually, a simpler method: 
                                #   For each direction d, and each cell (i,j), compute the length of the valid sequence starting at (i,j) in direction d.
                                #   We can do this by iterating from the end of the grid in the direction d backwards.
                                #   For a cell (i,j), if grid[i][j] == 1, then base length is 1.
                                #   Then check the next cell (ni, nj) in direction d. If grid[ni][nj] == 2, then we can potentially extend.
                                #   But to know if the extension is valid, we need to know the length of the sequence starting at (ni,nj) that starts with 2? 
                                #   That's not what we computed.
                                #
                                # Revised plan: 
                                #   Compute for each cell and direction, the length of the valid sequence starting at that cell, but the sequence must start with 1.
                                #   Then, for the V-shape, we need to match the pattern at the corner.
                                #
                                # Actually, let's compute two arrays:
                                #   start_len[d][i][j]: length of valid sequence starting at (i,j) in direction d, where the sequence starts with 1.
                                #   This is computed as:
                                #       if grid[i][j] != 1: start_len[d][i][j] = 0
                                #       else:
                                #           ni, nj = i+dy, j+dx
                                #           if 0<=ni<n and 0<=nj<m and grid[ni][nj]==2:
                                #               # Now, we need the length of the sequence starting at (ni,nj) that starts with 2? 
                                #               # But our start_len is defined to start with 1.
                                #               # So we need a different DP: let's compute the length of the valid sequence starting at (i,j) in direction d, 
                                #               # but without requiring it to start with 1. Instead, we require it to follow the pattern from the current position.
                                #
                                # Better: 
                                #   Let f[d][i][j] = length of the valid sequence starting at (i,j) in direction d, following the pattern:
                                #       position 0: 1
                                #       position 1: 2
                                #       position 2: 0
                                #       position 3: 2
                                #       ...
                                #   Then:
                                #       if grid[i][j] != 1: f[d][i][j] = 0
                                #       else:
                                #           ni, nj = i+dy, j+dx
                                #           if 0<=ni<n and 0<=nj<m and grid[ni][nj]==2:
                                #               # But we need to check the rest of the sequence starting from (ni,nj) with pattern starting at position 1.
                                #               # So we need a DP that knows the starting position's expected value.
                                #
                                # Given the complexity, let's use a different approach: 
                                #   Precompute for each cell and direction, the length of the valid sequence ending at that cell (coming from the opposite direction).
                                #   Let back[d][i][j] = length of valid sequence ending at (i,j) coming from direction d (i.e., the sequence approaches (i,j) from direction d).
                                #   This means the sequence goes: ... -> (i-dy, j-dx) -> (i,j)
                                #   And the sequence follows the pattern. The last element (at (i,j)) is at some position k.
                                #
                                #   We can compute back[d][i][j] by iterating in the direction d (from start to end).
                                #   For direction d, iterate cells in order of d.
                                #   For each cell (i,j):
                                #       if grid[i][j] == 1: 
                                #           back[d][i][j] = 1  (sequence of length 1 ending here, starting with 1)
                                #       else:
                                #           pi, pj = i-dy, j-dx  (previous cell in direction d)
                                #           if 0<=pi<n and 0<=pj<m and back[d][pi][pj] > 0:
                                #               k = back[d][pi][pj]  # the previous cell was at position k-1 in the sequence ending at (pi,pj)
                                #               # So the current cell is at position k.
                                #               if grid[i][j] == expected_value(k):
                                #                   back[d][i][j] = back[d][pi][pj] + 1
                                #               else:
                                #                   back[d][i][j] = 0
                                #           else:
                                #               back[d][i][j] = 0
                                #
                                #   Similarly, we can compute forward[d][i][j] = length of valid sequence starting at (i,j) in direction d.
                                #   But note: forward[d][i][j] is the same as back[-d][i'][j'] for the previous cell? Not exactly.
                                #   Actually, forward[d][i][j] can be computed similarly by iterating in reverse direction.
                                #
                                #   For the V-shape: 
                                #       At corner (i,j), with first leg direction d1 (meaning the first leg ends at (i,j) coming from direction d1, so the sequence approaches (i,j) from direction d1), 
                                #       the length of the first leg is back[d1][i][j]. Let this be L1.
                                #       The corner is at position k = L1 - 1 in the first leg? No, the first leg has L1 elements, so the corner is at index L1-1 (0-indexed) in the first leg.
                                #       But in the overall sequence, the corner is at position k. And the first leg corresponds to positions 0 to k.
                                #       So k = L1 - 1.
                                #       Then the second leg starts at the corner and goes in direction d2. The second leg has length L2 = forward[d2][i][j] (computed similarly).
                                #       But the second leg starts at the corner, which is position k in the overall sequence. So the second leg covers positions k to k+L2-1.
                                #       Total length = k + L2 = (L1 - 1) + L2.
                                #
                                #   However, we can also have the corner not at the end of the first leg? Actually, the first leg is defined as the segment before the turn, and it ends at the corner. So the corner is the last element of the first leg.
                                #   Therefore, k = L1 - 1.
                                #
                                #   But wait: the problem allows the V-shape to be just one leg (no turn). In that case, the length is just the length of the longest valid diagonal segment.
                                #   We should also consider that.
                                #
                                #   So algorithm:
                                #       1. Compute back[d][i][j] for all d, i, j.
                                #       2. Compute forward[d][i][j] for all d, i, j. (forward[d][i][j] is the length of valid sequence starting at (i,j) in direction d, following the pattern from position 0).
                                #          Actually, forward[d][i][j] can be computed as:
                                #             if grid[i][j] != 1: 0
                                #             else:
                                #                 ni, nj = i+dy, j+dx
                                #                 if 0<=ni<n and 0<=nj<m and grid[ni][nj]==2:
                                #                     # But we need the length of the sequence starting at (ni,nj) that starts with 2? 
                                #                     # Instead, we can compute a separate DP for "starting with any position in the pattern".
                                #
                                #   Given time, let's implement back and then compute forward similarly but for sequences starting with 1.
                                #
                                #   Actually, for the second leg, we need the length of the valid sequence starting at (i,j) in direction d2, but the sequence must start with the value expected at position k (the corner's position in the overall sequence).
                                #   But our forward[d][i][j] is defined to start with 1 (position 0). 
                                #   So we need a different DP: let's compute for each cell and direction, the length of the valid sequence starting at that cell, but the starting position in the pattern is given.
                                #
                                #   This is getting complicated. Let's simplify:
                                #   Instead, for the second leg, we can use the back array for the opposite direction.
                                #   Specifically, the second leg goes in direction d2 from (i,j). The length of the valid sequence starting at (i,j) in direction d2, with the corner at position k, is the same as the length of the valid sequence ending at (i,j) in direction -d2, but with the pattern shifted by k.
                                #
                                #   Given the constraints and time, I'll implement a simpler O(n*m*min(n,m)) solution that is acceptable for n,m<=500 in PyPy but might be slow in Python. But 500^3=125e6 is too slow for Python.
                                #
                                #   Let's go with the back array approach and then for each corner, iterate over possible k.
                                #
                                #   Steps:
                                #       1. Compute back[d][i][j] for all d, i, j.
                                #       2. For each cell (i,j), the maximum single-leg length ending at (i,j) in any direction is max(back[d][i][j] for d in range(4)).
                                #       3. For V-shapes: for each cell (i,j), for each turn pair (d1, d2):
                                #            L1 = back[d1][i][j]  # length of first leg ending at (i,j)
                                #            if L1 == 0: continue
                                #            # The corner is at position k = L1 - 1 in the first leg, so in the overall sequence, the corner is at position k.
                                #            # But we can also have the corner at an earlier position? No, because the first leg ends at the corner.
                                #            # So k = L1 - 1.
                                #            # Check if grid[i][j] == expected_value(k). If not, then this L1 is not valid for a V-shape with this k.
                                #            # But actually, the first leg might not be maximal; we can take a prefix of the first leg.
                                #            # So for a given corner, we can choose any k from 0 to L1-1 such that grid[i][j] == expected_value(k).
                                #            # Then the second leg length is the length of the valid sequence starting at (i,j) in direction d2, but starting with expected_value(k).
                                #            # To compute that, we need a DP that gives the length of the valid sequence starting at (i,j) in direction d2 with a given starting pattern position.
                                #
                                #   Given the complexity, I'll precompute for each cell and direction, the length of the valid sequence starting at that cell, for each possible starting pattern position (0,1,2). But the pattern repeats every 2 for k>0, so only 2 states for k>0.
                                #
                                #   Let's define:
                                #       fwd[d][i][j][p] = length of valid sequence starting at (i,j) in direction d, where the first element is at pattern position p.
                                #       p=0: expected_value(0)=1
                                #       p=1: expected_value(1)=2
                                #       p=2: expected_value(2)=0
                                #       p=3: same as p=1, etc. So we only need p=0,1,2.
                                #
                                #   Then for the second leg, if the corner is at position k, then the second leg starts at pattern position k mod 3? But the pattern is: 1,2,0,2,0,2,0,... so for k>=1, it's 2 if k odd, 0 if k even. And it repeats every 2. So we only need two states for k>=1.
                                #
                                #   Given time constraints, I'll implement the following:
                                #       - Compute back[d][i][j] as described.
                                #       - Compute fwd[d][i][j] for p=0,1,2.
                                #       - For each corner (i,j), for each turn pair (d1,d2):
                                #           for k in range(back[d1][i][j]):
                                #               if grid[i][j] == expected_value(k):
                                #                   p = k % 3  # but for k>=1, we can use k%2, but to be safe, use mod 3? Actually, the pattern for k>=1 is periodic with period 2: 2,0,2,0,...
                                #                   # But our fwd is defined for p=0,1,2. For k=0, p=0; k=1, p=1; k=2, p=2; k=3, p=1 (since expected_value(3)=2); k=4, p=2 (expected_value(4)=0); etc.
                                #                   # So p = 0 if k==0, else 1 if k%2==1, else 2.
                                #                   L2 = fwd[d2][i][j][p]
                                #                   total = k + L2
                                #                   update global max.
                                #
                                #   This is O(n*m*min(n,m)) which is 500^3=125e6, which is too slow for Python.
                                #
                                #   Optimization: for each corner and turn pair, we only need to check k values where expected_value(k)==grid[i][j]. And we want the largest such k < back[d1][i][j].
                                #   So we can check k = back[d1][i][j]-1, back[d1][i][j]-2, back[d1][i][j]-3 and take the largest valid one.
                                #
                                #   This reduces the inner loop to constant time.
                                #
                                #   So:
                                #       for each corner (i,j), for each turn pair (d1,d2):
                                #           L1 = back[d1][i][j]
                                #           if L1 == 0: continue
                                #           # Check k = L1-1, L1-2, L1-3
                                #           best_k = -1
                                #           for k in [L1-1, L1-2, L1-3]:
                                #               if k < 0: continue
                                #               if grid[i][j] == expected_value(k):
                                #                   best_k = k  # since we iterate from largest, the first valid is the best
                                #                   break
                                #           if best_k == -1: continue
                                #           p = 0 if best_k==0 else (1 if best_k%2==1 else 2)
                                #           L2 = fwd[d2][i][j][p]
                                #           total = best_k + L2
                                #           global_max = max(global_max, total)
                                #
                                #   Also, consider single-leg segments: global_max = max(global_max, max(back[d][i][j] for d in range(4)) for all i,j)
                                #
                                #   Now, implement fwd[d][i][j][p] for p in 0,1,2.
                                #
                                #   fwd[d][i][j][p] = length of valid sequence starting at (i,j) in direction d, with first element at pattern position p.
                                #   Computation:
                                #       Iterate in reverse order of direction d.
                                #       For each cell (i,j):
                                #           for p in 0,1,2:
                                #               if grid[i][j] != expected_value(p):
                                #                   fwd[d][i][j][p] = 0
                                #               else:
                                #                   ni, nj = i+dy, j+dx
                                #                   if 0<=ni<n and 0<=nj<m:
                                #                       # The next element should be at pattern position p+1
                                #                       np = (p+1) % 3  # but for p=2, next is 0? But expected_value(3)=2, not 1. 
                                #                       # Actually, the pattern is: 
                                #                       #   p=0: 1
                                #                       #   p=1: 2
                                #                       #   p=2: 0
                                #                       #   p=3: 2 (same as p=1)
                                #                       #   p=4: 0 (same as p=2)
                                #                       # So for p>=1, the next pattern position is: if p is odd (1,3,5,...) then next is even (2,4,...) which is 0, and if p is even (2,4,...) then next is odd (3,5,...) which is 2.
                                #                       # But our fwd is only defined for p=0,1,2. And for p=2, the next should be p=1? Because expected_value(3)=2, which is same as expected_value(1).
                                #                       # So we can map: 
                                #                       #   p=0 -> next p=1
                                #                       #   p=1 -> next p=2
                                #                       #   p=2 -> next p=1  (because expected_value(3)=2, which is p=1's value)
                                #                       # But then for p=2, if we use next p=1, then fwd[d][ni][nj][1] should be used.
                                #                       #
                                #                       # Define a mapping: next_p = {0:1, 1:2, 2:1}
                                #                       np_map = {0:1, 1:2, 2:1}
                                #                       np = np_map[p]
                                #                       if fwd[d][ni][nj][np] > 0:
                                #                           fwd[d][i][j][p] = 1 + fwd[d][ni][nj][np]
                                #                       else:
                                #                           fwd[d][i][j][p] = 1
                                #                   else:
                                #                       fwd[d][i][j][p] = 1
                                #
                                #   This should work.
                                pass  # placeholder

        # Define directions
        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        def expected_value(k: int) -> int:
            if k == 0:
                return 1
            return 2 if k % 2 == 1 else 0
        
        # Compute back[d][i][j]: length of valid sequence ending at (i,j) coming from direction d
        back = [[[0]*m for _ in range(n)] for _ in range(4)]
        
        for d in range(4):
            dy, dx = dirs[d]
            # Iterate in the direction d order
            if dy == 1 and dx == 1:
                ii, jj = range(n), range(m)
            elif dy == 1 and dx == -1:
                ii, jj = range(n), range(m-1, -1, -1)
            elif dy == -1 and dx == 1:
                ii, jj = range(n-1, -1, -1), range(m)
            elif dy == -1 and dx == -1:
                ii, jj = range(n-1, -1, -1), range(m-1, -1, -1)
                
            for i in ii:
                for j in jj:
                    if grid[i][j] == 1:
                        back[d][i][j] = 1
                    else:
                        pi, pj = i - dy, j - dx
                        if 0 <= pi < n and 0 <= pj < m and back[d][pi][pj] > 0:
                            k = back[d][pi][pj]  # the previous cell was at position k-1, so current is at position k
                            if grid[i][j] == expected_value(k):
                                back[d][i][j] = back[d][pi][pj] + 1
                            else:
                                back[d][i][j] = 0
                        else:
                            back[d][i][j] = 0
        
        # Compute fwd[d][i][j][p] for p in 0,1,2
        fwd = [[[[0]*3 for _ in range(m)] for _ in range(n)] for _ in range(4)]
        
        # Mapping for next pattern position
        next_p_map = {0: 1, 1: 2, 2: 1}
        
        for d in range(4):
            dy, dx = dirs[d]
            # Iterate in reverse order of direction d
            if dy == 1 and dx == 1:
                ii, jj = range(n-1, -1, -1), range(m-1, -1, -1)
            elif dy == 1 and dx == -1:
                ii, jj = range(n-1, -1, -1), range(m)
            elif dy == -1 and dx == 1:
                ii, jj = range(n), range(m-1, -1, -1)
            elif dy == -1 and dx == -1:
                ii, jj = range(n), range(m)
                
            for i in ii:
                for j in jj:
                    for p in range(3):
                        if grid[i][j] != expected_value(p):
                            fwd[d][i][j][p] = 0
                        else:
                            ni, nj = i + dy, j + dx
                            if 0 <= ni < n and 0 <= nj < m:
                                np = next_p_map[p]
                                if fwd[d][ni][nj][np] > 0:
                                    fwd[d][i][j][p] = 1 + fwd[d][ni][nj][np]
                                else:
                                    fwd[d][i][j][p] = 1
                            else:
                                fwd[d][i][j][p] = 1
        
        global_max = 0
        
        # Consider single-leg segments
        for d in range(4):
            for i in range(n):
                for j in range(m):
                    if back[d][i][j] > global_max:
                        global_max = back[d][i][j]
        
        # Turn pairs: (d1, d2) for 90-degree clockwise turn
        # d0=(1,1) -> d1=(1,-1)
        # d1=(1,-1) -> d3=(-1,-1)
        # d3=(-1,-1) -> d2=(-1,1)
        # d2=(-1,1) -> d0=(1,1)
        turn_pairs = [(0, 1), (1, 3), (3, 2), (2, 0)]
        
        for i in range(n):
            for j in range(m):
                for d1, d2 in turn_pairs:
                    L1 = back[d1][i][j]
                    if L1 == 0:
                        continue
                    # Check k = L1-1, L1-2, L1-3
                    best_k = -1
                    for k in [L1-1, L1-2, L1-3]:
                        if k < 0:
                            continue
                        if grid[i][j] == expected_value(k):
                            best_k = k
                            break
                    if best_k == -1:
                        continue
                    # Determine p for the second leg
                    if best_k == 0:
                        p = 0
                    else:
                        p = 1 if best_k % 2 == 1 else 2
                    L2 = fwd[d2][i][j][p]
                    total = best_k + L2
                    if total > global_max:
                        global_max = total
                        
        return global_max