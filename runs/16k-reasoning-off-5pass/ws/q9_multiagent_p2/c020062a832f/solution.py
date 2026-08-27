import sys
from collections import defaultdict

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Fenwick Tree (Binary Indexed Tree) implementation
    # 1-based indexing for BIT
    class FenwickTree:
        def __init__(self, size):
            self.tree = [0] * (size + 1)

        def update(self, i, delta):
            while i < len(self.tree):
                self.tree[i] += delta
                i += i & (-i)

        def query(self, i):
            s = 0
            while i > 0:
                s += self.tree[i]
                i -= i & (-i)
            return s

    # Step 1: Calculate initial inversion count for k=0
    # We use a BIT to count inversions.
    # Iterate from right to left, count how many elements to the right are smaller.
    
    temp_bit = FenwickTree(M)
    initial_inv = 0
    
    # Right to left
    for i in range(N - 1, -1, -1):
        x = A[i]
        # count elements < x
        # BIT is 1-based. Value v maps to v+1.
        # query(x) sums indices 1..x => values 0..x-1.
        cnt_smaller = temp_bit.query(x)
        initial_inv += cnt_smaller
        temp_bit.update(x + 1, 1)

    # Initialize BITs for the main algorithm
    # bit_pos tracks indices of elements in V (non-wrapped)
    # bit_val tracks values (A[i]) of elements in V
    bit_pos = FenwickTree(N)
    bit_val = FenwickTree(M)
    
    for i in range(N):
        bit_pos.update(i + 1, 1)
        bit_val.update(A[i] + 1, 1)
        
    curr_inv = initial_inv
    
    # Group indices by A[i]
    groups = defaultdict(list)
    for i in range(N):
        groups[A[i]].append(i)
    
    # Main loop for k = 0 to M-1
    for k in range(M):
        # Print current inversion count
        print(curr_inv)
        
        if k == M - 1:
            break
            
        # Prepare for k+1
        # Elements wrapping: A[i] = M - 1 - k
        target_val = M - 1 - k
        
        if target_val < 0 or target_val >= M:
            continue
            
        # Get indices to wrap
        wrap_indices = groups[target_val]
        
        # Sort descending to easily track right_wrap_count
        wrap_indices.sort(reverse=True)
        
        right_wrap_count = 0
        
        for p in wrap_indices:
            # p is 0-based index. BIT is 1-based.
            # cnt_V_left: count of indices < p (0..p-1)
            # query(p) sums 1..p => indices 0..p-1
            cnt_V_left = bit_pos.query(p)
            
            # cnt_V_right: count of indices > p (p+1..N-1)
            # query(N) - query(p+1) sums indices p+1..N-1
            cnt_V_right = bit_pos.query(N) - bit_pos.query(p + 1)
            
            # cnt_U_left: count of wrapped elements < p
            # Total elements < p is p.
            cnt_U_left = p - cnt_V_left
            
            # cnt_U_right: count of wrapped elements > p
            # Total elements > p is N - 1 - p.
            cnt_U_right = (N - 1 - p) - cnt_V_right
            
            # Count V elements with value < target_val
            # We need count of q in V with A[q] < target_val.
            # BIT_val stores A[q] + 1.
            # We want A[q] <= target_val - 1.
            # So query(target_val).
            cnt_V_small_val = bit_val.query(target_val)
            
            # Logic:
            # Gain inversions:
            #   - With V elements to the left (q < p): V elements increase by 1, p becomes 0. 
            #     Since V elements are >= 0, new value >= 1 > 0. Always inversion.
            #     Count: cnt_V_left
            #   - With U elements to the left (s < p): U elements increase by 1, p becomes 0.
            #     U elements are >= 0, new value >= 1 > 0. Always inversion.
            #     Count: cnt_U_left
            # Total Gain = cnt_V_left + cnt_U_left
            
            # Lose inversions:
            #   - With V elements to the right (q > p): 
            #     Old: p(M-1) > q(v_q). New: p(0) > q(v_q+1).
            #     Lose if M-1 > v_q. Since v_q <= M-1, this is true unless v_q = M-1.
            #     v_q = M-1 iff A[q] = M-1-k = target_val.
            #     So we lose for all q > p except those with value M-1.
            #     Count: cnt_V_right - (count of wrapping elements to the right)
            #   - With U elements to the right (s > p):
            #     Old: p(M-1) > s(v_s). New: p(0) > s(v_s+1).
            #     Lose if M-1 > v_s. Always true since v_s < M.
            #     Count: cnt_U_right
            # Total Lose = (cnt_V_right - right_wrap_count) + cnt_U_right
            
            lose = (cnt_V_right - right_wrap_count) + cnt_U_right
            gain = cnt_V_left + cnt_U_left
            
            delta = gain - lose
            curr_inv += delta
            
            # Update BITs: remove p from V
            bit_pos.update(p + 1, -1)
            bit_val.update(target_val + 1, -1)
            
            right_wrap_count += 1

if __name__ == '__main__':
    solve()