import sys

# Increase recursion depth to handle deep segment trees
sys.setrecursionlimit(300005)

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

    L = []
    R = []
    for _ in range(M):
        L.append(int(next(iterator)))
        R.append(int(next(iterator)))

    # Coordinate Compression
    # We need to map the ranges [L_i, R_i] to elementary intervals.
    # The critical points are L_i and R_i + 1.
    points = set()
    points.add(1)
    points.add(N + 1)
    for l, r in zip(L, R):
        points.add(l)
        points.add(r + 1)
    
    sorted_points = sorted(list(points))
    coord_map = {val: i for i, val in enumerate(sorted_points)}
    
    # Number of elementary intervals
    num_intervals = len(sorted_points) - 1
    
    # Segment Tree Implementation
    # Maintains the length of covered segments.
    # tree_count: lazy propagation counter
    # tree_len: length of the range covered by at least one interval
    
    class SegmentTree:
        def __init__(self, n_intervals):
            self.n = n_intervals
            self.tree_count = [0] * (4 * n_intervals)
            self.tree_len = [0] * (4 * n_intervals)
            self.sorted_points = sorted_points

        def update(self, node, start, end, l, r):
            if l > end or r < start:
                return
            if l <= start and end <= r:
                self.tree_count[node] += 1
                if self.tree_count[node] > 0:
                    # Calculate length of this node's range
                    self.tree_len[node] = self.sorted_points[end + 1] - self.sorted_points[start]
                else:
                    if start != end:
                        self.tree_len[node] = self.tree_len[2 * node] + self.tree_len[2 * node + 1]
                    else:
                        self.tree_len[node] = 0
                return
            
            mid = (start + end) // 2
            self.update(2 * node, start, mid, l, r)
            self.update(2 * node + 1, mid + 1, end, l, r)
            
            if self.tree_count[node] > 0:
                self.tree_len[node] = self.sorted_points[end + 1] - self.sorted_points[start]
            else:
                self.tree_len[node] = self.tree_len[2 * node] + self.tree_len[2 * node + 1]

        def query(self, node, start, end, ql, qr):
            if ql > end or qr < start:
                return 0
            if ql <= start and end <= qr:
                return self.tree_len[node]
            mid = (start + end) // 2
            return self.query(2 * node, start, mid, ql, qr) + \
                   self.query(2 * node + 1, mid + 1, end, ql, qr)

    # Initialize segment trees
    st1 = SegmentTree(num_intervals)
    st2 = SegmentTree(num_intervals)

    # Arrays to store the decision for each operation
    # 0: Op 0, 1: Op 1, 2: Op 2
    decisions = [0] * M
    possible = True

    # Reverse pass
    for i in range(M - 1, -1, -1):
        l, r = L[i], R[i]
        
        # Map to compressed coordinates
        # Interval [l, r] corresponds to elementary intervals from index coord_map[l] to coord_map[r] - 1
        l_idx = coord_map[l]
        r_idx = coord_map[r] - 1
        
        # Check if [l, r] is fully covered by st1 (Op 1 coverage)
        length = r - l + 1
        covered_len = st1.query(1, 0, num_intervals - 1, l_idx, r_idx)
        
        is_forced_op1 = (covered_len < length)
        
        # Check if complement [1, l-1] U [r+1, N] is fully covered by st2 (Op 2 coverage)
        is_forced_op2 = False
        
        # Part 1: [1, l-1] -> indices 0 to coord_map[l] - 1
        if l > 1:
            l_idx_part1 = 0
            r_idx_part1 = coord_map[l] - 1
            len_part1 = st2.query(1, 0, num_intervals - 1, l_idx_part1, r_idx_part1)
            if len_part1 < l - 1:
                is_forced_op2 = True
        else:
            is_forced_op2 = False # No points before l
            
        if not is_forced_op2 and r < N:
            # Part 2: [r+1, N] -> indices coord_map[r+1] to num_intervals - 1
            l_idx_part2 = coord_map[r + 1]
            r_idx_part2 = num_intervals - 1
            len_part2 = st2.query(1, 0, num_intervals - 1, l_idx_part2, r_idx_part2)
            if len_part2 < N - r:
                is_forced_op2 = True
        
        # Determine decision
        if is_forced_op1 and is_forced_op2:
            possible = False
            break
        elif is_forced_op1:
            decisions[i] = 1
            # Update st1 with [l, r]
            st1.update(1, 0, num_intervals - 1, l_idx, r_idx)
        elif is_forced_op2:
            decisions[i] = 2
            # Update st2 with complement
            if l > 1:
                st2.update(1, 0, num_intervals - 1, 0, coord_map[l] - 1)
            if r < N:
                st2.update(1, 0, num_intervals - 1, coord_map[r + 1], num_intervals - 1)
        else:
            decisions[i] = 0
            
    if not possible:
        print("-1")
        return

    # Forward verification
    # We need to check if the union of chosen operations covers [1, N]
    # Use a new segment tree to track coverage
    final_st = SegmentTree(num_intervals)
    
    for i in range(M):
        if decisions[i] == 1:
            l, r = L[i], R[i]
            l_idx = coord_map[l]
            r_idx = coord_map[r] - 1
            final_st.update(1, 0, num_intervals - 1, l_idx, r_idx)
        elif decisions[i] == 2:
            l, r = L[i], R[i]
            if l > 1:
                l_idx = 0
                r_idx = coord_map[l] - 1
                final_st.update(1, 0, num_intervals - 1, l_idx, r_idx)
            if r < N:
                l_idx = coord_map[r + 1]
                r_idx = num_intervals - 1
                final_st.update(1, 0, num_intervals - 1, l_idx, r_idx)
    
    # Check if total covered length is N
    total_covered = final_st.tree_len[1]
    if total_covered == N:
        # Calculate cost
        cost = sum(1 for d in decisions if d != 0)
        print(cost)
        print(*(decisions))
    else:
        print("-1")

if __name__ == '__main__':
    solve()