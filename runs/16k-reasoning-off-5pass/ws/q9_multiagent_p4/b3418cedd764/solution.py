import sys

# Increase recursion depth just in case, though iterative approach is used
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
            A.append(int(next(iterator)) - 1) # 0-indexed
    except StopIteration:
        return

    MOD = 998244353

    # Precompute factorials and inverse factorials for combinations
    # Max n for nCr will be (N-1) + M - 1 approx N+M
    # Specifically, we need C(s + v - 1, s). Max s is N, max v is M.
    # So max n is N + M - 1.
    MAX_VAL = N + M + 10
    fact = [1] * MAX_VAL
    finv = [1] * MAX_VAL

    for i in range(2, MAX_VAL):
        fact[i] = (fact[i-1] * i) % MOD

    finv[MAX_VAL-1] = pow(fact[MAX_VAL-1], MOD - 2, MOD)
    for i in range(MAX_VAL-2, 1, -1):
        finv[i] = (finv[i+1] * (i+1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (finv[r] * finv[n-r]) % MOD
        return (num * den) % MOD

    # Build graph and calculate in-degrees
    # Edge i -> A[i]
    adj = [0] * N
    in_degree = [0] * N
    
    for i in range(N):
        adj[i] = A[i]
        in_degree[A[i]] += 1

    # Topological sort to remove tree nodes (nodes with in-degree 0)
    # Queue for nodes with in-degree 0
    queue = [i for i in range(N) if in_degree[i] == 0]
    
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        v = A[u]
        in_degree[v] -= 1
        if in_degree[v] == 0:
            queue.append(v)
            
    # Nodes remaining with in_degree > 0 are cycle nodes
    cycle_nodes = [i for i in range(N) if in_degree[i] > 0]
    
    # Build reverse graph to count tree sizes
    # rev_adj[u] contains list of v such that v -> u in original graph
    rev_adj = [[] for _ in range(N)]
    for i in range(N):
        rev_adj[A[i]].append(i)

    # For each cycle node, count the size of the tree attached to it in the reverse graph
    # The reverse graph edges go from cycle nodes outwards to the leaves of the trees.
    tree_sizes = [0] * N 
    
    visited = [False] * N
    
    for start_node in cycle_nodes:
        # BFS to count size of tree rooted at start_node in rev_adj
        count = 0
        q_bfs = [start_node]
        visited[start_node] = True
        while q_bfs:
            u = q_bfs.pop(0)
            count += 1
            for v in rev_adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q_bfs.append(v)
        tree_sizes[start_node] = count

    # Group cycle nodes by component and calculate ways
    component_ways = []
    used_cycle = [False] * N
    
    for c in cycle_nodes:
        if used_cycle[c]:
            continue
        
        # Find the cycle and collect all cycle nodes in this component
        cycle_path = []
        curr = c
        while not used_cycle[curr]:
            used_cycle[curr] = True
            cycle_path.append(curr)
            curr = A[curr]
        
        # Collect tree sizes for these nodes
        sizes = [tree_sizes[node] for node in cycle_path]
        
        # Calculate sum_{v=1 to M} product_{s in sizes} C(s + v - 1, s)
        total_sum = 0
        
        for v in range(1, M + 1):
            term = 1
            for s in sizes:
                # nCr(s + v - 1, s)
                n_val = s + v - 1
                r_val = s
                term = (term * nCr_mod(n_val, r_val)) % MOD
            total_sum = (total_sum + term) % MOD
            
        component_ways.append(total_sum)

    # The answer is the product of ways for all components
    ans = 1
    for w in component_ways:
        ans = (ans * w) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()