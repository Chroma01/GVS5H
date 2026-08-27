import sys
import heapq

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        P = []
        for _ in range(N):
            P.append(int(next(iterator)))
    except StopIteration:
        return

    # Binary search for the largest T such that cost(T) <= M
    # T is the threshold for marginal costs.
    # Marginal cost of j-th unit of product i is (2*j - 1) * P_i.
    # We buy j-th unit if (2*j - 1) * P_i <= T  =>  j <= (T / P_i + 1) / 2
    # So k_i = floor((T + P_i) / (2 * P_i))
    
    low = 0
    high = 4 * 10**18 + 100 # Sufficiently large upper bound for T
    best_T = 0
    best_cost = 0
    best_X = 0
    
    # We want the largest T such that cost <= M.
    # However, we also need to track the state (k_i, cost, X) for that T.
    
    # To avoid recomputing everything, we can just store the best state.
    
    ans_T = 0
    ans_cost = 0
    ans_X = 0
    
    while low <= high:
        mid = (low + high) // 2
        
        # Calculate total units and cost for threshold mid
        total_units = 0
        total_cost = 0
        
        # Optimization: if total_cost exceeds M early, break
        # But we need to compute all to be sure? No, cost is monotonic in k_i, and k_i is monotonic in T.
        # So if total_cost > M, we can stop early? Yes, but we must be careful with overflow.
        # Python handles large integers, so overflow is not an issue, but speed might be.
        
        for p in P:
            # k_i = (mid + p) // (2 * p)
            # To avoid division by zero, but P_i >= 1.
            k = (mid + p) // (2 * p)
            if k > 0:
                total_units += k
                total_cost += k * k * p
        
        if total_cost <= M:
            ans_T = mid
            ans_cost = total_cost
            ans_X = total_units
            low = mid + 1
        else:
            high = mid - 1
            
    # Now we have the base state: ans_X units, ans_cost cost, with k_i = (ans_T + P_i) // (2 * P_i)
    # We need to add more units if possible.
    # The next unit for product i has marginal cost (2 * k_i + 1) * P_i.
    
    # Compute current k_i for each product
    k_list = []
    for p in P:
        k = (ans_T + p) // (2 * p)
        k_list.append(k)
        
    # Min-heap for marginal costs of the next unit
    # Each element: (marginal_cost, index_in_P)
    heap = []
    for i, p in enumerate(P):
        k = k_list[i]
        # Marginal cost of the (k+1)-th unit
        mc = (2 * k + 1) * p
        heapq.heappush(heap, (mc, i))
        
    current_cost = ans_cost
    current_units = ans_X
    
    while heap:
        mc, idx = heapq.heappop(heap)
        
        if current_cost + mc > M:
            # Cannot afford this unit, and since heap is min-heap, cannot afford any subsequent units
            break
            
        # Buy this unit
        current_cost += mc
        current_units += 1
        k_list[idx] += 1
        
        # Push the next marginal cost for this product
        p = P[idx]
        k = k_list[idx]
        next_mc = (2 * k + 1) * p
        heapq.heappush(heap, (next_mc, idx))
        
    print(current_units)

solve()