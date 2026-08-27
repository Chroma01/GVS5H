import sys

# Increase recursion depth to handle deep recursion in segment tree operations
sys.setrecursionlimit(2000000)

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = int(next(iterator))
        R[i] = int(next(iterator))
        
    try:
        Q_val = next(iterator)
        Q = int(Q_val)
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))
        
    MAX_X = 500000
    size = 1
    while size < MAX_X:
        size *= 2
        
    # tree[node] stores the maximum rating in the range covered by node
    # lazy[node] stores the pending rating increase for the range
    tree = [0] * (2 * size)
    lazy = [0] * (2 * size)
    
    # Initialize leaves: leaf i (0-indexed) corresponds to initial rating i+1
    for i in range(MAX_X):
        tree[size + i] = i + 1
        
    # Build the tree
    for i in range(size - 1, 0, -1):
        tree[i] = max(tree[2*i], tree[2*i+1])
        
    # Iterative function to find the first index with value >= V
    def find_first(V):
        if tree[1] < V:
            return size
        
        node = 1
        l, r = 0, size - 1
        while l < r:
            # Push lazy tag
            lz = lazy[node]
            if lz != 0:
                lazy[2*node] += lz
                tree[2*node] += lz
                lazy[2*node+1] += lz
                tree[2*node+1] += lz
                lazy[node] = 0
            
            mid = (l + r) // 2
            # Since the array is sorted, if left child's max >= V, the first index is in left child
            if tree[2*node] >= V:
                node = 2*node
                r = mid
            else:
                node = 2*node + 1
                l = mid + 1
        return l

    # Recursive function to update range [ql, qr] by adding val
    def update(node, l, r, ql, qr, val):
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            tree[node] += val
            lazy[node] += val
            return
        
        # Push lazy tag
        lz = lazy[node]
        if lz != 0:
            lazy[2*node] += lz
            tree[2*node] += lz
            lazy[2*node+1] += lz
            tree[2*node+1] += lz
            lazy[node] = 0
            
        mid = (l + r) // 2
        update(2*node, l, mid, ql, qr, val)
        update(2*node+1, mid+1, r, ql, qr, val)
        tree[node] = max(tree[2*node], tree[2*node+1])

    # Recursive function to query value at index idx
    def query(node, l, r, idx):
        if l == r:
            return tree[node]
        
        # Push lazy tag
        lz = lazy[node]
        if lz != 0:
            lazy[2*node] += lz
            tree[2*node] += lz
            lazy[2*node+1] += lz
            tree[2*node+1] += lz
            lazy[node] = 0
            
        mid = (l + r) // 2
        if idx <= mid:
            return query(2*node, l, mid, idx)
        else:
            return query(2*node+1, mid+1, r, idx)

    # Process each contest
    for i in range(N):
        l_val = L[i]
        r_val = R[i]
        
        # If the maximum rating is less than l_val, no rating falls in [l_val, r_val]
        if tree[1] < l_val:
            continue
            
        # Find the range of initial ratings whose current rating is in [l_val, r_val]
        # idx_l is the first index with rating >= l_val
        idx_l = find_first(l_val)
        
        # idx_r is the first index with rating >= r_val + 1
        # If no such index, idx_r = size
        if tree[1] < r_val + 1:
            idx_r = size
        else:
            idx_r = find_first(r_val + 1)
            
        # Update ratings for initial ratings in [idx_l, idx_r - 1]
        if idx_l < idx_r:
            update(1, 0, size-1, idx_l, idx_r - 1, 1)
            
    # Answer queries
    results = []
    for x in queries:
        idx = x - 1
        if 0 <= idx < MAX_X:
            res = query(1, 0, size-1, idx)
            results.append(str(res))
        else:
            results.append(str(x))
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()