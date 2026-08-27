import sys

# Increase recursion depth just in case, though iterative DSU is used
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
            
    except StopIteration:
        return

    # Sort edges by weight for Kruskal's algorithm
    edges.sort(key=lambda x: x[2])
    
    # DSU initialization
    parent = list(range(N + 1))
    rank = [0] * (N + 1)
    
    def find(i):
        path = []
        while i != parent[i]:
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
    
    # Prepare data structures for the greedy matching
    # cntA[root] = number of unmatched A_i such that A_i is in component root
    # cntB[root] = number of unmatched B_i such that B_i is in component root
    
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    
    # Populate initial counts based on vertex indices
    for x in A:
        cntA[x] += 1
        
    for x in B:
        cntB[x] += 1
        
    total_cost = 0
    pairs_matched = 0
    
    # Iterate through sorted edges and merge components
    for u, v, w in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Calculate how many new pairs can be formed with this edge weight
            # Pairs formed are those where one endpoint is in root_u and the other in root_v
            # Specifically: (A in root_u, B in root_v) and (A in root_v, B in root_u)
            
            # Number of A's in root_u is cntA[root_u]
            # Number of B's in root_v is cntB[root_v]
            # We can match min(cntA[root_u], cntB[root_v]) pairs of type (A_u, B_v)
            
            # Similarly for (A_v, B_u)
            matches_uv = min(cntA[root_u], cntB[root_v])
            matches_vu = min(cntA[root_v], cntB[root_u])
            
            new_matches = matches_uv + matches_vu
            
            # Add cost
            total_cost += new_matches * w
            pairs_matched += new_matches
            
            # Update counts for the merged component
            # We merge root_v into root_u (conceptually)
            # Remaining A's in root_u = (cntA[root_u] + cntA[root_v]) - matches_vu
            # (matches_vu consumes A from root_v and B from root_u)
            # Remaining B's in root_u = (cntB[root_u] + cntB[root_v]) - matches_uv
            # (matches_uv consumes A from root_u and B from root_v)
            
            cntA[root_u] += cntA[root_v] - matches_vu
            cntB[root_u] += cntB[root_v] - matches_uv
            
            # Clear counts for root_v as it's no longer a root
            cntA[root_v] = 0
            cntB[root_v] = 0
            
            # Union operation
            if rank[root_u] < rank[root_v]:
                root_u, root_v = root_v, root_u
            parent[root_v] = root_u
            if rank[root_u] == rank[root_v]:
                rank[root_u] += 1
                
            # Optimization: if all pairs are matched, we can stop early
            if pairs_matched == K:
                break
                
    print(total_cost)

if __name__ == '__main__':
    solve()