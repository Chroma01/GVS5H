import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    A = list(map(int, data[idx:idx+N])); idx += N
    B = list(map(int, data[idx:idx+N])); idx += N
    C = list(map(int, data[idx:idx+N])); idx += N
    
    S0 = 0
    P = []  # A=0, B=1 -> need to add c (0->1)
    M = []  # A=1, B=0 -> need to subtract c (1->0)
    
    for i in range(N):
        if A[i] == 1:
            S0 += C[i]
        if A[i] == 0 and B[i] == 1:
            P.append(C[i])
        elif A[i] == 1 and B[i] == 0:
            M.append(C[i])
    
    # Sort M descending (subtract largest first to reduce S quickly)
    M.sort(reverse=True)
    # Sort P ascending (add smallest first to keep S small)
    P.sort()
    
    m = len(M)
    p = len(P)
    K = m + p
    
    # Compute prefix sums
    prefix_M = [0] * (m + 1)
    for i in range(1, m + 1):
        prefix_M[i] = prefix_M[i-1] + M[i-1]
    
    prefix_P = [0] * (p + 1)
    for i in range(1, p + 1):
        prefix_P[i] = prefix_P[i-1] + P[i-1]
    
    # Sum of M prefix sums for k=1..m: sum_{k=1}^m prefix_M[k]
    sum_M_prefix = sum(prefix_M[1:m+1])
    # Sum of P prefix sums for j=1..p: sum_{j=1}^p prefix_P[j]
    sum_P_prefix = sum(prefix_P[1:p+1])
    
    total_M = prefix_M[m]
    
    # total = (m+p)*S0 - p*total_M - sum_M_prefix + sum_P_prefix
    total = K * S0 - p * total_M - sum_M_prefix + sum_P_prefix
    
    print(total)

if __name__ == "__main__":
    solve()