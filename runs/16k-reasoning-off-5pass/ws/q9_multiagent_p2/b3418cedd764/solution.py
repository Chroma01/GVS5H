import sys

# Increase recursion depth just in case, though iterative approaches are preferred
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

    # Build reversed graph: A[i] -> i
    # Original: i -> A[i]
    # Reversed: A[i] -> i (edges directed from parent to child in the dependency tree)
    rev_adj = [[] for _ in range(N)]
    in_degree = [0] * N
    for i in range(N):
        parent = A[i]
        rev_adj[parent].append(i)
        in_degree[i] += 1

    # Identify nodes that are part of cycles using Kahn's algorithm (topological sort)
    # Nodes with in-degree 0 in the reversed graph are leaves of the trees attached to cycles.
    # We peel them off. The remaining nodes will form the cycles.
    queue = [i for i in range(N) if in_degree[i] == 0]
    topo_order = []
    
    # Use a list as a queue for O(N) processing since we just need an order
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        topo_order.append(u)
        for v in rev_adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    # Nodes not in topo_order are part of cycles
    cycle_nodes = [i for i in range(N) if i not in topo_order]
    
    # Mark cycle nodes
    is_cycle = [False] * N
    for u in cycle_nodes:
        is_cycle[u] = True
        
    # DP arrays
    # W[u][k] stores the number of ways to assign the subtree rooted at u (in reversed graph)
    # given that x_u = k.
    # prefix_W[u][k] stores sum(W[u][1]...W[u][k]).
    W = [None] * N
    prefix_W = [None] * N
    
    # Process tree nodes (in topo_order)
    for u in topo_order:
        # Identify children in the reversed graph that are NOT cycle nodes
        children = [c for c in rev_adj[u] if not is_cycle[c]]
        
        if not children:
            # Leaf in the tree (points to cycle in original)
            # If x_u = k, there is 1 way (just x_u=k).
            # So W[u][k] = 1 for all k.
            W[u] = [1] * (M + 1)
        else:
            # Compute W[u][k] = product_{c} (sum_{m=1}^k W[c][m])
            # We need prefix sums of children's W values.
            # Since children are processed before u in topo_order, prefix_W[c] is ready.
            
            # Precompute prefix sums for children to avoid recomputing inside k loop
            child_prefix_sums = []
            for c in children:
                # prefix_W[c] is a list of size M+1
                child_prefix_sums.append(prefix_W[c])
            
            W[u] = [1] * (M + 1)
            for k in range(1, M + 1):
                val = 1
                for p_sum in child_prefix_sums:
                    val = (val * p_sum[k]) % MOD
                W[u][k] = val
        
        # Compute prefix_W[u]
        curr = 0
        pw = [0] * (M + 1)
        for k in range(1, M + 1):
            curr = (curr + W[u][k]) % MOD
            pw[k] = curr
        prefix_W[u] = pw

    # Process cycle nodes
    visited_cycle = [False] * N
    total_ans = 0
    
    for u in cycle_nodes:
        if visited_cycle[u]:
            continue
        
        # Find the cycle containing u
        cycle_path = []
        curr = u
        while not visited_cycle[curr]:
            visited_cycle[curr] = True
            cycle_path.append(curr)
            curr = A[curr]
            if curr == u:
                break
        
        # Compute W[node][k] for each node in the cycle
        # W[node][k] = product_{c in tree_children} (prefix_W[c][k])
        cycle_W = []
        for node in cycle_path:
            children = [c for c in rev_adj[node] if not is_cycle[c]]
            if not children:
                w_node = [1] * (M + 1)
            else:
                w_node = [1] * (M + 1)
                for k in range(1, M + 1):
                    val = 1
                    for c in children:
                        val = (val * prefix_W[c][k]) % MOD
                    w_node[k] = val
            cycle_W.append(w_node)
        
        # Sum over v=1..M of Product(W[u][v]) for u in cycle
        comp_sum = 0
        for v in range(1, M + 1):
            prod_v = 1
            for w_node in cycle_W:
                prod_v = (prod_v * w_node[v]) % MOD
            comp_sum = (comp_sum + prod_v) % MOD
            
        total_ans = (total_ans + comp_sum) % MOD

    print(total_ans)

if __name__ == '__main__':
    solve()