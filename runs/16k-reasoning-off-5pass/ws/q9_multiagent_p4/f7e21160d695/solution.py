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

    # Build MST using Kruskal's Algorithm
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    parent = list(range(N + 1))
    # We need to store counts of A and B in each component
    # cntA[i] = number of elements from A in component i
    # cntB[i] = number of elements from B in component i
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    
    # Initialize counts based on input sequences A and B
    # Note: A and B are sequences of vertex indices.
    # We count occurrences of each vertex in A and B.
    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1
        
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
            # Merge smaller to larger or just arbitrarily
            # We need to update counts
            # Let's merge root_j into root_i
            parent[root_j] = root_i
            cntA[root_i] += cntA[root_j]
            cntB[root_i] += cntB[root_j]
            return True
        return False

    total_cost = 0
    
    # Process edges in increasing order of weight
    for u, v, w in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Calculate unmatched A's and B's in each component
            # remA_u: A's in root_u that are not matched with B's in root_u
            # remB_u: B's in root_u that are not matched with A's in root_u
            
            # Number of pairs we can form internally in root_u
            # We greedily match as many as possible within the component
            # The number of unmatched A's is max(0, cntA - cntB)
            # The number of unmatched B's is max(0, cntB - cntA)
            
            remA_u = max(0, cntA[root_u] - cntB[root_u])
            remB_u = max(0, cntB[root_u] - cntA[root_u])
            
            remA_v = max(0, cntA[root_v] - cntB[root_v])
            remB_v = max(0, cntB[root_v] - cntA[root_v])
            
            # The number of pairs that MUST cross the cut (u, v)
            # is the number of unmatched A's in u that can match with unmatched B's in v
            # plus the number of unmatched A's in v that can match with unmatched B's in u.
            
            cross_pairs = min(remA_u, remB_v) + min(remA_v, remB_u)
            
            total_cost += cross_pairs * w
            
            # Now merge the components
            # We perform union by rank/size if needed, but simple linking is O(log N) amortized with path compression
            # Let's link root_v to root_u
            parent[root_v] = root_u
            cntA[root_u] += cntA[root_v]
            cntB[root_u] += cntB[root_v]
            
    print(total_cost)

if __name__ == '__main__':
    solve()