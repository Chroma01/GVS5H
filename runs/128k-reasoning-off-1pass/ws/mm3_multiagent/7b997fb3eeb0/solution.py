import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    Q = int(input())
    queries = [tuple(map(int, input().split())) for _ in range(Q)]

    # Precompute nxt[i] = smallest j > i with A[j] >= 2*A[i], or N if none
    nxt = [N] * N
    j = 0
    for i in range(N):
        if j <= i:
            j = i + 1
        while j < N and A[j] < 2 * A[i]:
            j += 1
        nxt[i] = j

    # Process each query using the DSU-based greedy algorithm
    # For each query, we maintain a DSU "next available" structure over the range
    # We'll use a segment tree that can find the first available index >= x in a range
    # and also remove an index.
    
    # Actually, we'll use a simple DSU on the array indices for each query.
    # Since Q is up to 2e5 and N is 2e5, in the worst case total work could be O(N*Q).
    # But with the DSU approach, each operation is nearly O(1), and the number of operations
    # per query is O((R-L+1)). In practice, with small constants, this may pass.
    # However, we can optimize by using a segment tree that supports point updates
    # (set to 0) and range queries (find first 1). This is O(log N) per operation.
    
    # Build a segment tree for availability: 1 if available, 0 if used
    size = 1
    while size < N:
        size <<= 1
    seg = [0] * (2 * size)
    for i in range(N):
        seg[size + i] = 1
    
    for i in range(size - 1, 0, -1):
        seg[i] = seg[2*i] + seg[2*i+1]
    
    def find_first(node, l, r, ql, qr):
        # Find first index with value 1 in [ql, qr)
        if qr <= l or r <= ql or seg[node] == 0:
            return -1
        if r - l == 1:
            return l
        mid = (l + r) // 2
        left_res = find_first(2*node, l, mid, ql, qr)
        if left_res != -1:
            return left_res
        return find_first(2*node+1, mid, r, ql, qr)
    
    def remove_idx(idx):
        # Set position idx to 0
        pos = size + idx
        seg[pos] = 0
        pos //= 2
        while pos:
            seg[pos] = seg[2*pos] + seg[2*pos+1]
            pos //= 2
    
    def add_idx(idx):
        # Set position idx to 1
        pos = size + idx
        seg[pos] = 1
        pos //= 2
        while pos:
            seg[pos] = seg[2*pos] + seg[2*pos+1]
            pos //= 2
    
    out = []
    for L, R in queries:
        L0 = L - 1
        R0 = R - 1
        # Reset availability for this query
        # Instead of resetting the whole segment tree, we can use a versioned DSU
        # or we can process the query by simulating the DSU locally.
        # Since the segment tree approach with O(log N) per operation might be too slow
        # for many queries, we'll use a local DSU array for each query.
        # The DSU array "parent" will point to the next available index.
        # We'll initialize it for the range [L0, R0+1] (with R0+1 as sentinel).
        
        # Local DSU initialization: parent[i] = i+1 for i in [L0, R0], parent[R0+1] = R0+1
        # We'll use a list of size R0 - L0 + 2
        length = R0 - L0 + 1
        parent = list(range(L0, R0 + 2))  # [L0, L0+1, ..., R0+1]
        # parent[i - L0] = next available index starting from i
        def find(x):
            # Path compression
            root = x
            while parent[root - L0] != root:
                root = parent[root - L0]
            while parent[x - L0] != root:
                parent[x - L0], x = root, parent[x - L0]
            return root
        
        def find_first(x):
            # Find first available index >= x in [L0, R0]
            if x > R0:
                return -1
            root = find(x)
            if root > R0:
                return -1
            return root
        
        count = 0
        # Process each index i from L0 to R0 as potential top
        i = L0
        while i <= R0:
            # Find next available index >= i (smallest top)
            top = find_first(i)
            if top == -1 or top > R0:
                break
            # This top is available
            need = nxt[top]
            if need > R0:
                # No valid bottom in range
                break
            # Find bottom: first available index >= need
            bottom = find_first(need)
            if bottom == -1 or bottom > R0:
                # No bottom available, this top remains unmatched
                # Move to next index
                i = top + 1
                continue
            # Match top and bottom
            count += 1
            # Remove both from available set
            # Union top with top+1, and bottom with bottom+1
            # For top:
            t_parent = find(top)
            b_parent = find(bottom)
            # Union top with top+1
            if t_parent <= R0:
                parent[t_parent - L0] = t_parent + 1
            # Union bottom with bottom+1
            if b_parent <= R0:
                parent[b_parent - L0] = b_parent + 1
            # Move to next index after top
            i = top + 1
        
        out.append(str(count))
    
    sys.stdout.write("\n".join(out))

solve()