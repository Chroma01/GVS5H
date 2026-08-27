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

    # Precompute 1/P_i is not needed, we work with P_i directly.
    # We want to find the maximum K such that min_cost(K) <= M.
    # min_cost(K) is the minimum cost to buy exactly K units.
    # To compute min_cost(K):
    # 1. Find the smallest threshold T such that sum(floor((T/P_i + 1)/2)) >= K.
    #    Let k_i = floor((T/P_i + 1)/2).
    #    Total units S = sum(k_i).
    # 2. The cost of buying k_i units for each product is sum(k_i^2 * P_i).
    # 3. If S > K, we have bought S-K extra units. These are the most expensive units among those bought.
    #    The marginal cost of the last unit of product i is m_i = (2*k_i - 1) * P_i.
    #    We need to subtract the sum of the largest (S-K) values from {m_i}.
    
    # Binary search for K in [0, M] (since min cost per unit is 1, max units <= M)
    # Actually, max units can be larger if P_i are small, but cost is at least 1 per unit, so K <= M.
    # Wait, if P_i=1, cost of 1 unit is 1. Cost of K units is K^2. So K^2 <= M => K <= sqrt(M).
    # But we can buy from multiple products. The max units is bounded by M because each unit costs at least 1.
    # So K in [0, M] is safe. M <= 10^18.
    
    low = 0
    high = M + 1 # Exclusive upper bound
    
    # Precompute P for faster access
    # P is already a list
    
    def get_min_cost(K):
        if K == 0:
            return 0
        
        # Binary search for T
        # T is the maximum marginal cost allowed.
        # Marginal cost of j-th unit of product i is (2j-1)*P_i.
        # We want (2j-1)*P_i <= T => j <= (T/P_i + 1)/2.
        # So k_i = floor((T/P_i + 1)/2).
        
        # Range for T:
        # Min T: 1 (if we buy at least 1 unit)
        # Max T: 2 * M + 1 (since max cost is M, and marginal cost can be up to 2*M roughly)
        # Actually, if we buy K units, the max marginal cost is bounded by 2*K*max(P) or similar.
        # But 2*10^18 is a safe upper bound since M <= 10^18 and P_i <= 2*10^9.
        # The max marginal cost for the last unit is (2k-1)P. If k=1, P. If k is large, it can be large.
        # But we only care about T such that sum k_i >= K.
        # A safe upper bound for T is 2 * M + 2 * max(P).
        # Let's use 2 * 10^18 + 4 * 10^9 as upper bound.
        
        t_low = 1
        t_high = 2 * 10**18 + 4 * 10**9
        best_T = t_high
        
        while t_low <= t_high:
            mid = (t_low + t_high) // 2
            total_units = 0
            for p in P:
                # k_i = floor((mid/p + 1)/2)
                # integer arithmetic: (mid // p + 1) // 2
                # But mid // p might be large, but it's fine.
                # Note: if mid < p, then mid//p = 0, k_i = 0.
                k = (mid // p + 1) // 2
                total_units += k
                if total_units >= K:
                    break
            
            if total_units >= K:
                best_T = mid
                t_high = mid - 1
            else:
                t_low = mid + 1
        
        T = best_T
        
        # Now compute the cost
        total_cost = 0
        total_units = 0
        marginal_costs_last_unit = []
        
        for p in P:
            k = (T // p + 1) // 2
            if k > 0:
                total_cost += k * k * p
                total_units += k
                # Marginal cost of the k-th unit is (2k-1)*p
                marginal_costs_last_unit.append((2 * k - 1) * p)
        
        excess = total_units - K
        if excess > 0:
            # We need to remove the 'excess' units with the largest marginal costs.
            # marginal_costs_last_unit contains the marginal costs of the last unit of each product.
            # We need to subtract the sum of the largest 'excess' values from this list.
            # Since N is up to 2*10^5, sorting is O(N log N).
            # We do this for each K in binary search, so total complexity O(N log N log M log T).
            # This might be tight. Let's optimize by using nlargest or just sort if N is small enough.
            # In Python, sort is very fast.
            marginal_costs_last_unit.sort(reverse=True)
            for i in range(excess):
                total_cost -= marginal_costs_last_unit[i]
                
        return total_cost

    # Binary search for the maximum K such that min_cost(K) <= M
    ans = 0
    while low < high:
        mid = (low + high) // 2
        if mid == 0:
            # 0 units cost 0, which is <= M
            ans = max(ans, 0)
            low = 1
            continue
            
        cost = get_min_cost(mid)
        if cost <= M:
            ans = mid
            low = mid + 1
        else:
            high = mid
            
    print(ans)

solve()