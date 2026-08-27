import sys

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    X = int(input_data[idx]); idx += 1
    U = []
    D = []
    for _ in range(N):
        U.append(int(input_data[idx])); idx += 1
        D.append(int(input_data[idx])); idx += 1
    
    # M is the absolute upper bound for H: H <= min_i(U_i + D_i)
    M = min(u + d for u, d in zip(U, D))
    
    # Total sum of U_i + D_i
    total_sum = sum(U) + sum(D)
    
    # Function to check if a given H is feasible
    def feasible(H):
        # Forward propagation: maintain [lo, hi] for current a_i
        lo = max(0, H - D[0])
        hi = min(U[0], H)
        if lo > hi:
            return False
        for i in range(1, N):
            # a_i must be in [L_i, R_i] and within X of a_{i-1}
            L = max(0, H - D[i])
            R = min(U[i], H)
            # The previous a_{i-1} is in [lo, hi]. So a_i must be in [lo - X, hi + X]
            new_lo = max(L, lo - X)
            new_hi = min(R, hi + X)
            if new_lo > new_hi:
                return False
            lo, hi = new_lo, new_hi
        return True
    
    # Binary search for the maximum feasible H in [0, M]
    # Feasibility is monotonic in H (proved by noting lo, hi are non-decreasing in H)
    lo_H, hi_H = 0, M
    while lo_H < hi_H:
        mid = (lo_H + hi_H + 1) // 2
        if feasible(mid):
            lo_H = mid
        else:
            hi_H = mid - 1
    
    H_max = lo_H
    answer = total_sum - N * H_max
    print(answer)

if __name__ == "__main__":
    solve()