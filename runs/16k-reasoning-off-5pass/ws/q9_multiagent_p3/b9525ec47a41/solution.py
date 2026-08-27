import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    s_str = input_data[1]
    
    # Count number of 1s in s
    K = s_str.count('1')
    
    MOD = 998244353
    
    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    finv = [1] * (N + 1)
    
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    # Precompute powers of 2
    pow2 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD
        
    total_ans = 0
    
    # We iterate i from 0 to N
    for i in range(N + 1):
        m = N - i
        
        # Coeff[i] = N! * 2^i / (i! * m! * m!)
        term = fact[N]
        term = (term * pow2[i]) % MOD
        term = (term * inv[i]) % MOD
        term = (term * inv[m]) % MOD
        term = (term * inv[m]) % MOD
        
        # Calculate H(i)
        # We sum L(S) for S in [0, K], where L(S) is the length of intersection of [0, i] and [i-S, N-S]
        # L(S) is defined piecewise based on S relative to i and N-i.
        # Let a = min(i, N-i), b = max(i, N-i).
        # Range [0, a]: L(S) = S + 1
        # Range (a, b]: L(S) = a + 1
        # Range (b, N]: L(S) = N - S + 1
        
        M = K if K < N else N
        
        if M <= 0:
            H_i = 0
        else:
            a = i if i < m else m
            b = i if i > m else m
            
            H_i = 0
            
            # Part 1: [0, min(M, a)]
            limit1 = M if M < a else a
            if limit1 >= 0:
                # Sum_{S=0}^{limit1} (S+1) = (limit1+1)(limit1+2)/2
                count1 = limit1 + 1
                sum1 = (count1 * (count1 + 1)) // 2
                H_i = (H_i + sum1) % MOD
            
            # Part 2: (a, min(M, b)]
            if M > a:
                limit2 = M if M < b else b
                if limit2 > a:
                    count2 = limit2 - a
                    val2 = a + 1
                    sum2 = (count2 * val2) % MOD
                    H_i = (H_i + sum2) % MOD
            
            # Part 3: (b, M]
            if M > b:
                count3 = M - b
                # Sum_{S=b+1}^{M} (N - S + 1)
                # Let k = N - S + 1. When S=b+1, k = N - b. When S=M, k = N - M + 1.
                # Sum k from N-M+1 to N-b.
                low_k = N - M + 1
                high_k = N - b
                sum3 = (count3 * (low_k + high_k)) // 2
                H_i = (H_i + sum3) % MOD
        
        # Add to total
        contribution = (term * H_i) % MOD
        total_ans = (total_ans + contribution) % MOD
        
    print(total_ans)

if __name__ == '__main__':
    solve()