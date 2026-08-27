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

    # Part 1: Calculate sum of D(L, R)
    # D(L, R) is the number of distinct values in A[L...R].
    # Sum D(L, R) = sum over i of (i - prev_occurrence_index[i]) * (N - i)
    # where prev_occurrence_index[i] is the index of the previous occurrence of A[i].
    # The term (i - prev_occurrence_index[i]) counts the number of valid start positions L.
    # The term (N - i) counts the number of valid end positions R.
    
    last_pos = {}
    sum_D = 0
    for i in range(N):
        val = A[i]
        if val in last_pos:
            count_L = i - last_pos[val]
        else:
            count_L = i + 1 # i - (-1)
        
        count_R = N - i
        sum_D += count_L * count_R
        last_pos[val] = i

    # Part 2: Calculate sum of G(L, R)
    # G(L, R) is the number of x such that x and x+1 both appear in A[L...R].
    # We sum over all x from 1 to N-1.
    # For a fixed x, we need the number of subarrays containing at least one x AND at least one x+1.
    # Let U be positions of x, W be positions of x+1.
    # Count = |S_U| + |S_W| - |S_U U S_W|
    # |S_U| = Total - (subarrays with no x)
    # |S_W| = Total - (subarrays with no x+1)
    # |S_U U S_W| = Total - (subarrays with neither x nor x+1)
    # So Count = (Total - no_x) + (Total - no_x+1) - (Total - neither)
    #          = Total - no_x - no_x+1 + neither
    
    # Helper to calculate number of subarrays with no occurrences given a list of indices
    def count_no_occurrences(indices, N):
        # indices is sorted list of positions (0-based)
        # Gaps: [0, indices[0]-1], [indices[0]+1, indices[1]-1], ..., [indices[-1]+1, N-1]
        total = 0
        prev = -1
        for idx in indices:
            length = idx - prev - 1
            if length > 0:
                total += length * (length + 1) // 2
            prev = idx
        # Gap after last occurrence
        length = N - 1 - prev
        if length > 0:
            total += length * (length + 1) // 2
        return total

    # Group positions by value
    pos_map = {}
    for i in range(N):
        val = A[i]
        if val not in pos_map:
            pos_map[val] = []
        pos_map[val].append(i)

    sum_G = 0
    total_subarrays = N * (N + 1) // 2

    # Iterate over distinct values present in the array
    # We only care about x if x exists in array. If x doesn't exist, no subarray contains x, so contribution is 0.
    # Similarly if x+1 doesn't exist.
    
    for x in pos_map:
        if x + 1 not in pos_map:
            continue
        
        U = pos_map[x]
        W = pos_map[x + 1]
        
        # Calculate terms
        no_x = count_no_occurrences(U, N)
        no_x_plus_1 = count_no_occurrences(W, N)
        
        # Union of indices: subarrays containing neither x nor x+1
        # We need the set of indices where A[i] is NOT x AND A[i] is NOT x+1.
        # This corresponds to the complement of (U U W) in [0, N-1].
        # The gaps in the combined set U U W represent regions with neither.
        combined = sorted(U + W)
        neither = count_no_occurrences(combined, N)
        
        count_for_x = total_subarrays - no_x - no_x_plus_1 + neither
        sum_G += count_for_x

    # Result
    ans = sum_D - sum_G
    print(ans)

if __name__ == '__main__':
    solve()