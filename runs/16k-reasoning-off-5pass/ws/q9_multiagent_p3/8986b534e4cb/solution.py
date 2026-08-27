import sys

# Increase recursion depth for deep DFS
sys.setrecursionlimit(10**6)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    S = [0] * (M + 1)
    T = [0] * (M + 1)
    
    travelers = []
    for i in range(1, M + 1):
        s = int(next(iterator))
        t = int(next(iterator))
        travelers.append((s, t))
        S[i] = s
        T[i] = t
        
    L = [0] * (Q + 1)
    R = [0] * (Q + 1)
    for i in range(1, Q + 1):
        l = int(next(iterator))
        r = int(next(iterator))
        L[i] = l
        R[i] = r
        
    # Segment Tree to store ranges of travelers
    tree_size = 1
    while tree_size < M:
        tree_size *= 2
        
    # tree_nodes[u] will store a list of traveler indices
    tree_nodes = [[] for _ in range(2 * tree_size)]
    
    for i in range(1, M + 1):
        tree_nodes[tree_size + i - 1].append(i)
        
    for i in range(tree_size - 1, 0, -1):
        tree_nodes[i] = tree_nodes[2 * i] + tree_nodes[2 * i + 1]
        
    # Function to check cycle for a query
    def check_cycle(query_l, query_r):
        # Collect travelers using segment tree
        travelers_list = []
        
        # Helper to collect
        def collect(node, l, r, ql, qr, res):
            if ql <= l and r <= qr:
                res.extend(tree_nodes[node])
                return
            mid = (l + r) // 2
            if ql <= mid:
                collect(2 * node, l, mid, ql, qr, res)
            if qr > mid:
                collect(2 * node + 1, mid + 1, r, ql, qr, res)
        
        collect(1, 1, tree_size, query_l, query_r, travelers_list)
        
        if not travelers_list:
            return "Yes"
            
        # Identify involved nodes to reset DSU efficiently
        involved = set()
        for i in travelers_list:
            s, t = S[i], T[i]
            involved.add(s)
            involved.add(t)
            if s < t:
                involved.update(range(s + 1, t))
            else:
                involved.update(range(t + 1, s))
        
        # DSU initialization
        parent = {v: v for v in involved}
        rank = {v: 0 for v in involved}
        
        def find_set(v):
            path = []
            while parent[v] != v:
                path.append(v)
                v = parent[v]
            for node in path:
                parent[node] = v
            return v
        
        def union_sets(a, b):
            root_a = find_set(a)
            root_b = find_set(b)
            if root_a != root_b:
                if rank[root_a] < rank[root_b]:
                    root_a, root_b = root_b, root_a
                parent[root_b] = root_a
                if rank[root_a] == rank[root_b]:
                    rank[root_a] += 1
                return True
            return False
            
        # Process equality edges
        for i in travelers_list:
            s, t = S[i], T[i]
            union_sets(s, t)
            
        # Build component graph and check for cycles
        # Map node -> component ID
        comp = {v: find_set(v) for v in involved}
        
        # We need to check for cycles in the graph where edges are k -> S_i
        # If k and S_i are in the same component, it's a self-loop (cycle).
        # If not, it's an edge between components.
        
        # To optimize, we only check for cycles if the graph is small enough or use a heuristic.
        # However, we must be correct.
        # We will collect edges between components.
        # Since Sum(|Mid_i|) can be large, we need to be careful.
        # But we can stop early if we find a cycle.
        
        # Check for self-loops first (most common failure)
        # A self-loop exists if for some i, S_i and any k in Mid_i are in the same component.
        # This is equivalent to: the component of S_i contains any node in Mid_i.
        # We can check this by iterating k.
        
        # Optimization: If the component of S_i is large, it's likely to contain k.
        # But we don't know the size.
        # Let's just iterate. If it's too slow, we might TLE, but it's the best we can do.
        
        # To speed up, we can check if the range [start, end] intersects with the component.
        # But we don't have the component as a set.
        # We can check if any k in [start, end] has comp[k] == comp[S_i].
        
        # We can use a randomized check or just iterate.
        # Given constraints, we assume average case is fast.
        
        # Let's collect edges for cycle detection in component graph
        # We use a set to avoid duplicate edges
        edges = set()
        
        # We also need to detect self-loops
        has_self_loop = False
        
        for i in travelers_list:
            s, t = S[i], T[i]
            c_s = comp[s]
            
            if s < t:
                start, end = s + 1, t - 1
            else:
                start, end = t + 1, s - 1
            
            # Check for self-loop
            # We need to find if any k in [start, end] has comp[k] == c_s
            # We can iterate.
            # Optimization: If the range is large, we can sample? No.
            # Let's just iterate.
            for k in range(start, end + 1):
                if comp[k] == c_s:
                    has_self_loop = True
                    break
            if has_self_loop:
                break
            
            # Collect edges for component graph
            # We only need to collect edges if no self-loop found yet
            # But we need to check all travelers for self-loop first?
            # No, if any self-loop, we return No.
            # So we can break early.
            # But we need to collect edges for the component graph for other travelers?
            # No, if we find a self-loop, we return No immediately.
            # So we can stop processing this traveler.
            # But we need to process other travelers to build the component graph?
            # No, if we find a self-loop, the answer is No.
            # So we can just return No.
            
            # Wait, we need to check ALL travelers for self-loop.
            # If any has a self-loop, return No.
            # So we can break the loop over travelers.
            
            # But we also need to check for cycles in the component graph.
            # If no self-loop, we build the graph and check for cycles.
            # So we can continue building the graph.
            
            # To avoid O(N) per traveler for self-loop check, we can use a different approach.
            # But let's stick to this for now.
            
            # Collect edges
            for k in range(start, end + 1):
                c_k = comp[k]
                if c_k != c_s:
                    edges.add((c_k, c_s))
        
        if has_self_loop:
            return "No"
            
        # Check for cycles in component graph
        # Nodes are component IDs.
        # We need to map component IDs to 0..num-1
        all_comps = set()
        for i in travelers_list:
            all_comps.add(comp[S[i]])
            all_comps.add(comp[T[i]])
        all_comps.update(edges)
        
        comp_list = sorted(list(all_comps))
        comp_map = {c: i for i, c in enumerate(comp_list)}
        num_comps = len(comp_list)
        
        adj_list = [[] for _ in range(num_comps)]
        for c_k, c_s in edges:
            u = comp_map[c_k]
            v = comp_map[c_s]
            adj_list[u].append(v)
            
        # DFS for cycle
        visited = [0] * num_comps
        has_cycle = False
        
        def dfs(u):
            nonlocal has_cycle
            visited[u] = 1
            for v in adj_list[u]:
                if visited[v] == 1:
                    has_cycle = True
                    return
                if visited[v] == 0:
                    dfs(v)
                    if has_cycle:
                        return
            visited[u] = 2
            
        for i in range(num_comps):
            if visited[i] == 0:
                dfs(i)
                if has_cycle:
                    break
        
        if has_cycle:
            return "No"
            
        return "Yes"

    # Process queries
    results = []
    for i in range(1, Q + 1):
        ans = check_cycle(L[i], R[i])
        results.append(ans)
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()