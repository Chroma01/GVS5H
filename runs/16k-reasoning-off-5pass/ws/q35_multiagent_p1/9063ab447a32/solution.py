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

    # Helper function to calculate total units bought with threshold X
    # k_i(X) = floor((X + P_i) / (2 * P_i))
    def count_units(X):
        total = 0
        for p in P:
            # k_i = (X + p) // (2 * p)
            total += (X + p) // (2 * p)
        return total

    # Helper function to calculate total cost for a given threshold X
    # Sum of k_i(X)^2 * P_i
    def calculate_cost(X):
        total_cost = 0
        for p in P:
            k = (X + p) // (2 * p)
            total_cost += k * k * p
        return total_cost

    # Binary search for the maximum total units T
    # Range for T: [0, M]
    # Since min cost for 1 unit is min(P_i) >= 1, max units <= M.
    # Actually, if P_i=1, cost of k units is k^2. If we have N products,
    # we can buy more. But each unit costs at least 1, so T <= M is a safe upper bound.
    
    low = 0
    high = M
    ans = 0

    while low <= high:
        mid = (low + high) // 2
        if mid == 0:
            # 0 units cost 0, which is <= M
            ans = max(ans, mid)
            low = mid + 1
            continue
            
        # Check if it's possible to buy 'mid' units with cost <= M
        # We need to find the minimum cost to buy exactly 'mid' units.
        # This is done by finding the threshold marginal cost X such that
        # sum(k_i(X)) >= mid and sum(k_i(X-1)) < mid.
        
        # Binary search for X
        # Lower bound for X: 1 (since P_i >= 1, min marginal cost is 1)
        # Upper bound for X: 2 * M + 1 is safe. 
        # Why? If we buy M units, the max marginal cost is bounded.
        # In worst case, 1 product, P=1, T=M. k^2 <= M => k <= sqrt(M).
        # Marginal cost ~ 2k ~ 2*sqrt(M).
        # If N products, T=M, P_i=1. k_i ~ M/N. Marginal cost ~ 2*M/N.
        # Max X is when N=1, P=1, T=M => X ~ 2*sqrt(M).
        # However, if P_i is large, say P_i=2*10^9, and we buy 1 unit, X=P_i.
        # If we buy many units, X grows.
        # A safe upper bound for X is 2 * M + 2 * max(P) is overkill but safe.
        # Since T <= M, and each unit costs at least 1, the marginal cost of the last unit
        # cannot exceed 2*M + 1 roughly? 
        # Let's use 2 * 10^18 + 2 * 10^9 as a safe upper bound for X.
        # Actually, since T <= M, and cost is convex, the max marginal cost for the T-th unit
        # is bounded by 2 * T * max(P) ? No.
        # Let's just use a sufficiently large number. 2 * 10^18 is enough because
        # even if we buy 1 unit of a product with P=2*10^9, X=2*10^9.
        # If we buy M units of a product with P=1, X ~ 2*sqrt(M) ~ 2*10^9.
        # So 2*10^18 is extremely safe.
        
        X_low = 1
        X_high = 2 * 10**18 + 2 * 10**9 + 7
        X_opt = X_high
        
        while X_low <= X_high:
            X_mid = (X_low + X_high) // 2
            if count_units(X_mid) >= mid:
                X_opt = X_mid
                X_high = X_mid - 1
            else:
                X_low = X_mid + 1
        
        # Now X_opt is the smallest X such that sum(k_i(X)) >= mid
        # Calculate cost for X_opt - 1
        # Units with marginal cost < X_opt are fully taken.
        # Units with marginal cost == X_opt are partially taken.
        
        # Number of units with marginal cost <= X_opt - 1
        units_prev = count_units(X_opt - 1)
        rem = mid - units_prev
        
        # Cost for units_prev units:
        # Sum of k_i(X_opt - 1)^2 * P_i
        cost_prev = calculate_cost(X_opt - 1)
        
        # Each of the 'rem' additional units has marginal cost X_opt
        total_cost = cost_prev + rem * X_opt
        
        if total_cost <= M:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    print(ans)

if __name__ == '__main__':
    solve()