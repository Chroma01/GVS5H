import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])
    A = list(map(int, input_data[2:]))
    
    MOD = 998244353
    
    # Precompute binomial coefficients C(K, p)
    C = [1] * (K + 1)
    for p in range(1, K + 1):
        C[p] = C[p-1] * (K - p + 1) // p
        
    # P[p] stores sum_{i=0}^{j-1} S_i^p
    # Initially j=1, so sum includes S_0 = 0
    # S_0^0 = 1, S_0^p = 0 for p > 0
    P = [0] * (K + 1)
    P[0] = 1
    
    current_S = 0
    ans = 0
    
    for x in A:
        current_S = (current_S + x) % MOD
        
        # Compute powers of current_S: powers[p] = current_S^p
        powers = [1] * (K + 1)
        for p in range(1, K + 1):
            powers[p] = (powers[p-1] * current_S) % MOD
            
        # Add contributions for each p
        # Contribution for fixed j and p: C[p] * (-1)^p * P[p] * S_j^{K-p}
        for p in range(K + 1):
            term = (C[p] * P[p]) % MOD
            term = (term * powers[K-p]) % MOD
            
            if p % 2 == 1:
                term = (MOD - term) % MOD
                
            ans = (ans + term) % MOD
            
        # Update P with current S_j^p for next iterations
        for p in range(K + 1):
            P[p] = (P[p] + powers[p]) % MOD
            
    print(ans)

if __name__ == '__main__':
    solve()