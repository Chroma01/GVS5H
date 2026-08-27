import sys

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    MOD = 998244353
    
    if N == 0:
        print(0)
        return

    # Precompute factorials and inverse factorials if needed, 
    # but we only need (N-1)!
    
    # Step 1: Group numbers by their digit length
    # Lengths can be 1 to 6 for N <= 200,000
    # We need sum of numbers for each length
    sum_by_len = {}
    
    # P(1) = product over all x in 1..N of (1 + 10^{len(x)})
    P1 = 1
    
    for x in range(1, N + 1):
        s = str(x)
        d = len(s)
        if d not in sum_by_len:
            sum_by_len[d] = 0
        sum_by_len[d] = (sum_by_len[d] + x) % MOD
        
        # Update P(1)
        term = (1 + pow(10, d, MOD)) % MOD
        P1 = (P1 * term) % MOD
        
    # Step 2: Compute (N-1)!
    if N == 1:
        fact_n_minus_1 = 1
    else:
        fact_n_minus_1 = 1
        for i in range(1, N):
            fact_n_minus_1 = (fact_n_minus_1 * i) % MOD
            
    # Step 3: Compute the answer
    # Answer = sum_{d} (Sum_d * (N-1)! * P(1) * inv(1 + 10^d))
    
    ans = 0
    
    for d, sum_d in sum_by_len.items():
        if sum_d == 0:
            continue
            
        # Compute inverse of (1 + 10^d)
        denom = (1 + pow(10, d, MOD)) % MOD
        inv_denom = pow(denom, MOD - 2, MOD)
        
        term = (sum_d * fact_n_minus_1) % MOD
        term = (term * P1) % MOD
        term = (term * inv_denom) % MOD
        
        ans = (ans + term) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()