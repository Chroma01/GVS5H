import sys

# Increase recursion depth to handle deep segment tree recursion
sys.setrecursionlimit(10**6)

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return
    
    # Precompute prefix distinct counts
    Pre = [0] * N
    seen = set()
    cnt = 0
    for i in range(N):
        if A[i] not in seen:
            seen.add(A[i])
            cnt += 1
        Pre[i] = cnt
        
    # Precompute suffix distinct counts
    Suf = [0] * N
    seen = set()
    cnt = 0
    for i in range(N-1, -1, -1):
        if A[i] not in seen:
            seen.add(A[i])
            cnt += 1
        Suf[i] = cnt
        
    # Segment Tree arrays
    # Size 4*N is safe for N up to 3*10^5
    tree = [-10**9] * (4 * N)
    lazy = [0] * (4 * N)
    
    def push(node):
        lz = lazy[node]
        if lz != 0:
            lazy[2*node] += lz
            tree[2*node] += lz
            lazy[2*node+1] += lz
            tree[2*node+1] += lz
            lazy[node] = 0
            
    def update_add(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            tree[node] += val
            lazy[node] += val
            return
        push(node)
        mid = (start + end) // 2
        update_add(2*node, start, mid, l, r, val)
        update_add(2*node+1, mid+1, end, l, r, val)
        tree[node] = tree[2*node] if tree[2*node] > tree[2*node+1] else tree[2*node+1]
        
    def set_val(node, start, end, idx, val):
        if start == end:
            tree[node] = val
            lazy[node] = 0
            return
        push(node)
        mid = (start + end) // 2
        if idx <= mid:
            set_val(2*node, start, mid, idx, val)
        else:
            set_val(2*node+1, mid+1, end, idx, val)
        tree[node] = tree[2*node] if tree[2*node] > tree[2*node+1] else tree[2*node+1]
        
    def query(node, start, end, l, r):
        if l > end or r < start:
            return -10**9
        if l <= start and end <= r:
            return tree[node]
        push(node)
        mid = (start + end) // 2
        left_max = query(2*node, start, mid, l, r)
        right_max = query(2*node+1, mid+1, end, l, r)
        return left_max if left_max > right_max else right_max

    Last = [-1] * (N + 1)
    max_ans = 0
    
    # Iterate over the end of the middle subarray
    # y corresponds to the index in 0-based A where the middle subarray ends
    # Middle subarray is A[x+1..y], first is A[0..x], third is A[y+1..N-1]
    # x ranges from 0 to y-1
    for y in range(1, N-1):
        val = A[y]
        p = Last[val]
        
        # If val appeared before at p, then for x in [p, y-2], 
        # val is already in A[x+1..y-1], so distinct count doesn't increase.
        # For x < p, val is new, so distinct count increases by 1.
        # We add 1 to Val(x) for x in [p, y-2].
        if p != -1 and p <= y-2:
            update_add(1, 0, N-1, p, y-2, 1)
            
        # Set value for the new valid split point x = y-1
        # Middle subarray is A[y..y], distinct count is 1.
        set_val(1, 0, N-1, y-1, Pre[y-1] + 1)
        
        # Query max over all valid x < y
        current_max = query(1, 0, N-1, 0, y-1)
        ans = current_max + Suf[y+1]
        if ans > max_ans:
            max_ans = ans
            
        Last[val] = y
        
    print(max_ans)

if __name__ == '__main__':
    solve()