import sys

# Increase recursion depth just in case, though iterative approach is preferred
sys.setrecursionlimit(2000)

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)

    def _push(self, node):
        if self.lazy[node] != 0:
            self.tree[2 * node] += self.lazy[node]
            self.lazy[2 * node] += self.lazy[node]
            self.tree[2 * node + 1] += self.lazy[node]
            self.lazy[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0

    def update(self, l, r, val):
        # Range add [l, r) with val
        if l >= r:
            return
        self._update(1, 0, self.size, l, r, val)

    def _update(self, node, start, end, l, r, val):
        if r <= start or end <= l:
            return
        if l <= start and end <= r:
            self.tree[node] += val
            self.lazy[node] += val
            return
        self._push(node)
        mid = (start + end) // 2
        self._update(2 * node, start, mid, l, r, val)
        self._update(2 * node + 1, mid, end, l, r, val)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, l, r):
        # Range max [l, r)
        if l >= r:
            return 0
        return self._query(1, 0, self.size, l, r)

    def _query(self, node, start, end, l, r):
        if r <= start or end <= l:
            return -float('inf')
        if l <= start and end <= r:
            return self.tree[node]
        self._push(node)
        mid = (start + end) // 2
        left_max = self._query(2 * node, start, mid, l, r)
        right_max = self._query(2 * node + 1, mid, end, l, r)
        return max(left_max, right_max)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Precompute suffix distinct counts
    # suff[i] = number of distinct elements in A[i...N-1]
    suff = [0] * (N + 1)
    seen_suffix = set()
    for i in range(N - 1, -1, -1):
        seen_suffix.add(A[i])
        suff[i] = len(seen_suffix)
    
    # Segment tree to manage range updates and max queries
    st = SegmentTree(N)
    
    # Track first and last occurrence of each number in the current prefix A[0...q]
    first_occ = {}
    last_occ = {}
    
    ans = 0
    distinct_prefix = 0
    
    # We iterate q from 1 to N-2 (0-indexed)
    # Split points: i (end of left), j (end of middle)
    # Here q corresponds to j.
    # Left: 0..p, Middle: p+1..q, Right: q+1..N-1
    # p ranges from 0 to q-1.
    
    for q in range(1, N - 1):
        val = A[q]
        
        if val in first_occ:
            # Element seen before. Update its interval.
            # Previous interval was [first_occ[val], last_occ[val] - 1]
            # New interval is [first_occ[val], q - 1]
            # We need to add 1 to the range [last_occ[val], q - 1]
            prev_last = last_occ[val]
            if prev_last < q:
                st.update(prev_last, q, 1)
            last_occ[val] = q
        else:
            # New element
            first_occ[val] = q
            last_occ[val] = q
            distinct_prefix += 1
        
        # Query max overlap in range [0, q)
        # p can be any integer from 0 to q-1.
        max_overlap = st.query(0, q)
        
        # If max_overlap is -inf (should not happen with correct logic and initialization), treat as 0
        if max_overlap == -float('inf'):
            max_overlap = 0
            
        # Total distinct count for this split configuration
        # = (distinct in 0..q) + (overlap count) + (distinct in q+1..N-1)
        current_total = distinct_prefix + max_overlap + suff[q + 1]
        if current_total > ans:
            ans = current_total
            
    print(ans)

if __name__ == '__main__':
    solve()