import sys

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        X = int(next(iterator))
    except StopIteration:
        return

    U = [0] * N
    D = [0] * N
    min_sum = float('inf')

    for i in range(N):
        u_val = int(next(iterator))
        d_val = int(next(iterator))
        U[i] = u_val
        D[i] = d_val
        s = u_val + d_val
        if s < min_sum:
            min_sum = s

    # Binary search for the maximum H
    # H must be at least 2 because U_i >= 1, D_i >= 1 => U_i + D_i >= 2
    # And H <= min_sum
    
    low = 2
    high = min_sum
    ans_H = 2

    while low <= high:
        mid = (low + high) // 2
        
        # Check feasibility for H = mid
        # cur_min, cur_max represent the feasible range for U'_i
        # Initially for i=0
        # L_0 = max(1, mid - D[0])
        # R_0 = min(U[0], mid - 1)
        
        cur_min = mid - D[0]
        if cur_min < 1:
            cur_min = 1
        cur_max = U[0]
        if cur_max > mid - 1:
            cur_max = mid - 1
            
        feasible = True
        if cur_min > cur_max:
            feasible = False
        else:
            for i in range(1, N):
                # Update range based on |U'_i - U'_{i-1}| <= X
                # Expand previous range
                new_min = cur_min - X
                new_max = cur_max + X
                
                # Intersect with [L_i, R_i]
                L_i = mid - D[i]
                if L_i < 1:
                    L_i = 1
                R_i = U[i]
                if R_i > mid - 1:
                    R_i = mid - 1
                
                if L_i > new_min:
                    new_min = L_i
                if R_i < new_max:
                    new_max = R_i
                    
                if new_min > new_max:
                    feasible = False
                    break
                    
                cur_min = new_min
                cur_max = new_max
        
        if feasible:
            ans_H = mid
            low = mid + 1
        else:
            high = mid - 1

    total_sum = sum(U) + sum(D)
    cost = total_sum - N * ans_H
    print(cost)

if __name__ == '__main__':
    solve()