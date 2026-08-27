import sys

# Increase recursion depth just in case, though we will use iterative approaches
sys.setrecursionlimit(10000)

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

    # 1-based indexing in problem, convert to 0-based
    # A[i] is the parent of node i+1. Edge: i -> A[i]-1
    # Let's use 0-based indexing for nodes 0 to N-1
    adj = [[] for _ in range(N)]
    rev_adj = [[] for _ in range(N)]
    in_degree = [0] * N
    
    for i in range(N):
        parent = A[i] - 1
        # Edge from i to parent
        adj[i].append(parent)
        rev_adj[parent].append(i)
        in_degree[parent] += 1

    # 2. Topological sort to peel off tree nodes and identify cycle nodes
    # Nodes in cycles will have in_degree >= 1 after peeling all tree nodes.
    # We use a queue for Kahn's algorithm.
    queue = []
    for i in range(N):
        if in_degree[i] == 0:
            queue.append(i)
            
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    # Nodes with in_degree > 0 are part of cycles
    cycle_nodes = [i for i in range(N) if in_degree[i] > 0]
    
    # 3. Compute cnt[u]: number of nodes in the subtree rooted at u in the reversed graph
    # (i.e., all nodes that flow into u).
    # We process nodes in reverse topological order (from leaves up to cycle).
    # The queue contains nodes in topological order (leaves first).
    # So iterating queue in reverse gives us leaves to roots.
    
    cnt = [1] * N
    
    # Process in reverse topological order
    for i in range(len(queue) - 1, -1, -1):
        u = queue[i]
        # u flows into adj[u]
        parent = adj[u][0] # Functional graph, only one outgoing edge
        cnt[parent] += cnt[u]
        
    # 4. Process each cycle
    # A node is in a cycle if it was not removed by Kahn's algorithm.
    # We need to find connected components among cycle nodes.
    visited = [False] * N
    
    total_ans = 1
    
    # Precompute powers sum: sum_{v=1}^M v^K mod MOD
    # Since M <= 2025, we can compute this directly for each K.
    # Or precompute for all possible K up to N.
    # Max K is N.
    
    # Let's compute sum_{v=1}^M v^K for each K we encounter.
    # Since N is small (2025), we can just compute it on the fly or precompute.
    # Given multiple components might have same K, caching is good.
    power_sum_cache = {}
    
    def get_power_sum(K, M, MOD):
        if K in power_sum_cache:
            return power_sum_cache[K]
        
        total = 0
        for v in range(1, M + 1):
            total = (total + pow(v, K, MOD)) % MOD
        power_sum_cache[K] = total
        return total

    for start_node in cycle_nodes:
        if visited[start_node]:
            continue
            
        # Find the cycle containing start_node
        cycle = []
        curr = start_node
        while not visited[curr]:
            visited[curr] = True
            cycle.append(curr)
            curr = adj[curr][0]
            
        # Calculate K for this component
        K = 0
        for node in cycle:
            K += cnt[node]
            
        # Add the contribution of this component
        term = get_power_sum(K, M, MOD)
        total_ans = (total_ans * term) % MOD
        
    print(total_ans)

solve()