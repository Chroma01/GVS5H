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

    # Step 1: Construct MST using Kruskal's Algorithm
    # Sort edges by weight
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

    # We need to process edges in increasing order of weight.
    # We will maintain counts of unmatched A's and B's in each component.
    # cntA[root] = number of unmatched A's in the component rooted at 'root'
    # cntB[root] = number of unmatched B's in the component rooted at 'root'
    
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    
    # Initialize counts based on input sequences A and B
    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1
        
    total_cost = 0
    
    # Process edges in sorted order
    for u, v, w in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Calculate how many pairs can be formed with cost w
            # Pairs formed: A in root_u matched with B in root_v
            #              A in root_v matched with B in root_u
            
            match_uv = min(cntA[root_u], cntB[root_v])
            match_vu = min(cntA[root_v], cntB[root_u])
            
            total_cost += w * (match_uv + match_vu)
            
            # Calculate new counts for the merged component
            # Total A consumed = match_uv (from u) + match_vu (from v)
            # Total B consumed = match_uv (from v) + match_vu (from u)
            
            new_cntA = cntA[root_u] + cntA[root_v] - match_uv - match_vu
            new_cntB = cntB[root_u] + cntB[root_v] - match_uv - match_vu
            
            # Perform union by rank
            if rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
                new_root = root_v
            else:
                parent[root_v] = root_u
                new_root = root_u
            
            if rank[root_u] == rank[root_v]:
                rank[new_root] += 1
            
            # Update counts for the new root
            cntA[new_root] = new_cntA
            cntB[new_root] = new_cntB
            
    print(total_cost)

if __name__ == '__main__':
    solve()