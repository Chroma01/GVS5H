import sys

def solve():
    # Read all input at once for efficiency
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
        edges.append((w, u, v))
        
    A = []
    for _ in range(K):
        A.append(int(next(iterator)))
        
    B = []
    for _ in range(K):
        B.append(int(next(iterator)))
        
    # Sort edges by weight to process in increasing order
    edges.sort(key=lambda x: x[0])
    
    # DSU initialization
    parent = list(range(N + 1))
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    
    # Count occurrences of A and B vertices
    for a in A:
        cntA[a] += 1
    for b in B:
        cntB[b] += 1
        
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
    
    total_cost = 0
    
    for w, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Calculate pairs to match between the two components
            # Pairs from A in root_u to B in root_v
            pairs1 = min(cntA[root_u], cntB[root_v])
            # Pairs from A in root_v to B in root_u
            pairs2 = min(cntA[root_v], cntB[root_u])
            
            pairs = pairs1 + pairs2
            total_cost += pairs * w
            
            # Update counts before merging (remove matched vertices)
            cntA[root_u] -= pairs1
            cntB[root_v] -= pairs1
            
            cntA[root_v] -= pairs2
            cntB[root_u] -= pairs2
            
            # Merge components
            parent[root_v] = root_u
            cntA[root_u] += cntA[root_v]
            cntB[root_u] += cntB[root_v]
            
    print(total_cost)

if __name__ == '__main__':
    solve()