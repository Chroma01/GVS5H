import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
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

    # pos[v] will store the list of 1-based indices where value v appears.
    # Values are in range [1, N]. We allocate N + 2 to be safe.
    pos = [[] for _ in range(N + 2)]
    for idx, val in enumerate(A):
        pos[val].append(idx + 1)

    # Total number of subarrays for an array of length N
    total_subarrays = N * (N + 1) // 2

    # Helper function to calculate the number of subarrays that do NOT contain
    # any index from the given sorted list 'indices'.
    # This is done by summing the number of subarrays within the gaps between
    # consecutive occurrences (including the boundaries 0 and N+1).
    def count_missing(indices):
        if not indices:
            # If the value never appears, all subarrays are "missing" it.
            return total_subarrays
        
        count = 0
        prev = 0
        for curr in indices:
            # Gap between prev occurrence and current occurrence
            length = curr - prev
            count += length * (length + 1) // 2
            prev = curr
        # Gap after the last occurrence up to N
        length = (N + 1) - prev
        count += length * (length + 1) // 2
        return count

    # Part 1: Calculate Sum of |Unique(A[L...R])|
    # The contribution of a specific value 'v' to the sum of unique counts is:
    # (Total Subarrays) - (Subarrays that do NOT contain 'v')
    sum_unique = 0
    for v in range(1, N + 1):
        if pos[v]:
            missing = count_missing(pos[v])
            sum_unique += (total_subarrays - missing)
        # If pos[v] is empty, missing == total_subarrays, so contribution is 0.

    # Part 2: Calculate Sum of C(L, R)
    # C(L, R) is the number of pairs (x, x+1) such that both x and x+1 appear in A[L...R].
    # We iterate over each possible value v from 1 to N-1 and calculate the number of
    # subarrays that contain BOTH v and v+1.
    # Using Inclusion-Exclusion Principle:
    # Count(both) = Total - Count(missing v) - Count(missing v+1) + Count(missing both)
    # Count(missing both) corresponds to subarrays lying entirely within the gaps of the union of indices.
    
    sum_pairs = 0
    
    for v in range(1, N):
        next_v = v + 1
        
        idx_v = pos[v]
        idx_next = pos[next_v]
        
        # Calculate missing counts for individual values
        miss_v = count_missing(idx_v)
        miss_next = count_missing(idx_next)
        
        # Calculate missing both: union of indices
        # Since idx_v and idx_next are sorted, we merge them in linear time.
        merged = []
        i, j = 0, 0
        len_v = len(idx_v)
        len_next = len(idx_next)
        
        while i < len_v and j < len_next:
            if idx_v[i] < idx_next[j]:
                merged.append(idx_v[i])
                i += 1
            else:
                merged.append(idx_next[j])
                j += 1
        
        while i < len_v:
            merged.append(idx_v[i])
            i += 1
            
        while j < len_next:
            merged.append(idx_next[j])
            j += 1
            
        miss_both = count_missing(merged)
        
        # Number of subarrays containing both v and v+1
        count_both = total_subarrays - miss_v - miss_next + miss_both
        sum_pairs += count_both

    # The answer is Sum(|Unique|) - Sum(C)
    ans = sum_unique - sum_pairs
    print(ans)

if __name__ == '__main__':
    solve()