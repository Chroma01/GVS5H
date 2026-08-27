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
        M = int(next(iterator))
        P = []
        for _ in range(N):
            P.append(int(next(iterator)))
    except StopIteration:
        return

    # Binary search for the maximum marginal cost threshold T
    # such that the cost to buy ALL units with marginal cost <= T is <= M.
    # The marginal cost of the k-th unit of product i is (2k-1)*P_i.
    # We want to find the largest T where sum(k_i^2 * P_i) <= M.
    # For a given T and price P_i, the max k satisfies (2k-1)*P_i <= T.
    # This simplifies to k = (floor(T/P_i) + 1) // 2.
    
    low = 0
    high = 2 * 10**18  # Sufficiently large upper bound since M <= 10^18 and P_i >= 1
    best_T = 0
    
    # We want to find the largest T such that cost(T) <= M.
    # cost(T) is monotonically increasing with T.
    
    while low <= high:
        mid = (low + high) // 2
        
        current_units = 0
        current_cost = 0
        
        # Calculate cost and units for threshold mid
        for p in P:
            if p == 0: 
                # Should not happen based on constraints (P_i >= 1)
                continue
            
            q = mid // p
            k = (q + 1) // 2
            
            if k > 0:
                current_units += k
                # Cost for k units is k^2 * p
                term = k * k * p
                current_cost += term
        
        if current_cost <= M:
            best_T = mid
            low = mid + 1
        else:
            high = mid - 1
            
    # Now best_T is the largest threshold where we can afford ALL units with marginal cost <= best_T.
    # Calculate the exact units and cost for best_T.
    units_at_best_T = 0
    cost_at_best_T = 0
    
    # We also need to find the marginal cost of the NEXT unit for each product to handle the remainder.
    # The next unit count for product i is k_i + 1.
    # Its marginal cost is (2*(k_i+1) - 1) * P_i = (2*k_i + 1) * P_i.
    
    next_costs = []
    
    for p in P:
        q = best_T // p
        k = (q + 1) // 2
        
        if k > 0:
            units_at_best_T += k
            cost_at_best_T += k * k * p
        
        # Calculate marginal cost of the (k+1)-th unit
        # If k=0, the 1st unit has marginal cost 1*p
        # Formula: (2*(k+1)-1)*p = (2k+1)*p
        next_marginal = (2 * k + 1) * p
        next_costs.append(next_marginal)
    
    if not next_costs:
        # Should not happen as N >= 1
        print(0)
        return

    min_next_cost = min(next_costs)
    
    remaining_budget = M - cost_at_best_T
    extra_units = remaining_budget // min_next_cost
    
    total_units = units_at_best_T + extra_units
    
    print(total_units)

if __name__ == '__main__':
    solve()