import sys

# Increase recursion depth just in case, though we use iterative find
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

    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    # DSU State
    parent = list(range(N + 1))
    # countA[i] = number of unmatched A nodes in component i
    # countB[i] = number of unmatched B nodes in component i
    countA = [0] * (N + 1)
    countB = [0] * (N + 1)
    
    # Initialize counts based on input A and B
    for x in A:
        countA[x] += 1
    for x in B:
        countB[x] += 1
        
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

    total_min_cost = 0
    
    for u, v, w in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Calculate how many pairs we can form between the two components
            # Pairs are (A in root_u, B in root_v) and (A in root_v, B in root_u)
            # Cost for each such pair is w
            
            pairs_1 = min(countA[root_u], countB[root_v])
            pairs_2 = min(countA[root_v], countB[root_u])
            
            total_pairs = pairs_1 + pairs_2
            total_cost = total_pairs * w
            
            # Update counts
            # Remove matched counts
            if pairs_1 > 0:
                countA[root_u] -= pairs_1
                countB[root_v] -= pairs_1
            if pairs_2 > 0:
                countA[root_v] -= pairs_2
                countB[root_u] -= pairs_2
                
            # Merge sets: attach root_v to root_u
            parent[root_v] = root_u
            
            # Add remaining counts to the new root
            countA[root_u] += countA[root_v]
            countB[root_u] += countB[root_v]
            
            # Reset counts for the old root (it's no longer a root)
            countA[root_v] = 0
            countB[root_v] = 0
            
            total_min_cost += total_cost
            
    print(total_min_cost)

if __name__ == '__main__':
    solve()