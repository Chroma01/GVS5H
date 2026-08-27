import sys
import bisect

# Increase recursion depth to handle deep segment tree traversals if necessary
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        S_x = int(next(iterator))
        S_y = int(next(iterator))
        
        houses = []
        for i in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            houses.append((x, y, i))
            
        moves = []
        for _ in range(M):
            d = next(iterator)
            c = int(next(iterator))
            moves.append((d, c))
            
    except StopIteration:
        return

    # Group houses by X and Y
    # by_x[x] -> list of (y, original_index)
    # by_y[y] -> list of (x, original_index)
    by_x = {}
    by_y = {}
    
    for x, y, idx in houses:
        if x not in by_x:
            by_x[x] = []
        by_x[x].append((y, idx))
        
        if y not in by_y:
            by_y[y] = []
        by_y[y].append((x, idx))
        
    # Sort the lists by the other coordinate
    for x in by_x:
        by_x[x].sort(key=lambda p: p[0])
    for y in by_y:
        by_y[y].sort(key=lambda p: p[0])
        
    # Pre-extract coordinate lists for binary search
    ys_by_x = {x: [p[0] for p in lst] for x, lst in by_x.items()}
    xs_by_y = {y: [p[0] for p in lst] for y, lst in by_y.items()}
    
    # Segment Tree Implementation
    # Supports: update, query_sum, find_first
    class SegmentTree:
        def __init__(self, size):
            self.n = size
            self.size = 1
            while self.size < size:
                self.size *= 2
            # Initialize tree with 1s (all unvisited)
            self.tree = [1] * (2 * self.size)
            # Leaves are at indices [size, size + n - 1]
            # We must ensure indices >= n are 0 for correctness of sums
            for i in range(self.n, self.size):
                self.tree[self.size + i] = 0
                
        def update(self, idx, val):
            """Set value at idx to val (0 or 1). idx is 0-based."""
            idx += self.size
            self.tree[idx] = val
            idx //= 2
            while idx > 0:
                self.tree[idx] = self.tree[2*idx] + self.tree[2*idx+1]
                idx //= 2
                
        def query_sum(self, l, r):
            """Sum in range [l, r] inclusive. Returns 0 if l > r."""
            if l > r:
                return 0
            l += self.size
            r += self.size
            res = 0
            while l <= r:
                if l % 2 == 1:
                    res += self.tree[l]
                    l += 1
                if r % 2 == 0:
                    res += self.tree[r]
                    r -= 1
                l //= 2
                r //= 2
            return res
            
        def find_first(self, l, r):
            """Find the smallest index in [l, r] with value 1. Returns -1 if none."""
            if l > r:
                return -1
            if self.query_sum(l, r) == 0:
                return -1
            
            # Recursive descent to find the first 1
            return self._find_first_recursive(1, 0, self.size - 1, l, r)

        def _find_first_recursive(self, node, node_l, node_r, q_l, q_r):
            # If current node range is outside query or sum is 0, return -1
            if node_l > q_r or node_r < q_l or self.tree[node] == 0:
                return -1
            
            if node_l == node_r:
                return node_l - self.size
            
            mid = (node_l + node_r) // 2
            
            # Try left child first
            res = self._find_first_recursive(2*node, node_l, mid, q_l, q_r)
            if res != -1:
                return res
            
            # Try right child
            return self._find_first_recursive(2*node+1, mid+1, node_r, q_l, q_r)

    # Build Segment Trees
    # trees_x maps x_coord -> SegmentTree
    # trees_y maps y_coord -> SegmentTree
    trees_x = {}
    trees_y = {}
    
    for x in by_x:
        trees_x[x] = SegmentTree(len(by_x[x]))
        
    for y in by_y:
        trees_y[y] = SegmentTree(len(by_y[y]))
        
    # Simulation
    curr_x, curr_y = S_x, S_y
    visited_count = 0
    
    for d, c in moves:
        if d == 'U':
            # Vertical move: X fixed, Y changes
            y_start = min(curr_y, curr_y + c)
            y_end = max(curr_y, curr_y + c)
            
            if curr_x in by_x:
                lst = by_x[curr_x]
                ys = ys_by_x[curr_x]
                # Find indices in sorted Y list
                l_idx = bisect.bisect_left(ys, y_start)
                r_idx = bisect.bisect_right(ys, y_end) - 1
                
                if l_idx <= r_idx:
                    st = trees_x[curr_x]
                    while True:
                        idx = st.find_first(l_idx, r_idx)
                        if idx == -1:
                            break
                        st.update(idx, 0)
                        visited_count += 1
                        
        elif d == 'D':
            y_start = min(curr_y, curr_y - c)
            y_end = max(curr_y, curr_y - c)
            
            if curr_x in by_x:
                lst = by_x[curr_x]
                ys = ys_by_x[curr_x]
                l_idx = bisect.bisect_left(ys, y_start)
                r_idx = bisect.bisect_right(ys, y_end) - 1
                
                if l_idx <= r_idx:
                    st = trees_x[curr_x]
                    while True:
                        idx = st.find_first(l_idx, r_idx)
                        if idx == -1:
                            break
                        st.update(idx, 0)
                        visited_count += 1
                        
        elif d == 'L':
            # Horizontal move: Y fixed, X changes
            x_start = min(curr_x, curr_x - c)
            x_end = max(curr_x, curr_x - c)
            
            if curr_y in by_y:
                lst = by_y[curr_y]
                xs = xs_by_y[curr_y]
                l_idx = bisect.bisect_left(xs, x_start)
                r_idx = bisect.bisect_right(xs, x_end) - 1
                
                if l_idx <= r_idx:
                    st = trees_y[curr_y]
                    while True:
                        idx = st.find_first(l_idx, r_idx)
                        if idx == -1:
                            break
                        st.update(idx, 0)
                        visited_count += 1
                        
        elif d == 'R':
            x_start = min(curr_x, curr_x + c)
            x_end = max(curr_x, curr_x + c)
            
            if curr_y in by_y:
                lst = by_y[curr_y]
                xs = xs_by_y[curr_y]
                l_idx = bisect.bisect_left(xs, x_start)
                r_idx = bisect.bisect_right(xs, x_end) - 1
                
                if l_idx <= r_idx:
                    st = trees_y[curr_y]
                    while True:
                        idx = st.find_first(l_idx, r_idx)
                        if idx == -1:
                            break
                        st.update(idx, 0)
                        visited_count += 1
                        
        # Update current position
        if d == 'U':
            curr_y += c
        elif d == 'D':
            curr_y -= c
        elif d == 'L':
            curr_x -= c
        elif d == 'R':
            curr_x += c
            
    print(f"{curr_x} {curr_y} {visited_count}")

if __name__ == '__main__':
    solve()