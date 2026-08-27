import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    iterator = iter(data)
    N = int(next(iterator))
    A = [int(next(iterator)) for _ in range(N)]
    B = [int(next(iterator)) for _ in range(N)]
    K = int(next(iterator))
    queries = []
    for k in range(K):
        X = int(next(iterator))
        Y = int(next(iterator))
        queries.append((X, Y, k))
    
    # Coordinate compression for values in A and B
    all_vals = sorted(set(A + B))
    comp_map = {val: i+1 for i, val in enumerate(all_vals)}
    max_comp = len(all_vals)
    
    # Fenwick Tree (Binary Indexed Tree) for counts and sums
    bit_count = [0] * (max_comp + 1)
    bit_sum = [0] * (max_comp + 1)
    
    def update(idx, val_count, val_sum):
        while idx <= max_comp:
            bit_count[idx] += val_count
            bit_sum[idx] += val_sum
            idx += idx & (-idx)
            
    def query(idx):
        c = 0
        s = 0
        while idx > 0:
            c += bit_count[idx]
            s += bit_sum[idx]
            idx -= idx & (-idx)
        return c, s
        
    # Group queries by Y
    queries_by_Y = {}
    for X, Y, k in queries:
        if Y not in queries_by_Y:
            queries_by_Y[Y] = []
        queries_by_Y[Y].append((X, k))
        
    # Sort distinct Y values
    sorted_Y = sorted(queries_by_Y.keys())
    
    # Precompute prefix sums for B? No, we use Fenwick Tree.
    # We'll process Y from 1 to N, but only up to the max Y in queries.
    # However, we can iterate Y from 1 to N, and for each Y, update the Fenwick Tree with B[Y-1] (0-indexed).
    
    # Current total sum of B[1..Y]
    current_total_sum_B = 0
    current_Y = 0
    
    # To store answers
    answers = [0] * K
    
    # We'll iterate Y from 1 to N, but only process when Y is in sorted_Y
    # But we need to update the Fenwick Tree for each Y from 1 to max_Y.
    max_Y_needed = sorted_Y[-1] if sorted_Y else 0
    
    # Precompute compressed values for A and B
    A_comp = [comp_map[a] for a in A]
    B_comp = [comp_map[b] for b in B]
    
    # Process each Y in sorted order
    for Y in sorted_Y:
        # Update Fenwick Tree for B[current_Y] to B[Y-1]
        while current_Y < Y:
            # current_Y is 0-indexed, so B[current_Y] is the (current_Y+1)-th element
            val = B[current_Y]
            c_val = B_comp[current_Y]
            current_total_sum_B += val
            update(c_val, 1, val)
            current_Y += 1
            
        # Now Fenwick Tree represents B[1..Y]
        # For each query with this Y, compute the answer
        for X, k in queries_by_Y[Y]:
            total_ans = 0
            # Iterate over A[0..X-1]
            for i in range(X):
                a_val = A[i]
                a_comp = A_comp[i]
                # Query Fenwick Tree for count and sum <= a_val
                cnt_le, sum_le = query(a_comp)
                cnt_gt = Y - cnt_le
                sum_gt = current_total_sum_B - sum_le
                term = a_val * cnt_le - sum_le + sum_gt - a_val * cnt_gt
                total_ans += term
            answers[k] = total_ans
            
    # Print answers
    for ans in answers:
        print(ans)

if __name__ == "__main__":
    main()