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

    # Binary search for the maximum total units K
    # Lower bound: 0
    # Upper bound: We need a safe upper bound.
    # Max units from one product with P=1 and M=10^18 is 10^9.
    # If we spread across N products, the cost is minimized when units are distributed.
    # Min cost for K units is roughly K^2 / sum(sqrt(P_i))? No.
    # A safe upper bound: if all P_i = 1, min cost for K units is when k_i = K/N.
    # Cost = N * (K/N)^2 = K^2 / N.
    # K^2 / N <= M => K <= sqrt(M * N).
    # M = 10^18, N = 2*10^5 => M*N = 2*10^23 => sqrt(M*N) ~ 4.5 * 10^11.
    # So upper bound 2 * 10^12 is safe.
    
    low = 0
    high = 2 * 10**12 + 1000000000000 # Add some buffer
    
    def get_k_for_lambda(lam, P):
        """
        For a given marginal cost threshold lam,
        returns the number of units k_i for each product i
        such that the marginal cost of the k_i-th unit is <= lam.
        Marginal cost of j-th unit of product i is P_i * (2*j - 1).
        Condition: P_i * (2*k_i - 1) <= lam
        2*k_i - 1 <= lam / P_i
        2*k_i <= lam / P_i + 1
        k_i <= (lam / P_i + 1) / 2
        """
        k_list = []
        total_units = 0
        for p in P:
            # Integer arithmetic: k_i = floor((lam // p + 1) / 2)
            # But careful: lam/p might not be integer.
            # k_i = (lam // p + 1) // 2
            # Let's verify:
            # If lam = 4, p = 1: k_i <= (4/1 + 1)/2 = 2.5 -> 2.
            # (4//1 + 1)//2 = 5//2 = 2. Correct.
            # If lam = 3, p = 1: k_i <= (3/1 + 1)/2 = 2. -> 2.
            # (3//1 + 1)//2 = 4//2 = 2. Correct.
            # If lam = 1, p = 1: k_i <= (1/1 + 1)/2 = 1. -> 1.
            # (1//1 + 1)//2 = 2//2 = 1. Correct.
            # If lam = 0, p = 1: k_i <= 0.5 -> 0.
            # (0//1 + 1)//2 = 1//2 = 0. Correct.
            
            k = (lam // p + 1) // 2
            if k < 0:
                k = 0
            k_list.append(k)
            total_units += k
        return total_units, k_list

    def get_cost_for_k_list(k_list, P):
        """
        Calculates the total cost for a given list of k_i values.
        Cost for product i is k_i^2 * P_i.
        """
        total_cost = 0
        for k, p in zip(k_list, P):
            total_cost += k * k * p
        return total_cost

    def get_marginal_costs_last_unit(k_list, P):
        """
        Returns the marginal cost of the last unit for each product.
        Marginal cost of j-th unit is P_i * (2*j - 1).
        """
        m_list = []
        for k, p in zip(k_list, P):
            if k > 0:
                m_list.append(p * (2 * k - 1))
            else:
                m_list.append(0)
        return m_list

    def check(K):
        """
        Checks if it is possible to buy K units with cost <= M.
        Returns True if min cost for K units <= M, else False.
        """
        if K == 0:
            return True
        
        # Binary search for lambda such that total units >= K
        # Lambda range: [0, 2 * 10^18] roughly.
        # Max marginal cost can be around 2 * 10^9 * 2 * 10^9 = 4 * 10^18?
        # If k_i = 10^9, P_i = 10^9, marginal cost = 10^9 * (2*10^9 - 1) ~ 2*10^18.
        # So upper bound 4*10^18 is safe.
        
        lam_low = 0
        lam_high = 4 * 10**18 + 1000000000000000000
        
        best_lam = lam_high
        best_total_units = 0
        best_k_list = []
        
        while lam_low <= lam_high:
            mid = (lam_low + lam_high) // 2
            total_units, k_list = get_k_for_lambda(mid, P)
            if total_units >= K:
                best_lam = mid
                best_total_units = total_units
                best_k_list = k_list
                lam_high = mid - 1
            else:
                lam_low = mid + 1
        
        # Now best_k_list gives the units for the smallest lambda such that sum(k_i) >= K
        # Total units bought is best_total_units
        # We need to remove R = best_total_units - K units
        # These should be the ones with the highest marginal costs.
        
        R = best_total_units - K
        
        if R == 0:
            cost = get_cost_for_k_list(best_k_list, P)
            return cost <= M
        
        # We need to subtract the sum of the R largest marginal costs among the selected units.
        # The selected units for product i have marginal costs: P_i, 3P_i, ..., P_i(2k_i-1).
        # We can binary search for a threshold mu such that the number of selected units with marginal cost > mu is <= R,
        # and with marginal cost >= mu is >= R.
        
        # Let cnt(mu) be the number of selected units with marginal cost > mu.
        # For product i, k_i units are selected.
        # The marginal costs are m_j = P_i * (2j - 1) for j=1..k_i.
        # We want to count how many j satisfy P_i * (2j - 1) > mu.
        # 2j - 1 > mu / P_i
        # 2j > mu / P_i + 1
        # j > (mu / P_i + 1) / 2
        # So j >= floor((mu / P_i + 1) / 2) + 1
        # Let k_i_prime = floor((mu / P_i + 1) / 2). This is the number of units with marginal cost <= mu.
        # Then the number of units with marginal cost > mu is max(0, k_i - k_i_prime).
        
        # Binary search for mu in [0, best_lam]
        mu_low = 0
        mu_high = best_lam
        
        best_mu = 0
        count_gt = 0
        
        while mu_low <= mu_high:
            mid = (mu_low + mu_high) // 2
            
            # Calculate count of units with marginal cost > mid
            cnt = 0
            for k, p in zip(best_k_list, P):
                if k > 0:
                    # k_i_prime = number of units with marginal cost <= mid
                    # k_i_prime = (mid // p + 1) // 2
                    k_prime = (mid // p + 1) // 2
                    if k_prime > k:
                        k_prime = k
                    cnt += (k - k_prime)
            
            if cnt <= R:
                best_mu = mid
                count_gt = cnt
                mu_high = mid - 1
            else:
                mu_low = mid + 1
        
        # Now, best_mu is the largest value such that the number of units with marginal cost > best_mu is <= R.
        # Let R_high = count_gt. These are the units we definitely remove.
        # The remaining R - R_high units to remove have marginal cost == best_mu (if any).
        
        # Calculate the cost to subtract:
        # 1. Sum of marginal costs of all units with marginal cost > best_mu.
        # 2. Plus (R - R_high) * best_mu.
        
        cost_to_subtract = 0
        
        # For each product, the units with marginal cost > best_mu are indices from k_i_prime + 1 to k_i.
        # Their marginal costs are P_i * (2j - 1) for j in [k_i_prime + 1, k_i].
        # Sum = P_i * sum_{j=k_i_prime+1}^{k_i} (2j - 1)
        # Sum of (2j - 1) from j=1 to k is k^2.
        # So sum from j=k_i_prime+1 to k_i is k_i^2 - k_i_prime^2.
        
        for k, p in zip(best_k_list, P):
            if k > 0:
                k_prime = (best_mu // p + 1) // 2
                if k_prime > k:
                    k_prime = k
                if k_prime < k:
                    cost_to_subtract += p * (k * k - k_prime * k_prime)
        
        cost_to_subtract += (R - count_gt) * best_mu
        
        total_cost = get_cost_for_k_list(best_k_list, P) - cost_to_subtract
        return total_cost <= M

    ans = 0
    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
            
    print(ans)

solve()