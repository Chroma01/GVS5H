import sys

def feasible(H, U, D, X):
    n = len(U)
    # L_i = max(0, H - D_i)
    # R_i = min(U_i, H)
    # Initialize v_i = R_i
    v = [min(U[i], H) for i in range(n)]
    L = [max(0, H - D[i]) for i in range(n)]
    
    # Forward pass: enforce u_{i+1} <= u_i + X
    for i in range(n - 1):
        new_val = v[i] + X
        if v[i+1] > new_val:
            v[i+1] = new_val
        if v[i+1] < L[i+1]:
            return False
    
    # Backward pass: enforce u_i <= u_{i+1} + X
    for i in range(n - 2, -1, -1):
        new_val = v[i+1] + X
        if v[i] > new_val:
            v[i] = new_val
        if v[i] < L[i]:
            return False
    
    return True

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    X = int(input_data[idx]); idx += 1
    U = []
    D = []
    S = []
    sum_S = 0
    min_S = float('inf')
    for _ in range(N):
        u = int(input_data[idx]); idx += 1
        d = int(input_data[idx]); idx += 1
        U.append(u)
        D.append(d)
        s = u + d
        S.append(s)
        sum_S += s
        if s < min_S:
            min_S = s
    
    # Binary search for maximum H in [0, min_S]
    lo = 0
    hi = min_S
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid, U, D, X):
            lo = mid
        else:
            hi = mid - 1
    
    answer = sum_S - N * lo
    print(answer)

if __name__ == "__main__":
    solve()