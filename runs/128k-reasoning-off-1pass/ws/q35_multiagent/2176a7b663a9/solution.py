import sys
from collections import defaultdict

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    N = int(next(iterator))
    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(next(iterator))
        
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    for i in range(1, N + 1):
        L[i] = int(next(iterator))
        R[i] = int(next(iterator))
        
    Q = int(next(iterator))
    queries = []
    for _ in range(Q):
        s = int(next(iterator))
        t = int(next(iterator))
        queries.append((s, t))
        
    # Check if two intervals are disjoint
    def is_disjoint(i, j):
        return R[i] < L[j] or R[j] < L[i]
    
    # Find connected components using DSU
    parent = list(range(N + 1))
    rank = [0] * (N + 1)
    
    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i == root_j:
            return
        if rank[root_i] < rank[root_j]:
            parent[root_i] = root_j
        elif rank[root_i] > rank[root_j]:
            parent[root_j] = root_i
        else:
            parent[root_j] = root_i
            rank[root_i] += 1
            
    # To find connected components in the complement of an interval graph:
    # Two intervals are connected if they are disjoint.
    # We can use a sweep-line approach. Sort intervals by L.
    # Maintain a set of "active" intervals that haven't been merged yet.
    # An interval i is connected to all previous intervals j where R[j] < L[i].
    # We can efficiently find and union these.
    
    # Create a list of indices sorted by L_i, then by R_i
    indices = list(range(1, N + 1))
    indices.sort(key=lambda x: (L[x], R[x]))
    
    # We'll use a min-heap to keep track of intervals by their R value
    import heapq
    heap = [] # (R[j], j)
    
    for idx in indices:
        # Remove all intervals from heap that are disjoint from current
        # An interval j in heap is disjoint from current if R[j] < L[idx]
        while heap and heap[0][0] < L[idx]:
            r_j, j = heapq.heappop(heap)
            union(j, idx)
            
        heapq.heappush(heap, (R[idx], idx))
        
    # Now, we need to handle the case where intervals might be connected through a chain.
    # The above logic only unions an interval with those that end before it starts.
    # But what if interval A is disjoint from B, and B is disjoint from C, but A and C overlap?
    # Then A and C are in the same component via B.
    # The DSU approach above should handle this because:
    # When processing C, if B is still in the heap and R[B] < L[C], B and C are unioned.
    # And if A was unioned with B earlier, then A, B, C are in the same component.
    # However, there's a subtlety: what if A and B are disjoint, but B is processed after A,
    # and when B is processed, A is no longer in the heap because some other interval C' 
    # with R[C'] < L[B] caused A to be popped? No, we only pop if R[j] < L[current].
    # If A is in the heap, it means R[A] >= L[B] is false? No.
    # Let's re-think.
    
    # Actually, the standard algorithm for connected components in complement of interval graph:
    # Sort intervals by L.
    # Maintain a set of intervals that are "active" (not yet merged into a component with future intervals).
    # For each new interval i, it is connected to all previous intervals j with R[j] < L[i].
    # We union i with all such j.
    # But we also need to ensure that all such j are in the same component.
    # Since they all have R[j] < L[i], they are all disjoint from i.
    # Are they disjoint from each other? Not necessarily.
    # But if j1 and j2 are both disjoint from i, they are in the same component as i.
    # So we can union all such j with i, and they will be in the same component.
    # The issue is efficiency. We can't iterate all j.
    # We can use the heap to find all j with R[j] < L[i].
    # But we need to union them all. We can union the first one with i, and then union the rest with the first one.
    # Or, we can maintain a "representative" for the group of intervals that are disjoint from the current "frontier".
    
    # Let's use a different approach:
    # Sort by L.
    # Keep a list of components. Each component has a min_R (the minimum R among all intervals in the component? No.)
    # Actually, a known efficient method:
    # 1. Sort intervals by L.
    # 2. Use a DSU.
    # 3. Maintain a pointer 'ptr' to the first interval in the sorted list that is not yet processed for merging.
    # 4. For each interval i, find all j < i such that R[j] < L[i]. These j are disjoint from i.
    # 5. Union i with all such j.
    # 6. To do this efficiently, we can maintain a set of intervals that are "active" and use a heap to extract those with small R.
    
    # The previous heap-based approach is correct for finding all j with R[j] < L[i].
    # But we need to union them all. We can do:
    #   first_j = None
    #   while heap and heap[0][0] < L[idx]:
    #       r_j, j = heapq.heappop(heap)
    #       if first_j is None:
    #           first_j = j
    #       else:
    #           union(j, first_j)
    #   if first_j is not None:
    #       union(first_j, idx)
    # This ensures all such j are in the same component as idx.
    
    # Let's re-run the DSU with this logic.
    # Reset DSU
    parent = list(range(N + 1))
    rank = [0] * (N + 1)
    
    # Re-sort
    indices = list(range(1, N + 1))
    indices.sort(key=lambda x: (L[x], R[x]))
    
    heap = []
    
    for idx in indices:
        first_j = None
        while heap and heap[0][0] < L[idx]:
            r_j, j = heapq.heappop(heap)
            if first_j is None:
                first_j = j
            else:
                union(j, first_j)
        if first_j is not None:
            union(first_j, idx)
        heapq.heappush(heap, (R[idx], idx))
        
    # Build components
    components = defaultdict(list)
    for i in range(1, N + 1):
        root = find(i)
        components[root].append(i)
        
    # For each component, find the min weight and the two smallest weights
    comp_min_w = {}
    comp_second_min_w = {}
    
    for root, nodes in components.items():
        weights = [W[i] for i in nodes]
        weights.sort()
        comp_min_w[root] = weights[0]
        if len(weights) > 1:
            comp_second_min_w[root] = weights[1]
        else:
            comp_second_min_w[root] = float('inf')
            
    # Precompute component for each node
    node_comp = {}
    for i in range(1, N + 1):
        node_comp[i] = find(i)
        
    results = []
    for s, t in queries:
        root_s = node_comp[s]
        root_t = node_comp[t]
        
        if root_s != root_t:
            results.append("-1")
        else:
            # Same component
            # Check direct edge
            direct = is_disjoint(s, t)
            ans = float('inf')
            
            if direct:
                ans = W[s] + W[t]
                
            # Check path through min weight node in component
            min_w = comp_min_w[root_s]
            # Find the node with min weight
            # We need to know if s and t are disjoint from the min weight node
            # Let's find the index of the min weight node
            # We can precompute this, but for now, let's just search.
            # Since we have the component, we can find the min node.
            # But we didn't store the node index, just the weight.
            # Let's store the node index for min weight.
            
            # Actually, let's just check all nodes in the component? No, too slow.
            # We need to know the node with min weight.
            # Let's recompute: find the node with min weight in the component.
            # We can do this during component building.
            
            # For now, let's assume we have a way to get the min weight node.
            # We'll store it in comp_min_node.
            pass
            
    # Let's redo the component processing to store min node
    comp_min_node = {}
    for root, nodes in components.items():
        min_w = float('inf')
        min_node = -1
        for i in nodes:
            if W[i] < min_w:
                min_w = W[i]
                min_node = i
        comp_min_node[root] = min_node
        
    results = []
    for s, t in queries:
        root_s = node_comp[s]
        root_t = node_comp[t]
        
        if root_s != root_t:
            results.append("-1")
        else:
            direct = is_disjoint(s, t)
            ans = float('inf')
            
            if direct:
                ans = W[s] + W[t]
                
            min_node = comp_min_node[root_s]
            # Path through min_node: s -> min_node -> t
            # This path exists if s is disjoint from min_node and t is disjoint from min_node
            # Note: if min_node is s or t, then the path is just the other node, which is covered by direct if they are disjoint.
            # But if min_node is s, then s and t are not necessarily disjoint.
            # If min_node is s, then the path s -> t is just the direct edge, which we already checked.
            # So we only consider min_node if it is different from s and t.
            
            if min_node != s and min_node != t:
                if is_disjoint(s, min_node) and is_disjoint(t, min_node):
                    path_weight = W[s] + W[min_node] + W[t]
                    if path_weight < ans:
                        ans = path_weight
                        
            if ans == float('inf'):
                results.append("-1")
            else:
                results.append(str(ans))
                
    print('\n'.join(results))

solve()