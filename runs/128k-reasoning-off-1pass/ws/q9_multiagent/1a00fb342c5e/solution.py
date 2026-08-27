import sys

# Increase recursion depth to handle deep recursion in DSU find operations
sys.setrecursionlimit(300000)

class DSU:
    def __init__(self, n):
        # parent[i] stores the parent of node i
        self.parent = list(range(n + 1))
        # xor_dist[i] stores the XOR sum from node i to its parent
        self.xor_dist = [0] * (n + 1)

    def find(self, i):
        if self.parent[i] != i:
            root = self.find(self.parent[i])
            # Path compression: update xor_dist to be relative to the root
            self.xor_dist[i] ^= self.xor_dist[self.parent[i]]
            self.parent[i] = root
        return self.parent[i]

    def union(self, i, j, w):
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            # We want: A[i] ^ A[j] = w
            # We know: A[i] = A[root_i] ^ dist[i]
            #           A[j] = A[root_j] ^ dist[j]
            # So: (A[root_i] ^ dist[i]) ^ (A[root_j] ^ dist[j]) = w
            # => A[root_i] ^ A[root_j] = w ^ dist[i] ^ dist[j]
            # Let's attach root_i to root_j.
            # Then A[root_i] = A[root_j] ^ new_xor_dist
            # So new_xor_dist = w ^ dist[i] ^ dist[j]
            self.parent[root_i] = root_j
            self.xor_dist[root_i] = w ^ self.xor_dist[i] ^ self.xor_dist[j]
            return True
        else:
            # Check consistency
            # A[i] ^ A[j] should be w
            # Current calculated: A[i] ^ A[j] = (A[root] ^ dist[i]) ^ (A[root] ^ dist[j]) = dist[i] ^ dist[j]
            if self.xor_dist[i] ^ self.xor_dist[j] != w:
                return False
            return True

def solve():
    # Read all input from stdin
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
    
    for _ in range(M):
        try:
            u = int(next(iterator))
            v = int(next(iterator))
            w = int(next(iterator))
            
            if not dsu.union(u, v, w):
                print("-1")
                return
        except StopIteration:
            break

    # Collect components and their distances to root
    # We need to determine the optimal value for the root of each component
    # to minimize the sum of (root_val ^ dist[node]) for all nodes in the component.
    
    # Group nodes by their root
    components = {}
    for i in range(1, N + 1):
        root = dsu.find(i)
        if root not in components:
            components[root] = []
        components[root].append(dsu.xor_dist[i])

    # Determine optimal root value for each component
    optimal_root_vals = {}
    max_bits = 31 # Sufficient for 10^9 (2^30 > 10^9)
    
    for root, dists in components.items():
        # For each bit, decide if it should be 0 or 1 in the root value
        # If we set bit b to 0: cost is count of nodes with bit b set (since 0^1=1)
        # If we set bit b to 1: cost is count of nodes with bit b unset (since 1^0=1)
        # We choose the one with smaller cost.
        
        root_val = 0
        for b in range(max_bits):
            count_set = 0
            for d in dists:
                if (d >> b) & 1:
                    count_set += 1
            
            count_unset = len(dists) - count_set
            
            if count_unset < count_set:
                root_val |= (1 << b)
        
        optimal_root_vals[root] = root_val

    # Construct the final answer
    result = [0] * (N + 1)
    for i in range(1, N + 1):
        root = dsu.find(i)
        result[i] = optimal_root_vals[root] ^ dsu.xor_dist[i]
    
    # Output 1-based indices
    print(*(result[1:]))

if __name__ == '__main__':
    solve()