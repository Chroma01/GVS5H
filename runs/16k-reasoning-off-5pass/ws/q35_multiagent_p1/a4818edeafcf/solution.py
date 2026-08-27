import sys

# Increase recursion depth just in case, though we will use iterative segment tree
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # 0-indexed array A: A[0], A[1], ..., A[N-1]
    # Split points i, j correspond to:
    # Part 1: A[0...i-1] (length i)
    # Part 2: A[i...j-1] (length j-i)
    # Part 3: A[j...N-1] (length N-j)
    # Constraints: 1 <= i < j <= N-1
    
    # Precompute prefix distinct counts
    # pre[k] = distinct elements in A[0...k-1]
    pre = [0] * (N + 1)
    seen = set()
    for k in range(1, N + 1):
        seen.add(A[k-1])
        pre[k] = len(seen)
        
    # Precompute suffix distinct counts
    # suf[k] = distinct elements in A[k...N-1]
    suf = [0] * (N + 1)
    seen = set()
    for k in range(N - 1, -1, -1):
        seen.add(A[k])
        suf[k] = len(seen)
        
    # We want to maximize: pre[i] + distinct(A[i...j-1]) + suf[j]
    # for 1 <= i < j <= N-1.
    
    # Let's iterate j from 2 to N-1.
    # For a fixed j, we need max_{1<=i<=j-1} (pre[i] + distinct(A[i...j-1]))
    # Let val[i] = pre[i] + distinct(A[i...j-1])
    # When moving from j to j+1, we add A[j] to the middle segment A[i...j-1] -> A[i...j]
    # The distinct count increases by 1 for all i such that A[j] is NOT in A[i...j-1].
    # A[j] is not in A[i...j-1] if the last occurrence of A[j] before index j is at position p < i.
    # Let last_pos[x] be the last index (0-indexed) where x appeared in A[0...j-1].
    # If last_pos[A[j]] = p, then for i <= p, the element A[j] is already in A[i...j-1] (since i <= p < j).
    # Wait, the middle segment is A[i...j-1]. The indices are 0-based.
    # i is the start index of the middle segment.
    # If the last occurrence of A[j] is at index p, then:
    # - If i <= p, then A[j] is in A[i...j-1] because p is in [i, j-1]. So distinct count doesn't change.
    # - If i > p, then A[j] is NOT in A[i...j-1] because p < i. So distinct count increases by 1.
    
    # So, when we move to consider middle segment ending at j (i.e., adding A[j] to the middle),
    # we update val[i] for i in range [last_pos[A[j]] + 1, j-1] by adding 1.
    # Note: i can range from 1 to j-1.
    # If A[j] has not appeared before, last_pos is -1. Then range is [0, j-1]. But i starts at 1.
    # So range is [max(1, last_pos[A[j]] + 1), j-1].
    
    # Segment Tree for Range Add and Range Max
    # Size of segment tree: we need to cover indices 1 to N-2 for i.
    # Actually, i can go up to N-2 (since j <= N-1, i < j => i <= N-2).
    # Let's build a segment tree over indices 1 to N-1.
    
    # Initialize segment tree with pre[i] for i in 1..N-1
    # The value at index i in the segment tree represents pre[i] + current_distinct_middle
    
    # We'll use an iterative segment tree with lazy propagation.
    # Tree size: power of 2 >= N.
    size = 1
    while size < N:
        size *= 2
    
    tree = [0] * (2 * size)
    lazy = [0] * (2 * size)
    
    # Initialize leaves
    # Index i in problem corresponds to leaf at size + i
    for i in range(1, N):
        tree[size + i] = pre[i]
        
    # Build the tree
    for i in range(size - 1, 0, -1):
        tree[i] = max(tree[2*i], tree[2*i+1])
        
    def push(node):
        if lazy[node] != 0:
            lazy[2*node] += lazy[node]
            tree[2*node] += lazy[node]
            lazy[2*node+1] += lazy[node]
            tree[2*node+1] += lazy[node]
            lazy[node] = 0
            
    def update(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            tree[node] += val
            lazy[node] += val
            return
        push(node)
        mid = (start + end) // 2
        update(2*node, start, mid, l, r, val)
        update(2*node+1, mid+1, end, l, r, val)
        tree[node] = max(tree[2*node], tree[2*node+1])
        
    def query(node, start, end, l, r):
        if l > end or r < start:
            return -10**9
        if l <= start and end <= r:
            return tree[node]
        push(node)
        mid = (start + end) // 2
        left_max = query(2*node, start, mid, l, r)
        right_max = query(2*node+1, mid+1, end, l, r)
        return max(left_max, right_max)

    # To make it faster, we can use iterative updates if needed, but recursive with N=3e5 is fine.
    # However, Python recursion limit might be an issue. Let's increase it or use iterative.
    # Given the constraints and Python, iterative segment tree is safer.
    
    # Let's rewrite with iterative segment tree for range add, range max.
    # Iterative lazy propagation is complex. Recursive is easier to implement correctly.
    # We already set recursion limit. Let's stick with recursive but optimize if needed.
    
    # Reset tree and lazy for iterative approach if we switch, but let's try recursive first.
    # Actually, let's just use the recursive functions defined above.
    
    # Track last positions of each number
    last_pos = {}
    
    ans = 0
    
    # Iterate j from 2 to N-1 (0-indexed j is the end of middle segment, exclusive of next part)
    # Middle segment is A[i...j-1].
    # j is the start of the third part.
    # i is the start of the middle segment.
    # i ranges from 1 to j-1.
    
    for j in range(2, N):
        val_j = A[j-1] # The element being added to the middle segment.
        # Wait, the middle segment for split (i, j) is A[i...j-1].
        # When we move from j-1 to j, we are considering middle segments ending at j-1.
        # Previously, for split (i, j-1), middle was A[i...j-2].
        # Now we add A[j-1] to the middle.
        
        # Find last position of val_j before index j-1
        p = last_pos.get(val_j, -1)
        
        # Update range [p+1, j-1] in the segment tree
        # i ranges from 1 to j-1.
        # The update range for i is [max(1, p+1), j-1].
        l_update = p + 1
        if l_update < 1:
            l_update = 1
        r_update = j - 1
        
        if l_update <= r_update:
            update(1, 1, N-1, l_update, r_update, 1)
            
        # Update last_pos
        last_pos[val_j] = j - 1
        
        # Query max in range [1, j-1]
        max_val = query(1, 1, N-1, 1, j-1)
        
        # Candidate answer: max_val + suf[j]
        current_ans = max_val + suf[j]
        if current_ans > ans:
            ans = current_ans
            
    print(ans)

solve()