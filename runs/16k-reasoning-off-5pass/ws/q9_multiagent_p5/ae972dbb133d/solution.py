import sys
import math

# Increase recursion depth just in case, though we use iterative DSU
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
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

    for _ in range(T):
        try:
            H = int(next(iterator))
            W = int(next(iterator))
            grid = []
            for _ in range(H):
                grid.append(next(iterator))
        except StopIteration:
            break

        # The problem asks for the number of ways to rotate tiles such that no dead ends exist.
        # Through analysis, we derived that the constraints imply:
        # 1. The vertical edge states y[i][j] must satisfy y[i][j] = y[i-1][j+1] (indices mod H, W).
        #    This implies y[i][j] depends only on (i + j) % G, where G = gcd(H, W).
        #    Let y[i][j] = f((i + j) % G).
        # 2. The horizontal edge states x[i][j] are determined by x[i][j] = 1 ^ y[i][j].
        # 3. For Type B tiles, we have an additional constraint: y[i][j] = y[i][j-1].
        #    Substituting the function form: f((i + j) % G) = f((i + j - 1) % G).
        #
        # Thus, the problem reduces to counting the number of binary functions f: Z_G -> {0, 1}
        # such that for every 'B' tile at (i, j), f((i+j)%G) == f((i+j-1)%G).
        # This is equivalent to counting the number of connected components in a graph where
        # nodes are 0..G-1 and edges connect (i+j)%G and (i+j-1)%G for each 'B' tile.
        # The answer is 2^(number of connected components).

        G = math.gcd(H, W)
        
        # DSU initialization
        parent = list(range(G))
        
        def find(i):
            path = []
            while parent[i] != i:
                path.append(i)
                i = parent[i]
            for node in path:
                parent[node] = i
            return i
        
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False
        
        # Process the grid
        for i in range(H):
            row_str = grid[i]
            for j in range(W):
                if row_str[j] == 'B':
                    u = (i + j) % G
                    v = (i + j - 1) % G
                    union(u, v)
        
        # Count connected components
        components = 0
        for i in range(G):
            if parent[i] == i:
                components += 1
        
        # Calculate 2^components % MOD
        ans = pow(2, components, MOD)
        print(ans)

if __name__ == '__main__':
    solve()