import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:N+1]))
    
    # Precompute L[i] = number of distinct elements in A[0..i-1] (1-indexed: A[1..i])
    # L[i] for i from 1 to N
    L = [0] * (N + 1)
    seen = set()
    for i in range(1, N + 1):
        seen.add(A[i-1])
        L[i] = len(seen)
    
    # Precompute R[j] = number of distinct elements in A[j..N-1] (1-indexed: A[j+1..N])
    # R[j] for j from 1 to N-1 (since the right subarray starts at j+1, which is index j in 0-based)
    # Actually, let's define R[k] as distinct count in A[k..N-1] (0-indexed), for k from 0 to N-1.
    # Then for a split where the middle subarray ends at index j-1 (0-based), the right subarray is A[j..N-1].
    # Let's re-index carefully.
    
    # Let's use 0-indexed for A: A[0], A[1], ..., A[N-1]
    # Split points: i and j where 0 <= i < j <= N-2
    # Left: A[0..i], Middle: A[i+1..j], Right: A[j+1..N-1]
    # All non-empty: i >= 0, j >= i+1, j <= N-2, so j+1 <= N-1.
    
    # Precompute prefix distinct counts: pref[k] = distinct in A[0..k]
    pref = [0] * N
    seen = set()
    for k in range(N):
        seen.add(A[k])
        pref[k] = len(seen)
    
    # Precompute suffix distinct counts: suff[k] = distinct in A[k..N-1]
    suff = [0] * N
    seen = set()
    for k in range(N-1, -1, -1):
        seen.add(A[k])
        suff[k] = len(seen)
    
    # We want to maximize: pref[i] + distinct(A[i+1..j]) + suff[j+1]
    # for 0 <= i < j <= N-2.
    
    # For a fixed j, we need max_{0 <= i < j} (pref[i] + distinct(A[i+1..j]))
    # Let val[i] = pref[i] + distinct(A[i+1..j])
    # As j increases from 1 to N-2:
    # When we move from j-1 to j, we add A[j] to the middle subarray.
    # For each i < j, distinct(A[i+1..j]) = distinct(A[i+1..j-1]) + (1 if A[j] not in A[i+1..j-1] else 0)
    # A[j] is not in A[i+1..j-1] iff the last occurrence of A[j] before j is at some position last_pos < i+1,
    # i.e., i > last_pos.
    # So for i in [0, last_pos], distinct count doesn't change.
    # For i in [last_pos+1, j-1], distinct count increases by 1.
    
    # We maintain a segment tree over indices i from 0 to N-2.
    # Initially for j=1:
    #   Middle is A[i+1..1] for i=0 only.
    #   val[0] = pref[0] + distinct(A[1..1]) = pref[0] + 1.
    #   pref[0] = 1 (since A[0] is one element).
    #   So val[0] = 2.
    
    # Segment tree for range add, range max.
    # Size: up to N-1 indices (0 to N-2).
    
    size = N - 1  # indices 0 to N-2
    if size <= 0:
        print(0)
        return
    
    tree = [0] * (4 * size)
    lazy = [0] * (4 * size)
    
    def push(node, start, end):
        if lazy[node] != 0:
            tree[node] += lazy[node]
            if start != end:
                lazy[2*node] += lazy[node]
                lazy[2*node+1] += lazy[node]
            lazy[node] = 0
    
    def update(node, start, end, l, r, val):
        push(node, start, end)
        if start > end or start > r or end < l:
            return
        if start >= l and end <= r:
            lazy[node] += val
            push(node, start, end)
            return
        mid = (start + end) // 2
        update(2*node, start, mid, l, r, val)
        update(2*node+1, mid+1, end, l, r, val)
        tree[node] = max(tree[2*node], tree[2*node+1])
    
    def query(node, start, end, l, r):
        push(node, start, end)
        if start > end or start > r or end < l:
            return 0
        if start >= l and end <= r:
            return tree[node]
        mid = (start + end) // 2
        return max(query(2*node, start, mid, l, r), query(2*node+1, mid+1, end, l, r))
    
    # Initialize: for j=1, we set val[0] = pref[0] + 1
    # But let's build the segment tree properly.
    # Initially, all val[i] = -infinity or 0, but we only care about valid i.
    # Let's set all to a very small number, then update.
    
    # Actually, let's initialize the tree with 0 and only update valid positions.
    # For j=1:
    #   last_pos of A[1]: find last occurrence of A[1] in A[0..0].
    #   If A[1] == A[0], last_pos = 0. Else last_pos = -1.
    
    last_occurrence = {}
    
    # Initialize segment tree with a very small value
    # We'll use -10**9 as infinity
    INF = 10**9
    # Build tree with -INF
    def build(node, start, end):
        if start == end:
            tree[node] = -INF
            lazy[node] = 0
            return
        mid = (start + end) // 2
        build(2*node, start, mid)
        build(2*node+1, mid+1, end)
        tree[node] = max(tree[2*node], tree[2*node+1])
    
    build(1, 0, size-1)
    
    ans = 0
    
    # j goes from 1 to N-2 (0-indexed), meaning middle subarray ends at index j.
    # Left subarray ends at i, where 0 <= i < j.
    # Right subarray starts at j+1.
    
    for j in range(1, N-1):
        # Update last_occurrence for A[j-1] before processing j? No, we process j and update last_occ for A[j].
        # Wait, let's think again.
        # When we are at j, we want to compute val[i] for all i < j.
        # val[i] = pref[i] + distinct(A[i+1..j])
        # As we increment j, we update val[i] based on A[j].
        
        # First, find last_pos of A[j] in A[0..j-1]
        val_j = A[j]
        last_pos = last_occurrence.get(val_j, -1)
        
        # For i in [0, last_pos]: distinct(A[i+1..j]) = distinct(A[i+1..j-1])
        #   So val[i] doesn't change.
        # For i in [last_pos+1, j-1]: distinct(A[i+1..j]) = distinct(A[i+1..j-1]) + 1
        #   So val[i] increases by 1.
        
        if last_pos + 1 <= j - 1:
            update(1, 0, size-1, last_pos+1, j-1, 1)
        
        # Now set val[j-1] = pref[j-1] + distinct(A[j..j]) = pref[j-1] + 1
        # This is the new i = j-1 for the current j.
        # But wait, for i = j-1, the middle subarray is A[j..j], and left is A[0..j-1].
        # val[j-1] = pref[j-1] + 1.
        # We need to set this in the segment tree.
        update(1, 0, size-1, j-1, j-1, pref[j-1] + 1 - (-INF)) 
        # Hmm, this is tricky because we initialized to -INF. Let's just set it directly.
        # Actually, let's re-think the initialization.
        
        # Let's just set val[j-1] = pref[j-1] + 1 by doing:
        # current_val = query(1, 0, size-1, j-1, j-1)
        # diff = (pref[j-1] + 1) - current_val
        # update(1, 0, size-1, j-1, j-1, diff)
        
        # But since we built with -INF, and j-1 was never set, it's -INF.
        # So diff = pref[j-1] + 1 - (-INF) = pref[j-1] + 1 + INF.
        # This is messy. Let's just use a different approach for initialization.
        
        # Alternative: Don't use -INF. Use 0 and only query valid ranges.
        # But the segment tree needs to handle the fact that some i are not yet valid.
        # Let's just set val[j-1] = pref[j-1] + 1 by overwriting.
        
        # Let's redo the segment tree to support point set.
        # Actually, let's just use the update with a large diff.
        
        # Let's re-initialize and redo.
        pass
    
    # Let me restart the segment tree logic more cleanly.
    
    # Re-initialize
    tree = [0] * (4 * size)
    lazy = [0] * (4 * size)
    
    def push2(node, start, end):
        if lazy[node] != 0:
            tree[node] += lazy[node]
            if start != end:
                lazy[2*node] += lazy[node]
                lazy[2*node+1] += lazy[node]
            lazy[node] = 0
    
    def update2(node, start, end, l, r, val):
        if start > end or start > r or end < l:
            return
        push2(node, start, end)
        if start >= l and end <= r:
            lazy[node] += val
            push2(node, start, end)
            return
        mid = (start + end) // 2
        update2(2*node, start, mid, l, r, val)
        update2(2*node+1, mid+1, end, l, r, val)
        tree[node] = max(tree[2*node], tree[2*node+1])
    
    def query2(node, start, end, l, r):
        if start > end or start > r or end < l:
            return -INF
        push2(node, start, end)
        if start >= l and end <= r:
            return tree[node]
        mid = (start + end) // 2
        return max(query2(2*node, start, mid, l, r), query2(2*node+1, mid+1, end, l, r))
    
    def set_val(node, start, end, idx, val):
        if start == end:
            tree[node] = val
            lazy[node] = 0
            return
        push2(node, start, end)
        mid = (start + end) // 2
        if idx <= mid:
            set_val(2*node, start, mid, idx, val)
        else:
            set_val(2*node+1, mid+1, end, idx, val)
        tree[node] = max(tree[2*node], tree[2*node+1])
    
    last_occurrence = {}
    ans = 0
    
    for j in range(1, N-1):
        val_j = A[j]
        last_pos = last_occurrence.get(val_j, -1)
        
        # Update range [last_pos+1, j-1] by +1
        if last_pos + 1 <= j - 1:
            update2(1, 0, size-1, last_pos+1, j-1, 1)
        
        # Set val[j-1] = pref[j-1] + 1
        set_val(1, 0, size-1, j-1, pref[j-1] + 1)
        
        # Query max in [0, j-1]
        max_left_mid = query2(1, 0, size-1, 0, j-1)
        
        # Add suff[j+1]
        if j + 1 < N:
            current_ans = max_left_mid + suff[j+1]
            if current_ans > ans:
                ans = current_ans
        
        # Update last_occurrence for A[j]
        last_occurrence[val_j] = j
    
    print(ans)

solve()