import sys

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    A = list(map(int, input_data[idx:idx+N])); idx += N
    B = list(map(int, input_data[idx:idx+N])); idx += N
    K = int(input_data[idx]); idx += 1
    queries = []
    for _ in range(K):
        X = int(input_data[idx]); idx += 1
        Y = int(input_data[idx]); idx += 1
        queries.append((X, Y))
    
    # Collect distinct X and Y values from queries
    distinct_X = sorted(set(q[0] for q in queries))
    distinct_Y = sorted(set(q[1] for q in queries))
    
    # Build sorted prefixes for only the required indices
    # We use incremental merging: process indices in order, sort new chunk, merge with existing
    def build_sorted_prefixes(arr, indices):
        result = {}
        current_sorted = []
        prev = 0
        for x in indices:
            # Elements arr[prev..x-1] are new
            new_elems = arr[prev:x]
            new_elems.sort()
            if not current_sorted:
                current_sorted = new_elems
            else:
                # Merge two sorted lists efficiently
                a = current_sorted
                b = new_elems
                la, lb = len(a), len(b)
                merged = []
                i = j = 0
                while i < la and j < lb:
                    if a[i] <= b[j]:
                        merged.append(a[i])
                        i += 1
                    else:
                        merged.append(b[j])
                        j += 1
                if i < la:
                    merged.extend(a[i:])
                if j < lb:
                    merged.extend(b[j:])
                current_sorted = merged
            result[x] = current_sorted
            prev = x
        return result
    
    # Compute sorted prefixes for A and B
    sorted_A_map = build_sorted_prefixes(A, distinct_X)
    sorted_B_map = build_sorted_prefixes(B, distinct_Y)
    
    # Precompute prefix sums of A and B for O(1) sum queries
    # prefix_A[i] = sum of A[0..i-1]
    prefix_A = [0] * (N + 1)
    for i in range(N):
        prefix_A[i+1] = prefix_A[i] + A[i]
    prefix_B = [0] * (N + 1)
    for i in range(N):
        prefix_B[i+1] = prefix_B[i] + B[i]
    
    # For each query, compute the sum using the two-pointer technique
    out = []
    for X, Y in queries:
        a = sorted_A_map[X]
        b = sorted_B_map[Y]
        len_a = len(a)
        len_b = len(b)
        
        # Compute sum of min(a_i, b_j) using two pointers
        sum_min = 0
        i = j = 0
        while i < len_a and j < len_b:
            if a[i] <= b[j]:
                # a[i] is the minimum for all remaining b's
                sum_min += a[i] * (len_b - j)
                i += 1
            else:
                # b[j] is the minimum for all remaining a's
                sum_min += b[j] * (len_a - i)
                j += 1
        
        # Use prefix sums for O(1) sum queries
        sum_a = prefix_A[X]
        sum_b = prefix_B[Y]
        
        # S = sum_a * len_b + sum_b * len_a - 2 * sum_min
        S = sum_a * len_b + sum_b * len_a - 2 * sum_min
        out.append(str(S))
    
    sys.stdout.write('\n'.join(out))

solve()