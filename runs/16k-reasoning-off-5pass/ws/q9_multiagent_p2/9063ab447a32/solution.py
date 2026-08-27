import sys

# Set recursion depth just in case, though this solution is iterative.
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

    # The problem asks to maximize the total number of units bought with budget M.
    # Cost for k units of product i is k^2 * P_i.
    # The marginal cost of the k-th unit of product i is (k^2 - (k-1)^2) * P_i = (2k - 1) * P_i.
    # Since the marginal cost increases with k, the optimal strategy is to greedily buy
    # units with the lowest marginal costs.
    #
    # We can binary search for the maximum marginal cost threshold V such that we can
    # afford all units with marginal cost <= V.
    # For a given V, the number of units x_i of product i we can buy is the largest integer
    # such that (2*x_i - 1) * P_i <= V.
    # Solving for x_i: 2*x_i <= V/P_i + 1  =>  x_i = floor((V + P_i) / (2 * P_i)).
    #
    # The total cost for these x_i units is sum(x_i^2 * P_i).
    # We binary search for the largest V where total_cost <= M.
    # The answer is the sum of x_i for this optimal V.

    # Range for V:
    # Lower bound: 0
    # Upper bound: Since M <= 10^18 and min P_i >= 1, the max marginal cost 
    # we might consider is bounded. If we buy k units of product with P=1, 
    # cost is k^2. k^2 <= 10^18 => k <= 10^9. Marginal cost of last unit is ~2*10^9.
    # However, if P_i is large, V is small. The absolute upper bound for V 
    # where we might buy at least 1 unit is roughly M (since 1st unit costs P_i).
    # If P_i > M, we buy 0 units. If P_i <= M, we buy at least 1.
    # The marginal cost of the last unit bought cannot exceed M (since that unit alone costs <= M).
    # So V_max = M is a safe upper bound. Let's use 2*10^18 to be safe and cover edge cases.
    
    low = 0
    high = 2 * 10**18 
    ans_V = 0
    
    # Pre-calculate 2*P_i to avoid repeated multiplication if needed, 
    # but direct calculation is fast enough.
    
    def check(V):
        total_cost = 0
        for p in P:
            if V < p:
                # x_i = 0
                continue
            
            # x_i = floor((V + p) / (2*p))
            x = (V + p) // (2 * p)
            
            # Cost contribution: x^2 * p
            # Python handles large integers automatically.
            term = x * x * p
            total_cost += term
            # Optimization: break early if cost exceeds M
            if total_cost > M:
                return False
        return total_cost <= M

    # Binary Search
    # We want max V such that check(V) is True.
    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans_V = mid
            low = mid + 1
        else:
            high = mid - 1
            
    # Calculate the total units for ans_V
    total_units = 0
    for p in P:
        if ans_V >= p:
            x = (ans_V + p) // (2 * p)
            total_units += x
            
    print(total_units)

if __name__ == '__main__':
    solve()