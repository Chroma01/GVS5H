import sys

# Increase recursion depth to handle deep trees in DSU if path compression isn't sufficient
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
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
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            if rank[root_i] == rank[root_j]:
                rank[root_i] += 1
            return True
        return False

    mst_edges = []
    edges_count = 0
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            edges_count += 1
            if edges_count == N - 1:
                break

    # Now process the MST edges in increasing order of weight
    # We need to track the number of unmatched A's and B's in each component
    # comp_A[root] = number of unmatched A's in the component rooted at root
    # comp_B[root] = number of unmatched B's in the component rooted at root
    
    comp_A = [0] * (N + 1)
    comp_B = [0] * (N + 1)

    # Populate initial counts based on A and B arrays
    # Note: A and B are 1-indexed vertices
    for x in A:
        comp_A[x] += 1
    for x in B:
        comp_B[x] += 1

    total_cost = 0

    # Sort MST edges by weight (already sorted from Kruskal's, but good to be explicit)
    mst_edges.sort(key=lambda x: x[2])

    for u, v, w in mst_edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # We are merging component root_u and root_v with edge weight w
            # Calculate available A's and B's in both components
            a_u = comp_A[root_u]
            b_u = comp_B[root_u]
            a_v = comp_A[root_v]
            b_v = comp_B[root_v]
            
            # We want to maximize the number of pairs (A, B) such that A is in one component
            # and B is in the other. These pairs will have bottleneck weight w.
            # Let x be pairs (A in U, B in V) and y be pairs (A in V, B in U).
            # Constraints: x <= a_u, x <= b_v, y <= a_v, y <= b_u.
            # Maximize x + y.
            # The maximum is min(a_u, b_v) + min(a_v, b_u).
            
            P = min(a_u, b_v) + min(a_v, b_u)
            
            total_cost += P * w
            
            # Update counts for the merged component
            # The new component will have (a_u + a_v - P) unmatched A's
            # and (b_u + b_v - P) unmatched B's.
            
            # Attach root_v to root_u
            parent[root_v] = root_u
            
            comp_A[root_u] = (a_u + a_v) - P
            comp_B[root_u] = (b_u + b_v) - P
            
    print(total_cost)

if __name__ == '__main__':
    solve()