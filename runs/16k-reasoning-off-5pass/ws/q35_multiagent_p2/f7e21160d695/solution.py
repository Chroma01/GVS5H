import sys

# Increase recursion depth just in case, though we use iterative DSU
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
        edges.append((w, u, v))
    
    # Read A sequence
    A = []
    for _ in range(K):
        A.append(int(next(iterator)))
        
    # Read B sequence
    B = []
    for _ in range(K):
        B.append(int(next(iterator)))

    # Sort edges by weight for Kruskal's
    edges.sort(key=lambda x: x[0])

    # DSU Implementation
    parent = list(range(N + 1))
    # Count of unmatched A and B nodes in each component
    # cntA[i] stores the number of A-nodes in the component with root i
    # cntB[i] stores the number of B-nodes in the component with root i
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)

    # Initialize counts based on A and B arrays
    for node in A:
        cntA[node] += 1
    for node in B:
        cntB[node] += 1

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
            # Merge smaller into larger or just arbitrary
            # We need to merge counts
            # Let's make root_i the new root
            parent[root_j] = root_i
            cntA[root_i] += cntA[root_j]
            cntB[root_i] += cntB[root_j]
            return True
        return False

    total_cost = 0

    # Process edges in increasing order of weight
    for w, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # We are connecting two components with an edge of weight w.
            # Any match formed between an A-node in comp_u and a B-node in comp_v
            # will have minimax cost w (since this is the smallest edge connecting them).
            # Same for A in comp_v and B in comp_u.
            
            # Number of matches we can form:
            # 1. A from u with B from v
            match1 = min(cntA[root_u], cntB[root_v])
            
            # 2. A from v with B from u
            match2 = min(cntA[root_v], cntB[root_u])
            
            total_cost += w * (match1 + match2)
            
            # Update counts
            cntA[root_u] -= match1
            cntB[root_v] -= match1
            
            cntA[root_v] -= match2
            cntB[root_u] -= match2
            
            # Merge the components
            # We perform the union logic manually here to ensure counts are updated correctly
            # before the next iteration, although union() does it. 
            # Let's just call union, but we need to be careful about which root becomes parent.
            # The union function above merges root_j into root_i.
            # Let's standardize: merge root_v into root_u
            
            parent[root_v] = root_u
            cntA[root_u] += cntA[root_v]
            cntB[root_u] += cntB[root_v]
            
            # Note: cntA[root_v] and cntB[root_v] are now irrelevant as root_v is no longer a root.

    print(total_cost)

if __name__ == '__main__':
    solve()