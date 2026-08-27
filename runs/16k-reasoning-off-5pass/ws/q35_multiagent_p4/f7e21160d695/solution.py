import sys

# Increase recursion depth just in case, though iterative DSU is preferred
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

    A = []
    for _ in range(K):
        A.append(int(next(iterator)))

    B = []
    for _ in range(K):
        B.append(int(next(iterator)))

    # Kruskal's Algorithm to build MST
    # Sort edges by weight
    edges.sort(key=lambda x: x[0])

    parent = list(range(N + 1))
    rank = [0] * (N + 1)

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
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    # DSU state for counting unmatched A and B nodes in each component
    # cntA[root] stores the number of unmatched A-nodes in the component with root
    # cntB[root] stores the number of unmatched B-nodes in the component with root
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)

    for node in range(1, N + 1):
        # Initialize counts based on input arrays A and B
        # Note: A and B are 1-indexed lists of vertex numbers
        # We need to count occurrences of each vertex in A and B
        pass

    # Count occurrences of each vertex in A and B
    # Since vertices are 1 to N
    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1

    total_cost = 0
    
    # Process MST edges
    for w, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Calculate matches between the two components
            # Matches: A in comp_u with B in comp_v
            matches1 = min(cntA[root_u], cntB[root_v])
            # Matches: A in comp_v with B in comp_u
            matches2 = min(cntA[root_v], cntB[root_u])
            
            total_matches = matches1 + matches2
            
            total_cost += total_matches * w
            
            # Update counts for the new merged component
            # The matched nodes are removed from the pool of unmatched nodes
            new_cntA = cntA[root_u] + cntA[root_v] - total_matches
            new_cntB = cntB[root_u] + cntB[root_v] - total_matches
            
            # Perform union
            # We need to attach one root to another and update the counts
            if rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
                cntA[root_v] = new_cntA
                cntB[root_v] = new_cntB
            elif rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
                cntA[root_u] = new_cntA
                cntB[root_u] = new_cntB
            else:
                parent[root_v] = root_u
                rank[root_u] += 1
                cntA[root_u] = new_cntA
                cntB[root_u] = new_cntB

    print(total_cost)

if __name__ == '__main__':
    solve()