import sys

# Increase recursion depth just in case, though iterative DSU is used
sys.setrecursionlimit(300000)

def solve():
    # Fast I/O
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
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
        
    # Sort edges by weight for Kruskal's
    edges.sort(key=lambda x: x[0])
    
    # DSU initialization
    parent = list(range(N + 1))
    
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
            # Union by rank/size could be added, but path compression is usually sufficient
            parent[root_j] = root_i
            return True
        return False
    
    # Counters for A and B in each component
    # cntA[root] stores number of A nodes in the component rooted at 'root'
    # cntB[root] stores number of B nodes in the component rooted at 'root'
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    
    for x in A:
        cntA[x] = 1
    for x in B:
        cntB[x] = 1
        
    total_cost = 0
    
    for w, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Calculate how many pairs (a, b) with a in component U and b in component V
            # or vice versa can be matched using this edge as the bottleneck.
            # Since we process edges in increasing order, any pair connected within U or V
            # already has a cost < w (or <= w if equal weights processed earlier).
            # The number of new pairs formed by merging U and V is:
            # min(cntA[U], cntB[V]) + min(cntA[V], cntB[U])
            
            term1 = min(cntA[root_u], cntB[root_v])
            term2 = min(cntA[root_v], cntB[root_u])
            
            count = term1 + term2
            total_cost += count * w
            
            # Merge components
            # We attach root_v to root_u
            parent[root_v] = root_u
            cntA[root_u] += cntA[root_v]
            cntB[root_u] += cntB[root_v]
            
    print(total_cost)

if __name__ == '__main__':
    solve()