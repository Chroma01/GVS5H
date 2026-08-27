import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

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

    # Store positions of each value
    # Values are 1-based, up to N. Indices are 0-based.
    pos = {}
    for idx, val in enumerate(A):
        if val not in pos:
            pos[val] = []
        pos[val].append(idx)

    # Precompute gaps for each value v.
    # A gap is defined by start and end indices [a, b] such that no occurrence of v is in [a, b].
    # If v is not present, the whole array [0, N-1] is one gap.
    gaps = {}
    for v in pos:
        occs = pos[v]
        current_start = 0
        for p in occs:
            if p > current_start:
                # Gap from current_start to p-1
                gaps[v].append((current_start, p - 1))
            current_start = p + 1
        if current_start < N:
            # Gap from current_start to N-1
            gaps[v].append((current_start, N - 1))
    
    # If a value v is not in pos, it has no occurrences, so the only gap is [0, N-1]
    for v in range(1, N + 1):
        if v not in pos:
            gaps[v] = [(0, N - 1)]

    total_ops = 0
    
    # Helper to count pairs (L, R) in range [a, b] containing at least one occurrence of x
    # We calculate Total pairs in [a, b] - Sum of pairs in intervals between consecutive occurrences of x.
    def count_in_gap(a, b, x):
        if a > b:
            return 0
        
        occs_x = pos.get(x, [])
        
        # Find occurrences of x within [a, b]
        # Since occs_x is sorted, we can use binary search or just iterate.
        # Given the structure, we can just filter.
        relevant = [p for p in occs_x if a <= p <= b]
        
        if not relevant:
            return 0
        
        # Total pairs in [a, b]
        length = b - a + 1
        total_pairs = length * (length + 1) // 2
        
        bad_pairs = 0
        
        # Interval before first relevant occurrence: [a, relevant[0]-1]
        first_p = relevant[0]
        if first_p > a:
            k = first_p - a
            bad_pairs += k * (k + 1) // 2
        
        # Intervals between consecutive relevant occurrences
        for i in range(len(relevant) - 1):
            u = relevant[i]
            v = relevant[i+1]
            # Range [u+1, v-1]
            if v > u + 1:
                k = v - u - 1
                bad_pairs += k * (k + 1) // 2
        
        # Interval after last relevant occurrence: [relevant[-1]+1, b]
        last_p = relevant[-1]
        if last_p < b:
            k = b - last_p
            bad_pairs += k * (k + 1) // 2
            
        return total_pairs - bad_pairs

    # Iterate over all possible values x present in the array
    # We sum the contribution of each x: count pairs (L, R) where x is present AND x-1 is absent.
    # x-1 is absent in A[L..R] means [L, R] must be contained within a "gap" of x-1.
    for x in pos:
        prev_val = x - 1
        gap_list = gaps.get(prev_val, [(0, N - 1)])
        
        for a, b in gap_list:
            cnt = count_in_gap(a, b, x)
            total_ops += cnt

    print(total_ops)

if __name__ == '__main__':
    solve()