import sys
from bisect import bisect_left, bisect_right

# Increase recursion depth just in case, though not strictly needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Use fast I/O
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
        l = int(next(iterator))
        r = int(next(iterator))
        contests.append((l, r))
        
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))
        
    # Maximum possible rating
    # Initial max X is 500,000. Max increase is N (200,000).
    # So max rating is 700,000. Let's allocate a bit more for safety.
    MAX_VAL = 500000 + N + 5
    
    # BIT Implementation (Fenwick Tree)
    # 1-indexed BIT
    # We use a difference array approach where bit stores the increments.
    # The actual rating for initial value v is v + prefix_sum(bit, v).
    bit = [0] * (MAX_VAL + 2)
    
    def update_bit(idx, val):
        while idx < len(bit):
            bit[idx] += val
            idx += idx & (-idx)
            
    def query_bit(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s
    
    # We need to find the range [start, end] of indices v such that:
    # L <= current_ans[v] <= R
    # i.e., L <= v + query_bit(v) <= R
    
    # Helper to get current_ans
    def get_ans(v):
        return v + query_bit(v)
    
    # Binary search for lower bound (first v such that get_ans(v) >= L)
    def find_lower_bound(L):
        low = 1
        high = MAX_VAL
        ans = -1
        while low <= high:
            mid = (low + high) // 2
            if get_ans(mid) >= L:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans

    # Binary search for upper bound (first v such that get_ans(v) > R)
    def find_upper_bound(R):
        low = 1
        high = MAX_VAL
        ans = MAX_VAL + 1
        while low <= high:
            mid = (low + high) // 2
            if get_ans(mid) > R:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans

    # Process contests
    for l, r in contests:
        start = find_lower_bound(l)
        if start == -1:
            continue
        
        end_plus = find_upper_bound(r)
        
        # The range of starting values that get incremented is [start, end_plus - 1]
        # We need to increment inc[v] for v in [start, end_plus - 1]
        # This corresponds to updating the difference array:
        # diff[start] += 1
        # diff[end_plus] -= 1
        
        if start < end_plus:
            update_bit(start, 1)
            update_bit(end_plus, -1)
            
    # Answer queries
    results = []
    for x in queries:
        # Ensure x is within bounds
        if x >= len(bit):
            results.append(x)
        else:
            results.append(x + query_bit(x))
            
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()