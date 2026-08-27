import sys

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        P = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # We want to find the maximum threshold T such that the cost of buying all units 
    # with marginal cost <= T is <= M.
    # The marginal cost of the k-th unit (1-indexed) of product i is (2*k - 1) * P[i].
    # If we set a threshold T, we buy k_i units of product i such that (2*k_i - 1)*P[i] <= T.
    # This implies 2*k_i - 1 <= T / P[i]  =>  2*k_i <= T/P[i] + 1  =>  k_i = floor((T/P[i] + 1) / 2).
    # Since k_i must be integer, k_i = floor((T + P[i]) / (2 * P[i])).
    
    # Binary search range for T:
    # Max possible marginal cost we might pick is bounded.
    # If P=1, M=1e18, k ~ 1e9, marginal cost ~ 2e9.
    # If P=2e9, M=1e18, k=1, marginal cost = 1.
    # Generally, max marginal cost ~ 2 * sqrt(M * P).
    # Max P = 2e9, M = 1e18 => sqrt(2e27) ~ 4.5e13.
    # So T can be up to ~ 9e13. Let's set high = 2 * 10**14 to be safe.
    
    low = 1
    high = 2 * 10**14
    ans_T = 0
    
    # Function to calculate total cost and total units for a given threshold T
    def check(T):
        total_cost = 0
        total_units = 0
        for p in P:
            if T < p:
                k = 0
            else:
                k = (T + p) // (2 * p)
            
            if k > 0:
                total_units += k
                cost = k * k * p
                total_cost += cost
                # Optimization: if total_cost already exceeds M, we can stop early
                if total_cost > M:
                    return total_cost, total_units
        return total_cost, total_units

    # Binary search for the largest T such that cost <= M
    while low <= high:
        mid = (low + high) // 2
        cost, units = check(mid)
        if cost <= M:
            ans_T = mid
            low = mid + 1
        else:
            high = mid - 1
    
    # Now we know we can buy all units with marginal cost <= ans_T.
    # Calculate the exact cost and units for ans_T.
    base_cost = 0
    base_units = 0
    next_marginal_costs = []
    
    for p in P:
        if ans_T < p:
            k = 0
        else:
            k = (ans_T + p) // (2 * p)
        
        if k > 0:
            base_units += k
            base_cost += k * k * p
        
        # The next unit (k+1) has marginal cost (2*(k+1) - 1) * p = (2k + 1) * p
        # We collect these next marginal costs to see if we can afford them with remaining budget.
        next_cost = (2 * k + 1) * p
        next_marginal_costs.append(next_cost)
    
    # Sort the next marginal costs to greedily buy the cheapest ones
    next_marginal_costs.sort()
    
    rem = M - base_cost
    final_units = base_units
    
    for cost in next_marginal_costs:
        if rem >= cost:
            rem -= cost
            final_units += 1
        else:
            break
            
    print(final_units)

if __name__ == '__main__':
    solve()