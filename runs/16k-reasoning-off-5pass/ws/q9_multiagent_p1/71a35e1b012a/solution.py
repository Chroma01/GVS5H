import sys

# Increase recursion depth just in case, though not strictly needed for this iterative solution
sys.setrecursionlimit(2000000)

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

    intervals = []
    for _ in range(M):
        l = int(next(iterator))
        r = int(next(iterator))
        intervals.append((l, r))

    # Store intervals with original indices for output construction
    # Format: (L, R, original_index)
    intervals_idx = []
    for i in range(M):
        intervals_idx.append((intervals[i][0], intervals[i][1], i))
    
    # Sort intervals by L, then by R
    intervals_idx.sort(key=lambda x: (x[0], x[1]))
    
    # Check for Cost 1: Is there an interval [1, N]?
    # If so, we can just pick Operation 1 for that interval.
    for l, r, idx in intervals_idx:
        if l == 1 and r == N:
            ans_cost = 1
            ans_ops = [0] * M
            ans_ops[idx] = 1
            print(ans_cost)
            print(*(ans_ops))
            return

    # Check for Cost 2
    # There are two ways to achieve cost 2:
    # 1. Disjoint Intervals: If there exist two disjoint intervals [L_i, R_i] and [L_k, R_k],
    #    we can choose Operation 2 for both. The union of their complements covers [1, N].
    #    Disjoint means R_i < L_k or R_k < L_i.
    # 2. Subset Intervals: If there exist two distinct intervals [L_i, R_i] and [L_k, R_k]
    #    such that [L_i, R_i] is a subset of [L_k, R_k] (i.e., L_k <= L_i and R_i <= R_k),
    #    we can choose Operation 2 for i and Operation 1 for k.
    #    The intersection of the Op2 intervals is [L_i, R_i], which is covered by Op1 interval [L_k, R_k].
    
    found_disjoint = False
    found_subset = False
    idx1 = -1
    idx2 = -1
    
    # --- Check Disjoint ---
    # Sort by L. If L_j > max_R_so_far, then interval j is disjoint from the interval that set max_R.
    max_r = -1
    best_i = -1
    
    for l, r, idx in intervals_idx:
        if l > max_r:
            # Disjoint from the interval that set max_r
            found_disjoint = True
            idx1 = best_i
            idx2 = idx
            break
        if r > max_r:
            max_r = r
            best_i = idx
            
    if found_disjoint:
        ans_cost = 2
        ans_ops = [0] * M
        ans_ops[idx1] = 2
        ans_ops[idx2] = 2
        print(ans_cost)
        print(*(ans_ops))
        return

    # --- Check Subset ---
    # We need i, k such that [L_i, R_i] is subset of [L_k, R_k] and i != k.
    # Since sorted by L, for k > i, L_k >= L_i.
    # We need R_k >= R_i.
    # So we need to find if there exists k > i such that R_k >= R_i.
    # We can iterate from right to left, maintaining max_R_suffix.
    
    max_r_suffix = -1
    best_k_idx = -1
    
    for i in range(M - 1, -1, -1):
        l, r, idx = intervals_idx[i]
        if max_r_suffix >= r:
            # Found k (best_k_idx) such that R_k >= R_i and L_k >= L_i (since k > i)
            # Thus [L_i, R_i] is a subset of [L_k, R_k].
            found_subset = True
            idx1 = idx
            idx2 = best_k_idx
            break
        if r > max_r_suffix:
            max_r_suffix = r
            best_k_idx = idx
            
    if found_subset:
        ans_cost = 2
        ans_ops = [0] * M
        # S2 = {idx1}, S1 = {idx2}
        # Intersection of S2 is [L_{idx1}, R_{idx1}].
        # S1 must cover it. idx2 covers [L_{idx2}, R_{idx2}] which contains [L_{idx1}, R_{idx1}].
        ans_ops[idx1] = 2
        ans_ops[idx2] = 1
        print(ans_cost)
        print(*(ans_ops))
        return

    # If neither Cost 1 nor Cost 2 is possible, output -1.
    print("-1")

if __name__ == '__main__':
    solve()