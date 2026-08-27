import sys

# Increase recursion depth just in case
sys.setrecursionlimit(200005)

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
    for i in range(M):
        l = int(next(iterator))
        r = int(next(iterator))
        intervals.append((l, r))

    # Precompute max_r_le for efficient cover cost calculation
    # max_r_le[i] stores the maximum R of any interval with L <= i
    max_r_le = [-1] * (N + 2)
    
    max_r_at_L = [-1] * (N + 2)
    for l, r in intervals:
        if r > max_r_at_L[l]:
            max_r_at_L[l] = r
            
    current_max = -1
    for i in range(1, N + 2):
        if max_r_at_L[i] > current_max:
            current_max = max_r_at_L[i]
        max_r_le[i] = current_max
        
    def get_cover_cost(L, R):
        if L > R:
            return 0
        if max_r_le[L] < L:
            return float('inf')
        
        curr = L
        count = 0
        while curr <= R:
            best_r = max_r_le[curr]
            if best_r < curr:
                return float('inf')
            curr = best_r + 1
            count += 1
            if curr > R:
                break
        return count

    # Calculate base costs for all intervals (for |S2|=1)
    base_costs = []
    for l, r in intervals:
        c = get_cover_cost(l, r)
        base_costs.append(c)
        
    ans_cost = float('inf')
    ans_ops = None
    
    # Case 1: |S2| = 1
    # Check if any single interval covers [1, N]
    has_full = False
    full_idx = -1
    for i, (l, r) in enumerate(intervals):
        if l == 1 and r == N:
            has_full = True
            full_idx = i
            break
            
    if has_full:
        ans_cost = 1
        ans_ops = [0] * M
        ans_ops[full_idx] = 1
        print(ans_cost)
        print(*(ans_ops))
        return

    # Check min(1 + base_cost)
    min1_cost = float('inf')
    min1_idx = -1
    for i in range(M):
        c = 1 + base_costs[i]
        if c < min1_cost:
            min1_cost = c
            min1_idx = i
            
    # Case 2: |S2| = 2
    # Check if any pair is disjoint -> Cost 2
    # Sort by L, then R
    sorted_with_idx = sorted([(l, r, i) for i, (l, r) in enumerate(intervals)], key=lambda x: (x[0], x[1]))
    min_r_prefix = float('inf')
    disjoint_found = False
    disjoint_pair = (-1, -1)
    
    for l, r, idx in sorted_with_idx:
        if min_r_prefix < l:
            disjoint_found = True
            disjoint_pair = (min_r_idx, idx)
            break
        if r < min_r_prefix:
            min_r_prefix = r
            min_r_idx = idx
            
    if disjoint_found:
        ans_cost = 2
        ops = [0] * M
        ops[disjoint_pair[0]] = 2
        ops[disjoint_pair[1]] = 2
        print(ans_cost)
        print(*(ops))
        return

    # Case 3: |S2| = 2 with non-empty intersection
    # Check if any interval k contains at least 2 other intervals -> Cost 3
    # We need to find if there exists k such that count(j != k | j contained in k) >= 2
    
    # Sort by L, then R
    sorted_with_idx = sorted([(l, r, i) for i, (l, r) in enumerate(intervals)], key=lambda x: (x[0], x[1]))
    
    # Coordinate compress R for Fenwick tree
    all_rs = sorted(list(set([r for l, r in intervals])))
    r_map = {val: i + 1 for i, val in enumerate(all_rs)}
    max_r_idx = len(all_rs)
    
    bit = [0] * (max_r_idx + 1)
    
    def update(idx, val):
        while idx <= max_r_idx:
            bit[idx] += val
            idx += idx & (-idx)
            
    def query(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s
        
    contained_pair_found = False
    contained_idx = -1
    
    # Iterate backwards to count contained intervals
    for i in range(M - 1, -1, -1):
        l, r, idx = sorted_with_idx[i]
        update(r_map[r], 1)
        cnt = query(r_map[r])
        # cnt includes self. If cnt >= 2, then there is at least one other interval contained in i.
        if cnt >= 2:
            contained_pair_found = True
            contained_idx = idx
            break
            
    if contained_pair_found:
        ans_cost = 3
        # Reconstruct solution
        # We need to find the specific interval in the original list
        # The loop above used sorted_with_idx[i]. Let's re-run to find the specific indices.
        
        # Reset BIT
        bit = [0] * (max_r_idx + 1)
        container_idx = -1
        for i in range(M - 1, -1, -1):
            l, r, idx = sorted_with_idx[i]
            update(r_map[r], 1)
            cnt = query(r_map[r])
            if cnt >= 2:
                # Found the container
                container_idx = idx
                break
        
        # Find two distinct intervals contained in container
        found_j = -1
        found_k = -1
        for j, (jl, jr) in enumerate(intervals):
            if j == container_idx:
                continue
            if intervals[container_idx][0] <= jl and intervals[container_idx][1] >= jr:
                if found_j == -1:
                    found_j = j
                else:
                    found_k = j
                    break
        
        ops = [0] * M
        ops[container_idx] = 1
        ops[found_j] = 2
        ops[found_k] = 2
        print(ans_cost)
        print(*(ops))
        return

    # Case 4: General
    # If no disjoint pair and no contained pair, the answer is min(1 + base_cost)
    # Note: If contained pair exists, cost is 3. If min(1+base) is 2, we prefer 2.
    # If min(1+base) is 3, it's equal.
    # If min(1+base) > 3, we might have missed something?
    # Actually, if contained pair exists, cost is 3.
    # If min(1+base) is 4, we should output 3.
    # So we need to compare min1_cost and 3 if contained_pair_found.
    # But we already returned if contained_pair_found.
    # So if we are here, contained_pair_found is False.
    # Thus, we cannot achieve cost 3 via contained pair.
    # Can we achieve cost 3 via other means?
    # Cost 3 via pairs requires cover_cost(intersection) = 1.
    # This implies intersection is covered by 1 interval.
    # i.e., intersection \subseteq k.
    # This is exactly the condition "k contains intersection of i and j".
    # If i and j are contained in k, then intersection is contained in k.
    # If i is not contained in k, but intersection is?
    # Intersection = [max(Li, Lj), min(Ri, Rj)].
    # If this is contained in k, then L_k <= max(Li, Lj) and min(Ri, Rj) <= R_k.
    # This implies L_k <= Li and L_k <= Lj, and Ri <= R_k and Rj <= R_k.
    # So i and j are both contained in k.
    # So the condition "intersection covered by k" is equivalent to "i and j contained in k".
    # So if contained_pair_found is False, we cannot achieve cost 3 via pairs.
    # So the answer is indeed min(1 + base_cost).
    
    ans_cost = min1_cost
    ops = [0] * M
    ops[min1_idx] = 1
    print(ans_cost)
    print(*(ops))

solve()