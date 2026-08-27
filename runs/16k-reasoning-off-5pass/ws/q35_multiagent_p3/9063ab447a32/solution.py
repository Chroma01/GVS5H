import sys

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

    # Sort P to potentially help with cache locality, though not strictly necessary
    P.sort()

    # Binary search for the maximum total units K
    # Lower bound: 0
    # Upper bound: Since min P_i >= 1, max K is when we buy all from cheapest.
    # k^2 * 1 <= M => k <= sqrt(M). M <= 10^18, so k <= 10^9.
    # Let's set high to 2 * 10^9 to be safe.
    low = 0
    high = 2 * 10**9 + 7
    ans = 0

    # Precompute P for faster access
    # P is already a list

    def check(K):
        """
        Check if it is possible to buy K units with cost <= M.
        We minimize the cost by optimally distributing K units among products.
        """
        if K == 0:
            return True
        
        # Binary search for lambda such that sum(floor(lambda / (2*P_i))) >= K
        # The optimal continuous allocation is k_i = lambda / (2*P_i).
        # We want integer k_i = floor(lambda / (2*P_i)).
        # Let's search for the smallest lambda such that sum(floor(lambda / (2*P_i))) >= K.
        
        # Range for lambda:
        # Min lambda: 0
        # Max lambda: If we put all K units on the cheapest product P[0],
        # k_0 = K, so lambda approx 2 * P[0] * K.
        # Max P_i is 2e9, Max K is 2e9, so lambda can be up to 8e18.
        
        l_lambda = 0
        r_lambda = 8 * 10**18 + 100
        best_lambda = r_lambda
        
        while l_lambda <= r_lambda:
            mid = (l_lambda + r_lambda) // 2
            total_units = 0
            for p in P:
                # k_i = floor(mid / (2*p))
                # To avoid float, use integer division
                total_units += mid // (2 * p)
                if total_units >= K:
                    break
            
            if total_units >= K:
                best_lambda = mid
                r_lambda = mid - 1
            else:
                l_lambda = mid + 1
        
        # Now, calculate the base allocation using best_lambda
        k_base = []
        sum_k_base = 0
        for p in P:
            k = best_lambda // (2 * p)
            k_base.append(k)
            sum_k_base += k
        
        # We might have sum_k_base > K due to the floor function and the fact that we found the smallest lambda
        # giving >= K. Actually, the function f(lambda) = sum(floor(lambda/(2*P_i))) is a step function.
        # It's possible that f(best_lambda) > K.
        # In that case, we have "extra" units in the base allocation that we need to remove.
        # Removing a unit from product i reduces cost by: k_i^2 P_i - (k_i-1)^2 P_i = (2k_i - 1) P_i.
        # This is the marginal saving. We want to remove units with the largest marginal saving to minimize the remaining cost?
        # No, we want to achieve exactly K units.
        # If sum_k_base > K, we have excess units. We should remove units that have the highest marginal cost of removal?
        # Wait. The cost function is convex. The base allocation minimizes cost for sum_k_base units.
        # If sum_k_base > K, we need to reduce the total units by (sum_k_base - K).
        # To minimize the cost of the resulting K units, we should remove units that contribute the most to the cost.
        # The cost contribution of the k_i-th unit (1-indexed) is (2k_i - 1) P_i.
        # So we should remove units with the largest (2k_i - 1) P_i.
        
        # If sum_k_base < K, we need to add (K - sum_k_base) units.
        # We should add units with the smallest marginal cost.
        # The marginal cost of adding the (k_i+1)-th unit is (2k_i + 1) P_i.
        
        excess = sum_k_base - K
        
        # Calculate marginal costs for removal (if excess > 0) or addition (if excess < 0)
        # Marginal cost of removing the k_i-th unit from product i: (2*k_i - 1) * P_i
        # Marginal cost of adding the (k_i+1)-th unit to product i: (2*k_i + 1) * P_i
        
        # We can compute the total cost of the base allocation first
        total_cost = 0
        for i in range(N):
            k = k_base[i]
            if k > 0:
                total_cost += k * k * P[i]
        
        if excess == 0:
            return total_cost <= M
        
        if excess > 0:
            # We need to remove 'excess' units.
            # Calculate marginal savings for removing each unit.
            # For product i with k_base[i] units, the units are 1, 2, ..., k_base[i].
            # Removing unit j (1-indexed) saves (2j - 1) * P_i.
            # We want to remove the 'excess' units with the largest savings.
            # This is equivalent to removing the units with the largest (2j - 1) * P_i.
            # Since (2j - 1) is increasing with j, for a fixed product, the last unit has the highest saving.
            # So we can just consider the marginal saving of the last unit of each product, remove it, update, and repeat?
            # No, that's a priority queue approach. O(N + excess log N) which is too slow if excess is large.
            # Instead, we can binary search on the threshold marginal saving S.
            # We want to find the largest S such that the number of units with marginal saving >= S is at least excess.
            # Marginal saving of removing the j-th unit of product i is (2j - 1) P_i.
            # Condition: (2j - 1) P_i >= S  =>  2j - 1 >= S / P_i  =>  j >= (S / P_i + 1) / 2.
            # So for product i, the number of units we can remove with saving >= S is:
            # count_i = max(0, k_base[i] - floor((S - 1) / (2 * P_i))) ?
            # Let's derive carefully.
            # We want to count j in [1, k_base[i]] such that (2j - 1) P_i >= S.
            # 2j - 1 >= ceil(S / P_i). Let T = ceil(S / P_i).
            # 2j >= T + 1 => j >= ceil((T + 1) / 2).
            # Let j_min = ceil((ceil(S/P_i) + 1) / 2).
            # Number of such units = max(0, k_base[i] - j_min + 1).
            
            # This seems complex. Let's use a simpler approach.
            # Since N is 2e5, we can collect all marginal savings? No, too many.
            # But we only need to remove 'excess' units. If excess is small, we can use a heap.
            # If excess is large, we use binary search on S.
            # What is the max excess? It can be up to N (since each floor can overshoot by less than 1, sum of floors can be less than sum of reals by at most N).
            # Actually, sum(floor(x_i)) >= sum(x_i) - N.
            # So excess = sum_k_base - K <= N.
            # Since N <= 2e5, we can just collect the marginal savings for the last unit of each product, sort them, and remove the top 'excess'.
            # Wait, if we remove a unit, the next unit's marginal saving changes.
            # However, since excess <= N, and we only remove at most N units, and each product contributes at most 1 unit to the "top" list initially?
            # No. If we remove the last unit of product i, the new last unit has a lower saving.
            # But since excess <= N, we can just use a max-heap of size N to remove 'excess' units one by one.
            # Heap operations: O(excess log N). Since excess <= N, this is O(N log N).
            # This is acceptable.
            
            import heapq
            
            # Max-heap for marginal savings. Python has min-heap, so store negative values.
            # Each element: (-savings, product_index, current_k)
            # current_k is the number of units currently in the product.
            # The marginal saving of removing the current_k-th unit is (2*current_k - 1) * P_i.
            
            heap = []
            for i in range(N):
                k = k_base[i]
                if k > 0:
                    saving = (2 * k - 1) * P[i]
                    heapq.heappush(heap, (-saving, i, k))
            
            removed_count = 0
            while removed_count < excess and heap:
                neg_saving, i, k = heapq.heappop(heap)
                saving = -neg_saving
                
                # Remove this unit
                total_cost -= saving
                k -= 1
                removed_count += 1
                
                # If there are still units left in this product, push the next marginal saving
                if k > 0:
                    new_saving = (2 * k - 1) * P[i]
                    heapq.heappush(heap, (-new_saving, i, k))
                    
            return total_cost <= M
        
        else:
            # excess < 0, so we need to add -excess units.
            # Let add_count = -excess.
            add_count = -excess
            
            # Calculate marginal costs for adding the next unit to each product.
            # Marginal cost of adding the (k_i+1)-th unit is (2*k_i + 1) * P_i.
            # We want to add units with the smallest marginal cost.
            # Min-heap for marginal costs.
            
            heap = []
            for i in range(N):
                k = k_base[i]
                cost = (2 * k + 1) * P[i]
                heapq.heappush(heap, (cost, i, k))
            
            added_count = 0
            while added_count < add_count and heap:
                cost, i, k = heapq.heappop(heap)
                
                # Add this unit
                total_cost += cost
                k += 1
                added_count += 1
                
                # Push the next marginal cost for this product
                next_cost = (2 * k + 1) * P[i]
                heapq.heappush(heap, (next_cost, i, k))
                
            return total_cost <= M

    # Binary search for the maximum K
    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    print(ans)

solve()