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
            A.append(int(next(iterator)))
    except StopIteration:
        return

    MOD = 998244353

    # A[i] is the node that i points to. Note: input is 1-based, convert to 0-based.
    # Adjust A to be 0-indexed
    adj = [x - 1 for x in A]

    visited = [False] * N
    in_stack = [False] * N
    component_ways = 1

    # We need to process each component.
    # Since each node has exactly one outgoing edge, the graph is a collection of components.
    # Each component consists of exactly one cycle and some trees rooted on the cycle nodes.
    
    # We will iterate through all nodes. If a node is not visited, we start a traversal to find its component.
    # To find the cycle and the size of the component, we can follow the path.
    
    # However, a simpler way given the constraints (N <= 2025) is:
    # 1. Identify the cycle for each unvisited node.
    # 2. Count the size of the component (nodes that eventually reach this cycle).
    
    # Let's use an iterative approach to avoid recursion depth issues and manage state.
    
    # We need to find for each node:
    # - Is it part of a cycle?
    # - Which cycle does it belong to?
    # - What is the size of the component?
    
    # Strategy:
    # 1. Detect cycles. Since out-degree is 1, we can follow paths.
    #    Use a "visited" array to mark nodes we've processed.
    #    If we hit a node currently in the current path, we found a cycle.
    #    If we hit a node already fully processed, we merge into that component.
    
    # Let's maintain:
    # - visited: boolean, true if node is part of a processed component
    # - component_id: integer, ID of the component the node belongs to
    # - cycle_len[comp_id]: length of the cycle in that component
    # - total_size[comp_id]: total number of nodes in that component
    
    visited = [False] * N
    comp_id = [-1] * N
    cycle_len = []
    total_size = []
    
    # To efficiently find cycles, we can use a "path" list for the current traversal.
    # But since N is small, we can just simulate the path.
    
    # We will iterate i from 0 to N-1. If i is not visited, we start a traversal.
    # We follow the path: i -> adj[i] -> adj[adj[i]] ...
    # We keep track of the path.
    # If we encounter a node that is already visited:
    #   - If it belongs to a component with a known cycle, we just add the current path nodes to that component.
    #   - If it belongs to a component without a cycle yet (impossible in this graph structure as every component has a cycle), 
    #     wait, actually, if we hit a visited node, it MUST be part of a component that already has a cycle identified.
    #     Why? Because every component has exactly one cycle. If we hit a visited node, that node is part of a component.
    #     That component must have a cycle. So we just attach the current path to that component.
    # If we encounter a node that is in the current path (not yet visited globally, but in current stack):
    #   - We found a cycle. The cycle is from the first occurrence of this node to the end of the path.
    #   - We record the cycle length.
    #   - We record the total size of the component (which is the length of the path so far).
    #   - Mark all nodes in the path as visited and assign them to a new component ID.
    
    # Wait, the logic "If we hit a visited node... it MUST be part of a component that already has a cycle" is correct.
    # But we need to be careful about the "current path" detection.
    
    # Let's refine:
    # We maintain `visited` (globally processed).
    # When starting a traversal from `start_node`:
    #   current = start_node
    #   path = []
    #   while current is not visited:
    #       if current is in path:
    #           # Cycle detected
    #           cycle_start_idx = path.index(current)
    #           cycle_nodes = path[cycle_start_idx:]
    #           cycle_len = len(cycle_nodes)
    #           total_size = len(path)
    #           # Create new component
    #           new_comp_id = len(cycle_len)
    #           cycle_len.append(cycle_len_val) # wait, need to store
    #           total_size.append(total_size_val)
    #           # Mark all nodes in path as visited and assign comp_id
    #           for node in path:
    #               visited[node] = True
    #               comp_id[node] = new_comp_id
    #           break
    #       path.append(current)
    #       current = adj[current]
    #   else:
    #       # Loop finished because we hit a visited node
    #       # The last node 'current' is visited. It belongs to some component.
    #       # We need to find which component.
    #       # Since 'current' is visited, comp_id[current] is set.
    #       # All nodes in 'path' belong to the same component as 'current'.
    #       target_comp = comp_id[current]
    #       # We need to update the total_size of target_comp.
    #       # But wait, we might have multiple paths merging into the same component.
    #       # We need to count how many nodes are in the component.
    #       # Actually, the standard way is:
    #       # 1. Identify the cycle first.
    #       # 2. Then count the size of the component (all nodes reaching the cycle).
    #       # Since N is small, we can just do a BFS/DFS from the cycle nodes backwards?
    #       # No, edges are directed towards the cycle. We need to reverse edges to find the trees.
    
    # Revised Plan:
    # 1. Build reverse graph (adj_rev) where edge u -> v in original becomes v -> u in reverse.
    # 2. Find all cycles. For each node, follow path until a cycle is found or a visited node is hit.
    #    Actually, simpler:
    #    - Compute in-degrees.
    #    - Topological sort (Kahn's algorithm) to remove all tree nodes.
    #    - The remaining nodes are the cycles.
    #    - For each cycle, identify the cycle nodes.
    #    - The size of the component is the number of nodes that can reach this cycle.
    #      Since we removed tree nodes, the remaining nodes are exactly the cycles.
    #      We can then do a BFS/DFS on the REVERSE graph starting from all cycle nodes to count the total size of the component.
    
    # This seems robust.
    
    # Step 1: Build reverse graph and compute in-degrees
    adj_rev = [[] for _ in range(N)]
    in_degree = [0] * N
    for u in range(N):
        v = adj[u]
        adj_rev[v].append(u)
        in_degree[u] += 1 # Wait, in_degree[u] is number of edges pointing TO u.
        # Original: u -> adj[u]. So in_degree[adj[u]]++.
    
    in_degree = [0] * N
    for u in range(N):
        v = adj[u]
        in_degree[v] += 1
        
    # Step 2: Topological sort to remove tree nodes
    queue = [i for i in range(N) if in_degree[i] == 0]
    topo_order = []
    
    # Use a list as queue
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        topo_order.append(u)
        for v in adj_rev[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    # Nodes in topo_order are the tree nodes (not in cycles).
    # Nodes NOT in topo_order are in cycles.
    
    # Step 3: Identify cycles and their lengths
    # We can iterate through all nodes. If a node is not in topo_order, it's in a cycle.
    # We need to group them by cycle.
    # Since each component has exactly one cycle, we can just traverse the cycle.
    
    cycle_nodes = [i for i in range(N) if i not in topo_order]
    
    # We need to map each cycle to a unique ID and store its length.
    # Also, we need to count the size of the component for each cycle.
    # The size of the component is the number of nodes that eventually reach this cycle.
    # This includes the cycle nodes themselves and all tree nodes that flow into them.
    # Since we have the reverse graph, we can start BFS from all cycle nodes in the reverse graph.
    # But we must be careful not to double count if we just run BFS from all cycle nodes simultaneously.
    # Actually, since the graph is a set of disjoint components, running BFS from all cycle nodes 
    # in the reverse graph will naturally cover each component exactly once.
    
    # Let's assign a component ID to each node.
    comp_id = [-1] * N
    comp_cycle_len = []
    comp_total_size = []
    
    # We will run BFS on the reverse graph starting from all cycle nodes.
    # We need to ensure we don't process a node twice.
    # Since components are disjoint, we can just maintain a visited array for the BFS.
    
    # However, we need to know which cycle a node belongs to to calculate the answer.
    # Actually, the formula is: Product over components of (Sum_{v=1 to M} v^(size - cycle_len)).
    # So we need (size - cycle_len) for each component.
    
    # Let's collect all cycle nodes.
    # Then for each unvisited cycle node, traverse the cycle to find its length and assign a new component ID.
    # Then run BFS on reverse graph from all nodes in that cycle to count total size.
    
    visited_cycle = [False] * N
    # Mark cycle nodes
    for i in range(N):
        if i not in topo_order:
            visited_cycle[i] = True
            
    # Identify cycles
    # We can iterate through all nodes. If a node is in a cycle and not visited, start traversing.
    # But we need to be careful not to re-traverse the same cycle.
    
    # Let's create a list of cycles.
    cycles = [] # List of lists of nodes
    
    for i in range(N):
        if i not in topo_order and not visited_cycle[i]:
            # Found a new cycle
            cycle = []
            curr = i
            while not visited_cycle[curr]:
                visited_cycle[curr] = True
                cycle.append(curr)
                curr = adj[curr]
            cycles.append(cycle)
            
    # Now we have all cycles.
    # For each cycle, calculate total component size using BFS on reverse graph.
    
    # We need a global visited array for the BFS to count sizes.
    bfs_visited = [False] * N
    
    # We also need to track which component each node belongs to, or just group the results.
    # Let's store the result for each component.
    component_results = [] # List of (cycle_len, total_size)
    
    for cycle in cycles:
        # Start BFS from all nodes in this cycle
        q = cycle[:]
        for node in cycle:
            bfs_visited[node] = True
            
        count = 0
        while q:
            u = q.pop(0)
            count += 1
            for v in adj_rev[u]:
                if not bfs_visited[v]:
                    bfs_visited[v] = True
                    q.append(v)
        
        # The count is the total size of the component.
        # The cycle length is len(cycle).
        component_results.append((len(cycle), count))
        
    # Calculate the answer
    ans = 1
    for cycle_len, total_size in component_results:
        k = total_size - cycle_len
        if k == 0:
            # If k=0, the sum is sum(v^0) = sum(1) = M.
            # Wait, if k=0, it means the component is just the cycle.
            # The cycle nodes must have the same value v.
            # v can be 1..M. So M ways.
            # Formula: sum_{v=1}^M v^0 = M. Correct.
            term = M
        else:
            # We need sum_{v=1}^M v^k mod MOD
            # Since M is up to 2025, we can just loop.
            term = 0
            for v in range(1, M + 1):
                term = (term + pow(v, k, MOD)) % MOD
        
        ans = (ans * term) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()