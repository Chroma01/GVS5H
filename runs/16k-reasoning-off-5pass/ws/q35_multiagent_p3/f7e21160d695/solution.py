import sys

# Increase recursion depth just in case, though we try to avoid deep recursion
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    edges = []
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        edges.append((u, v, w))

    A = []
    for _ in range(K):
        A.append(int(next(iterator)))
        
    B = []
    for _ in range(K):
        B.append(int(next(iterator)))

    # Step 1: Build MST using Kruskal's Algorithm
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    parent = list(range(N + 1))
    rank = [0] * (N + 1)
    
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
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    mst_edges = []
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            if len(mst_edges) == N - 1:
                break

    # Step 2: Greedy Matching on MST using DSU
    # We process MST edges from smallest weight to largest.
    # For each component, we track the number of unmatched A nodes and B nodes.
    
    # Initialize DSU for the greedy matching process
    # We can reuse the parent/rank arrays or create new ones. 
    # Since we need to store counts, we'll use arrays for counts.
    
    dsu_parent = list(range(N + 1))
    dsu_rank = [0] * (N + 1)
    
    # Count of unmatched A and B nodes in the component rooted at i
    # Initially, each node is its own component.
    # If node i is in A, it contributes 1 to A-count.
    # If node i is in B, it contributes 1 to B-count.
    # Note: A node can be in both A and B lists? The problem says A_i != B_j for all i,j.
    # So a node cannot be in both sets.
    
    comp_a = [0] * (N + 1)
    comp_b = [0] * (N + 1)
    
    for x in A:
        comp_a[x] = 1
    for x in B:
        comp_b[x] = 1
        
    def dsu_find(i):
        path = []
        while dsu_parent[i] != i:
            path.append(i)
            i = dsu_parent[i]
        for node in path:
            dsu_parent[node] = i
        return i

    def dsu_union(i, j):
        root_i = dsu_find(i)
        root_j = dsu_find(j)
        if root_i != root_j:
            if dsu_rank[root_i] < dsu_rank[root_j]:
                dsu_parent[root_i] = root_j
                return root_j
            elif dsu_rank[root_i] > dsu_rank[root_j]:
                dsu_parent[root_j] = root_i
                return root_i
            else:
                dsu_parent[root_j] = root_i
                dsu_rank[root_i] += 1
                return root_i
        return root_i

    total_cost = 0
    
    # Process MST edges in increasing order of weight
    for u, v, w in mst_edges:
        root_u = dsu_find(u)
        root_v = dsu_find(v)
        
        if root_u == root_v:
            continue
            
        # Get counts from both components
        a_u = comp_a[root_u]
        b_u = comp_b[root_u]
        a_v = comp_a[root_v]
        b_v = comp_b[root_v]
        
        # Greedily match A from u with B from v, and B from u with A from v
        match1 = min(a_u, b_v) # Match A_u with B_v
        match2 = min(b_u, a_v) # Match B_u with A_v
        
        total_cost += w * (match1 + match2)
        
        # Update counts for the merged component
        # Remaining A in u: a_u - match1 (since match1 used A_u)
        # Remaining B in u: b_u - match2 (since match2 used B_u)
        # Remaining A in v: a_v - match2 (since match2 used A_v)
        # Remaining B in v: b_v - match1 (since match1 used B_v)
        
        new_a = (a_u - match1) + (a_v - match2)
        new_b = (b_u - match2) + (b_v - match1)
        
        # Union the two components
        new_root = dsu_union(root_u, root_v)
        
        # Update the counts in the new root
        comp_a[new_root] = new_a
        comp_b[new_root] = new_b

    print(total_cost)

if __name__ == '__main__':
    solve()