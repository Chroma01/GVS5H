import sys

def solve():
    # Read all input at once
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

    # Precompute P for faster access
    # P is a list of integers

    # Function to compute S(T) = total number of units with marginal cost <= T
    def get_S(T):
        if T < 0:
            return 0
        total_units = 0
        for p in P:
            # Marginal cost of j-th unit is (2j-1)*p
            # We want (2j-1)*p <= T  =>  2j-1 <= T/p  =>  j <= (T/p + 1)/2
            # q = floor(T / p)
            # cnt = floor((q + 1) / 2)
            q = T // p
            cnt = (q + 1) // 2
            if cnt > 0:
                total_units += cnt
        return total_units

    # Function to compute minimum cost to buy exactly X units
    def get_min_cost(X):
        if X == 0:
            return 0
        
        # Binary search for the threshold T such that S(T) >= X and S(T-1) < X
        # Range for T: [0, 2*M]
        low = 0
        high = 2 * M
        
        while low < high:
            mid = (low + high) // 2
            if get_S(mid) >= X:
                high = mid
            else:
                low = mid + 1
        
        T_star = low
        
        # Calculate cost of all units with marginal cost < T_star
        # These are units with marginal cost <= T_star - 1
        # Number of such units is K = S(T_star - 1)
        K = get_S(T_star - 1)
        
        cost = 0
        # Sum of costs for units with marginal cost < T_star
        # For each product i, if we take cnt_i units, cost is cnt_i^2 * P_i
        # cnt_i is the number of units with marginal cost <= T_star - 1
        for p in P:
            q = (T_star - 1) // p
            cnt = (q + 1) // 2
            if cnt > 0:
                cost += cnt * cnt * p
        
        # Add remaining units at marginal cost T_star
        remaining = X - K
        cost += remaining * T_star
        
        return cost

    # Binary search on the answer X (total units)
    # Range [0, M] since min cost per unit is 1
    low = 0
    high = M
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        cost = get_min_cost(mid)
        if cost <= M:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
            
    print(ans)

if __name__ == '__main__':
    solve()