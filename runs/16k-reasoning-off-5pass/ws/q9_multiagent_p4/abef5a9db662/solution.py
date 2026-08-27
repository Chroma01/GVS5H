import sys

# Increase recursion depth to handle deep segment tree traversals safely
sys.setrecursionlimit(300000)

class SegmentTree:
    def __init__(self, n):
        # Size of the tree array. 2^k >= n
        self.size = 1
        while self.size <= n:
            self.size *= 2
        # min_val and max_val arrays
        self.min_val = [0] * (2 * self.size)
        self.max_val = [0] * (2 * self.size)
        # Lazy propagation array
        self.lazy = [0] * (2 * self.size)
        
        # Initialize leaves: index i (1-based) corresponds to value i
        # Leaf at 'size + i' stores value 'i'
        for i in range(1, n + 1):
            self.min_val[self.size + i] = i
            self.max_val[self.size + i] = i
        
        # Build the tree
        for i in range(self.size - 1, 0, -1):
            self.min_val[i] = min(self.min_val[2 * i], self.min_val[2 * i + 1])
            self.max_val[i] = max(self.max_val[2 * i], self.max_val[2 * i + 1])

    def push(self, node):
        if self.lazy[node] != 0:
            self.lazy[2 * node] += self.lazy[node]
            self.lazy[2 * node + 1] += self.lazy[node]
            self.min_val[2 * node] += self.lazy[node]
            self.max_val[2 * node] += self.lazy[node]
            self.min_val[2 * node + 1] += self.lazy[node]
            self.max_val[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0

    def update_range(self, l, r, val, node=1, start=0, end=None):
        if end is None:
            end = self.size - 1
        
        if l > end or r < start:
            return
        
        if l <= start and end <= r:
            self.lazy[node] += val
            self.min_val[node] += val
            self.max_val[node] += val
            return
        
        self.push(node)
        mid = (start + end) // 2
        self.update_range(l, r, val, 2 * node, start, mid)
        self.update_range(l, r, val, 2 * node + 1, mid + 1, end)
        
        self.min_val[node] = min(self.min_val[2 * node], self.min_val[2 * node + 1])
        self.max_val[node] = max(self.max_val[2 * node], self.max_val[2 * node + 1])

    def find_first_ge(self, target, node=1, start=0, end=None):
        if end is None:
            end = self.size - 1
        
        # If max value in this range is less than target, no element >= target exists here
        if self.max_val[node] < target:
            return -1
        
        if start == end:
            return start + 1 # Return 1-based index
        
        self.push(node)
        mid = (start + end) // 2
        
        # Try left child first
        res = self.find_first_ge(target, 2 * node, start, mid)
        if res != -1:
            return res
        
        return self.find_first_ge(target, 2 * node + 1, mid + 1, end)

    def find_last_le(self, target, node=1, start=0, end=None):
        if end is None:
            end = self.size - 1
        
        # If min value in this range is greater than target, no element <= target exists here
        if self.min_val[node] > target:
            return -1
        
        if start == end:
            return start + 1 # Return 1-based index
        
        self.push(node)
        mid = (start + end) // 2
        
        # Try right child first
        res = self.find_last_le(target, 2 * node + 1, mid + 1, end)
        if res != -1:
            return res
        
        return self.find_last_le(target, 2 * node, start, mid)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    contests = []
    for _ in range(N):
        L = int(next(iterator))
        R = int(next(iterator))
        contests.append((L, R))
    
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))
    
    MAX_VAL = 500000
    st = SegmentTree(MAX_VAL)
    
    for L, R in contests:
        # Find range [l, r] of indices such that st values are in [L, R]
        # l: first index with value >= L
        l = st.find_first_ge(L)
        if l == -1:
            continue
            
        # r: last index with value <= R
        r = st.find_last_le(R)
        if r == -1 or l > r:
            continue
            
        st.update_range(l, r, 1)
        
    results = []
    for x in queries:
        if x > MAX_VAL:
            # If X > MAX_VAL, it won't be incremented by any interval [L, R] where R < X.
            # Since max R is 500000, if X > 500000, it never enters any interval.
            results.append(x) 
        else:
            # Retrieve the value at leaf x (1-based index)
            # Leaf index in array is size + x
            results.append(st.min_val[st.size + x])
            
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()