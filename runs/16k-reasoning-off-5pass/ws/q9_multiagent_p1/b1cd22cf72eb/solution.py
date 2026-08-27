import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        
        U = []
        D = []
        
        for _ in range(N):
            u_val = int(next(iterator))
            d_val = int(next(iterator))
            U.append(u_val)
            D.append(d_val)
            
    except StopIteration:
        return

    # Calculate the maximum possible sum for each pair
    # The upper bound for H is max(U[i] + D[i]) because we can only reduce lengths.
    # Actually, H must be <= U[i] + D[i] for ALL i.
    # So the absolute upper bound is max(U[i] + D[i]), but the check function 
    # will naturally return False for any H > min(U[i] + D[i]).
    max_possible_H = 0
    for i in range(N):
        s = U[i] + D[i]
        if s > max_possible_H:
            max_possible_H = s
            
    # Binary search for the maximum feasible H
    # Lower bound for H is 1 (since lengths are positive integers, min sum is 2, but 1 is safe lower bound)
    low = 1
    high = max_possible_H
    ans_H = 1
    
    # We need to find the largest H such that a valid sequence U' exists.
    # A sequence U' exists if for all i, L_i <= U'_i <= R_i and |U'_i - U'_{i+1}| <= X.
    # Where L_i = H - D[i] and R_i = U[i].
    # Feasibility check:
    # Maintain [min_val, max_val] representing the range of possible values for U'_i
    # considering constraints from 1 to i.
    # For i=1: [min_val, max_val] = [L_1, R_1]
    # For i+1:
    #   Reachable from previous: [min_val - X, max_val + X]
    #   Constraint at i+1: [L_{i+1}, R_{i+1}]
    #   New range: Intersection of the two.
    #   If min_new > max_new, then H is invalid.
    
    def check(H):
        # Calculate initial bounds for U'_1
        L1 = H - D[0]
        R1 = U[0]
        
        if L1 > R1:
            return False
        
        min_val = L1
        max_val = R1
        
        for i in range(1, N):
            Li = H - D[i]
            Ri = U[i]
            
            # Intersection with reachable range from previous
            # Reachable: [min_val - X, max_val + X]
            # Constraint: [Li, Ri]
            
            new_min = max(Li, min_val - X)
            new_max = min(Ri, max_val + X)
            
            if new_min > new_max:
                return False
            
            min_val = new_min
            max_val = new_max
            
        return True

    # Binary Search
    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans_H = mid
            low = mid + 1
        else:
            high = mid - 1
            
    # Calculate minimum cost
    # Cost = Sum(U[i] + D[i]) - N * H
    total_sum = sum(U) + sum(D)
    min_cost = total_sum - N * ans_H
    
    print(min_cost)

if __name__ == '__main__':
    solve()