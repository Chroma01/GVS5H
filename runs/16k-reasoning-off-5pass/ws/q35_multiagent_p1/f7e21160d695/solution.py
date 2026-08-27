import sys

# Increase recursion depth just in case, though we use iterative find or path compression
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

    # Kruskal's Algorithm to build MST
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    parent = list(range(N + 1))
    # Size is not strictly needed for correctness of MST, but good for union by rank/size
    # We will use path compression and union by rank/size implicitly or explicitly
    
    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        
        # Path compression
        curr = i
        while curr != root:
            nxt = parent[curr]
            parent[curr] = root
            curr = nxt
        return root

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    mst_edges = []
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            if len(mst_edges) == N - 1:
                break

    # Initialize DSU for the greedy matching process
    # We need to track counts of A and B nodes in each component
    # Note: A node can appear multiple times in the sequence A, same for B
    # So we count occurrences.
    
    # Re-initialize parent for the DSU used in matching
    # We can reuse the parent array but we need to reset it because the previous union
    # operations already merged components. We need fresh components for each vertex.
    parent_match = list(range(N + 1))
    
    def find_match(i):
        root = i
        while parent_match[root] != root:
            root = parent_match[root]
        
        curr = i
        while curr != root:
            nxt = parent_match[curr]
            parent_match[curr] = root
            curr = nxt
        return root

    def union_match(i, j):
        root_i = find_match(i)
        root_j = find_match(j)
        if root_i != root_j:
            parent_match[root_i] = root_j
            return True
        return False

    # Count A and B occurrences for each vertex
    # cntA[i] = number of times vertex i appears in sequence A
    # cntB[i] = number of times vertex i appears in sequence B
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    
    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1

    # For each component, we maintain the total unmatched A and B nodes
    # Initially, each node is its own component
    compA = [0] * (N + 1)
    compB = [0] * (N + 1)
    
    for i in range(1, N + 1):
        compA[i] = cntA[i]
        compB[i] = cntB[i]

    # Process MST edges in increasing order of weight
    # mst_edges is already sorted by weight
    total_cost = 0
    
    for u, v, w in mst_edges:
        root_u = find_match(u)
        root_v = find_match(v)
        
        if root_u != root_v:
            # Calculate pairs to match
            # Pairs between A in comp_u and B in comp_v
            pairs1 = min(compA[root_u], compB[root_v])
            # Pairs between A in comp_v and B in comp_u
            pairs2 = min(compA[root_v], compB[root_u])
            
            pairs = pairs1 + pairs2
            total_cost += pairs * w
            
            # Update counts for the new merged component
            # The roots will be merged. Let's merge root_u into root_v
            # New counts at root_v:
            # Remaining A = (A_u - pairs1) + (A_v - pairs2)
            # Remaining B = (B_u - pairs2) + (B_v - pairs1)
            
            new_compA = (compA[root_u] - pairs1) + (compA[root_v] - pairs2)
            new_compB = (compB[root_u] - pairs2) + (compB[root_v] - pairs1)
            
            compA[root_v] = new_compA
            compB[root_v] = new_compB
            
            # Union the sets
            union_match(root_u, root_v)
            
            # Clear counts for the old root to avoid confusion, though not strictly necessary if we always use find
            compA[root_u] = 0
            compB[root_u] = 0

    print(total_cost)

if __name__ == '__main__':
    solve()