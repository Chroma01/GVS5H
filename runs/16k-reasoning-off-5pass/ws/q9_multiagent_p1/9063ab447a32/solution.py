import sys
import heapq

# Set recursion limit just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

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

    # Binary search for the maximum threshold T such that the cost of taking
    # ALL units with marginal cost <= T is <= M.
    # Marginal cost of k-th unit of product i is (2k-1)*P[i].
    # Condition: (2k-1)*P[i] <= T  =>  2k-1 <= T/P[i]  =>  k <= (T/P[i] + 1)/2
    # So k_i(T) = floor((floor(T/P[i]) + 1) / 2)
    
    # Range for T:
    # Min cost is 1 (if P[i]=1, k=1). Max possible T?
    # If we buy 1 unit of each product, cost is sum(P[i]).
    # If M is large, T can be large.
    # Max M = 10^18. Min P = 1. Max units approx 10^9.
    # Max marginal cost approx 2 * 10^9 * 10^9 = 2 * 10^18.
    # So T range [1, 2*10^18 + 7] is safe.
    
    low = 1
    high = 2 * 10**18 + 7
    ans_T = 0
    cost_at_ans_T = 0
    
    # We need to find the largest T such that total_cost(T) <= M.
    # However, calculating total_cost(T) involves summing P[i]*k_i^2.
    # We must be careful with overflow, but Python handles large integers.
    
    while low <= high:
        mid = (low + high) // 2
        
        total_units = 0
        total_cost = 0
        
        # Optimization: if mid is very large, k_i might be large.
        # k_i approx mid / (2*P[i]).
        # cost approx P[i] * (mid/(2*P[i]))^2 = mid^2 / (4*P[i]).
        # Sum of costs approx mid^2 / 4 * sum(1/P[i]).
        # If mid is too large, cost will exceed M.
        
        for p in P:
            if mid < p:
                k = 0
            else:
                # k = floor((floor(mid/p) + 1) / 2)
                # Let q = mid // p
                # k = (q + 1) // 2
                q = mid // p
                k = (q + 1) // 2
            
            if k > 0:
                total_units += k
                # cost contribution: p * k^2
                total_cost += p * k * k
        
        if total_cost <= M:
            ans_T = mid
            cost_at_ans_T = total_cost
            low = mid + 1
        else:
            high = mid - 1
            
    # Now we have taken all units with marginal cost <= ans_T.
    # Total cost is cost_at_ans_T.
    # Remaining budget R = M - cost_at_ans_T.
    # We need to buy more units with marginal cost > ans_T.
    # The next available unit for product i (after k_i units) has marginal cost:
    # c_i = (2*k_i + 1) * P[i]
    # where k_i is the count we already bought for product i.
    
    R = M - cost_at_ans_T
    pq = []
    
    # Calculate k_i for ans_T and prepare next costs
    # We also need to know which product has which next cost to update it later.
    current_counts = [0] * N
    
    for i in range(N):
        p = P[i]
        if ans_T >= p:
            q = ans_T // p
            k = (q + 1) // 2
            current_counts[i] = k
            if k > 0:
                # Next unit cost
                next_c = (2 * k + 1) * p
                heapq.heappush(pq, (next_c, i))
    
    # Now greedily pick units from the priority queue
    # We need to pick as many as possible such that total cost <= M.
    # Since we already spent cost_at_ans_T, we have R left.
    # We pick units with smallest next_c.
    
    added_units = 0
    
    # We can't simply pop all because R might run out.
    # But we can pop as long as pq is not empty and next_c <= R.
    # Wait, if next_c <= R, we can buy it. Then R -= next_c.
    # Then we push the new next cost for that product.
    # Is it possible that we skip a cheaper unit later? No, pq is sorted.
    # Is it possible that we buy a unit, and then the new next cost is still <= R? Yes.
    # Is it possible that we buy a unit, and then a previously "more expensive" unit becomes cheaper? No.
    # So simple greedy with PQ works.
    
    # However, we must be careful: if next_c > R, we stop?
    # Yes, because all other available units have cost >= next_c > R.
    
    while pq and pq[0][0] <= R:
        cost, idx = heapq.heappop(pq)
        
        # Buy this unit
        R -= cost
        added_units += 1
        
        # Update product idx
        # The unit we just bought was the (current_counts[idx] + 1)-th unit.
        # The next one is (current_counts[idx] + 2)-th unit.
        # Its marginal cost is (2*(current_counts[idx] + 2) - 1) * P[idx]
        # = (2*current_counts[idx] + 3) * P[idx]
        # Alternatively, previous next cost was (2*k + 1)*P. New is (2*(k+1)+1)*P = (2k+3)*P = prev + 2*P.
        
        p = P[idx]
        new_cost = cost + 2 * p
        
        # Push back if we still have budget for it? No, push it, the loop condition checks.
        heapq.heappush(pq, (new_cost, idx))
        
        # Optimization: if R becomes 0, break
        if R == 0:
            break
            
    # Total units = units from ans_T layer + added_units
    # Calculate units from ans_T layer
    total_units_base = sum(current_counts)
    total_units = total_units_base + added_units
    
    print(total_units)

if __name__ == '__main__':
    solve()