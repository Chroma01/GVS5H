import sys

# Increase recursion depth just in case, though not used here
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

    # Sort P to allow early breaking in the loop
    P.sort()

    # Binary search for the maximum marginal cost threshold T
    # such that the total cost of all units with marginal cost <= T is <= M.
    # The marginal cost of the k-th unit of product i is (2k-1)*P_i.
    # The total cost to buy k units of product i is k^2 * P_i.
    
    low = 0
    # The maximum possible marginal cost we might consider is bounded by M.
    # Even if we buy 1 unit, its cost is P_i <= 2*10^9, but if M is large,
    # we might buy many units. The marginal cost of the last unit cannot exceed M.
    high = M + 2 
    best_T = 0
    best_cost = 0
    best_cnt = 0

    while low <= high:
        mid = (low + high) // 2
        current_cost = 0
        current_cnt = 0
        possible = True
        
        # Iterate through sorted products to sum up costs for units with marginal cost <= mid
        for p in P:
            # If the base cost P_i is already greater than mid, 
            # then the 1st unit (marginal cost P_i) is too expensive.
            # Since P is sorted, all subsequent products will also be too expensive.
            if p > mid:
                break
            
            # We want to find the largest k such that the marginal cost of the k-th unit <= mid.
            # Marginal cost of k-th unit = (2k - 1) * p
            # (2k - 1) * p <= mid
            # 2k - 1 <= mid // p
            # 2k <= mid // p + 1
            # k = (mid // p + 1) // 2
            
            q = mid // p
            k = (q + 1) // 2
            
            if k == 0:
                continue
            
            # The cost to buy k units is k^2 * p
            term = k * k * p
            
            # Pruning: if adding this term exceeds M, we can stop early
            if current_cost + term > M:
                possible = False
                break
            
            current_cost += term
            current_cnt += k
        
        if possible:
            best_T = mid
            best_cost = current_cost
            best_cnt = current_cnt
            low = mid + 1
        else:
            high = mid - 1

    # After finding the best threshold T (best_T), we have bought 'best_cnt' units
    # with total cost 'best_cost'. We might have some remaining budget.
    # The next cheapest units available have marginal cost = best_T + 1.
    # We need to check how many products offer a unit with exactly this marginal cost.
    
    rem = M - best_cost
    next_cost = best_T + 1
    
    # If best_T was 0, next_cost is 1. This is valid since P_i >= 1.
    # We count how many products i have a unit with marginal cost == next_cost.
    # Condition: (2k - 1) * P_i = next_cost for some integer k >= 1.
    # This implies next_cost must be divisible by P_i, and (next_cost / P_i) must be odd.
    
    count_next = 0
    for p in P:
        if next_cost % p == 0:
            x = next_cost // p
            if x % 2 == 1:
                count_next += 1
    
    # We can buy at most 'count_next' units of this marginal cost.
    # Also limited by the remaining budget.
    if next_cost > 0:
        can_buy = min(count_next, rem // next_cost)
        total_units = best_cnt + can_buy
    else:
        total_units = best_cnt

    print(total_units)

if __name__ == '__main__':
    solve()