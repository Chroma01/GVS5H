import sys

# Increase recursion depth to handle deep recursion in find operations
sys.setrecursionlimit(300000)

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        # xor_dist[i] stores the XOR sum from node i to its parent
        self.xor_dist = [0] * (n + 1)

    def find(self, i):
        if self.parent[i] != i:
            root = self.find(self.parent[i])
            # Path compression: update xor_dist[i] to be from i to root
            # The distance from i to root is (distance from i to old_parent) ^ (distance from old_parent to root)
            self.xor_dist[i] ^= self.xor_dist[self.parent[i]]
            self.parent[i] = root
        return self.parent[i]

    def union(self, u, v, w):
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            # We want to set parent[root_u] = root_v
            # We need to determine xor_dist[root_u] such that the constraint holds.
            # The constraint is: A[u] ^ A[v] = w
            # We know: A[u] = A[root_u] ^ xor_dist[u]
            #          A[v] = A[root_v] ^ xor_dist[v]
            # If we set A[root_v] = 0 (conceptually), then A[root_u] must be such that:
            # (A[root_u] ^ xor_dist[u]) ^ (0 ^ xor_dist[v]) = w
            # A[root_u] = xor_dist[u] ^ xor_dist[v] ^ w
            # Since we are attaching root_u to root_v, xor_dist[root_u] represents A[root_u] ^ A[root_v].
            # So xor_dist[root_u] = xor_dist[u] ^ xor_dist[v] ^ w
            self.parent[root_u] = root_v
            self.xor_dist[root_u] = self.xor_dist[u] ^ self.xor_dist[v] ^ w
            return True
        else:
            # Check consistency
            # dist(u, v) should be w
            # dist(u, v) = dist(u, root) ^ dist(v, root)
            if self.xor_dist[u] ^ self.xor_dist[v] != w:
                return False
            return True

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    dsu = DSU(N)
    possible = True

    for _ in range(M):
        try:
            u = int(next(iterator))
            v = int(next(iterator))
            w = int(next(iterator))
            if not dsu.union(u, v, w):
                possible = False
        except StopIteration:
            break
    
    if not possible:
        print("-1")
        return

    # Group nodes by their root to process each connected component
    # We need to store the relative distances (dist to root) for each node
    # Since find() performs path compression, we must call find() again to ensure
    # xor_dist[i] is relative to the current root.
    
    components = {}
    for i in range(1, N + 1):
        root = dsu.find(i)
        if root not in components:
            components[root] = []
        components[root].append((i, dsu.xor_dist[i]))

    # Initialize result array
    A = [0] * (N + 1)

    # Process each component to find the optimal K
    for root, nodes_list in components.items():
        n_comp = len(nodes_list)
        
        # Determine optimal K bit by bit
        # Z_i <= 10^9, so we need up to bit 29 (2^30 > 10^9)
        K = 0
        for b in range(30):
            count_1 = 0
            for _, d in nodes_list:
                if (d >> b) & 1:
                    count_1 += 1
            
            # If majority have bit 1, set K's bit to 1 to flip them to 0
            # If majority have bit 0, set K's bit to 0 (keep them 0)
            # If equal, either works, let's pick 0
            if count_1 > n_comp // 2:
                K |= (1 << b)
        
        # Assign values
        for idx, d in nodes_list:
            A[idx] = d ^ K

    # Output result
    print(*(A[1:]))

if __name__ == '__main__':
    solve()