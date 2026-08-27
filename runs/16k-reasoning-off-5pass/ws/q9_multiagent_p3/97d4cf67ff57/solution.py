import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    if N == 0:
        print(-1)
        return

    # Adjacency list
    adj = [[] for _ in range(N + 1)]
    
    # Read edges
    # There are N-1 edges
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # DP state: dp[u][j][p][h]
    # u: current node
    # j: number of children chosen as internal (degree 4 in subgraph)
    # p: number of children chosen as leaf (degree 1 in subgraph)
    # h: 1 if any node in the subtree (including u) has degree 4, else 0
    # Value: max number of vertices
    
    INF = float('-inf')
    
    # We will use a standard DFS that returns the DP table for the subtree.
    # The DP table is a 3D list: dp[j][p][h]
    # Dimensions: j in 0..4, p in 0..4, h in 0..1
    
    def dfs(u, p):
        # Initialize DP table for the current node u
        # dp[j][p][h]
        # We only care about j + p <= 4
        dp = [[[-INF] * 2 for _ in range(5)] for _ in range(5)]
        
        # Base state: 0 children chosen (j=0, p=0)
        # u is included.
        # h = 0 (no degree 4 yet in subtree, assuming children don't contribute)
        # Since no children, h=0.
        dp[0][0][0] = 1
        
        # Collect children
        children = []
        for v in adj[u]:
            if v == p:
                continue
            children.append(v)
        
        # If no children, return base state
        if not children:
            return dp

        # We will update dp iteratively for each child
        # current_dp[j][p][h] represents the max vertices using j internal and p leaf children from the processed subset.
        current_dp = [[[-INF] * 2 for _ in range(5)] for _ in range(5)]
        current_dp[0][0][0] = 1
        
        for v in children:
            child_res = dfs(v, u)
            
            # Create next_dp initialized to -inf
            next_dp = [[[-INF] * 2 for _ in range(5)] for _ in range(5)]
            
            # Iterate over current states (j, p, h)
            for j in range(5):
                for p in range(5):
                    if j + p > 4:
                        continue
                    for h in range(2):
                        if current_dp[j][p][h] == -INF:
                            continue
                        
                        val = current_dp[j][p][h]
                        
                        # Option 1: Do not include child v
                        # State remains (j, p, h)
                        if val > next_dp[j][p][h]:
                            next_dp[j][p][h] = val
                            
                        # Option 2: Include child v as leaf (p increases by 1)
                        # Child v has degree 1 (0 children + 1 parent u). Valid.
                        # Child v contributes dp[v][0][0][0] vertices.
                        # Child v does NOT contribute to h (since degree 1).
                        
                        if p + 1 <= 4:
                            child_val_leaf = child_res[0][0][0] 
                            if child_val_leaf != -INF:
                                new_h = h
                                if val + child_val_leaf > next_dp[j][p+1][new_h]:
                                    next_dp[j][p+1][new_h] = val + child_val_leaf
                                    
                        # Option 3: Include child v as internal (j increases by 1)
                        # Child v has degree 4 (3 children + 1 parent u). Valid.
                        # Child v contributes dp[v][3][0][1] vertices.
                        # Child v contributes to h (since it has degree 4).
                        # Note: dp[v][3][0][0] is impossible because a node with 3 children 
                        # and 1 parent MUST have degree 4. So we only look at h=1.
                        
                        if j + 1 <= 4:
                            child_val_int = child_res[3][0][1] 
                            if child_val_int != -INF:
                                new_h = 1
                                if val + child_val_int > next_dp[j+1][p][new_h]:
                                    next_dp[j+1][p][new_h] = val + child_val_int
                                    
            current_dp = next_dp
            
        return current_dp

    # Run DFS from root 1
    root_dp = dfs(1, -1)
    
    # Calculate answer
    # Root 1 has no parent.
    # Its degree in subgraph is j + p.
    # Must be 1 or 4.
    # Also must have at least one degree 4 node.
    
    ans = -1
    
    # Case 1: Root degree 1 => j+p = 1
    # Possible (j, p): (1, 0) or (0, 1)
    for j in range(2):
        for p in range(2):
            if j + p == 1:
                # Check if valid alkane
                # Need at least one degree 4 node.
                # Root is degree 1, so must come from subtree.
                # Check root_dp[j][p][1]
                if root_dp[j][p][1] != -INF:
                    ans = max(ans, root_dp[j][p][1])
                    
    # Case 2: Root degree 4 => j+p = 4
    # Possible (j, p): (4, 0), (3, 1), (2, 2), (1, 3), (0, 4)
    for j in range(5):
        for p in range(5):
            if j + p == 4:
                # Root is degree 4, so condition "at least one degree 4" is satisfied.
                # Check both h=0 and h=1 (h=0 is impossible if root is deg4? No, root deg4 implies h=1).
                # Actually, if root is deg4, then h MUST be 1.
                # But let's just check max of both.
                if root_dp[j][p][0] != -INF:
                    ans = max(ans, root_dp[j][p][0])
                if root_dp[j][p][1] != -INF:
                    ans = max(ans, root_dp[j][p][1])
                    
    print(ans)

if __name__ == '__main__':
    solve()