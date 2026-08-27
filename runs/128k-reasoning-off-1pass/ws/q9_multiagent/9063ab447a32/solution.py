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

    # Sort P to optimize the check function (though not strictly necessary for correctness)
    P.sort()

    # Binary search for the maximum marginal cost threshold X
    # The marginal cost of the k-th unit of product i is (2k-1)*P[i].
    # If we set a threshold X, we buy k units if (2k-1)*P[i] <= X.
    # Solving for k: 2k-1 <= X/P[i] => 2k <= X/P[i] + 1 => k = floor((X/P[i] + 1) / 2)
    
    # Range for X:
    # Min marginal cost is 1*min(P) >= 1.
    # Max marginal cost: 
    # If P=1, M=10^18, we buy ~10^9 units. Marginal cost ~ 2*10^9.
    # If P=2*10^9, we buy 1 unit (cost 2*10^9). Marginal cost = 2*10^9.
    # So X is in range [1, 4*10^9] is safe.
    
    low = 1
    high = 4000000000 # 4 * 10^9
    ans_units = 0
    
    while low <= high:
        mid = (low + high) // 2
        
        total_cost = 0
        possible = True
        
        # Calculate cost for threshold mid
        for p in P:
            if mid < p:
                # mid / p = 0 => k = (0+1)//2 = 0
                continue
            
            val = mid // p
            k = (val + 1) // 2
            
            if k == 0:
                continue
            
            # Cost = k^2 * p
            cost = k * k * p
            total_cost += cost
            if total_cost > M:
                possible = False
                break
        
        if possible and total_cost <= M:
            # mid is valid, try to find a higher threshold
            # Calculate actual units for this mid
            current_units = 0
            for p in P:
                if mid < p:
                    continue
                val = mid // p
                k = (val + 1) // 2
                current_units += k
            ans_units = current_units
            low = mid + 1
        else:
            high = mid - 1
            
    print(ans_units)

if __name__ == '__main__':
    solve()