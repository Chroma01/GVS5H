import sys

# Set recursion depth just in case
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    s = input_data[1]

    MOD = 998244353

    # Count K = number of 1s in s
    K = s.count('1')
    len_S0 = N - K

    # Precompute factorials and inverse factorials for multinomial coefficients
    # We need factorials up to K
    fact = [1] * (K + 1)
    inv_fact = [1] * (K + 1)

    for i in range(1, K + 1):
        fact[i] = (fact[i-1] * i) % MOD

    # Fermat's Little Theorem for modular inverse since MOD is prime
    inv_fact[K] = pow(fact[K], MOD - 2, MOD)
    for i in range(K - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD

    # Constraints for S_B (sum of B_i for i in S1)
    # From A part: 0 <= N - S_B <= 2 * len_S0
    # => N - 2 * len_S0 <= S_B <= N
    min_SB = N - 2 * len_S0
    max_SB = N
    
    # Also S_B must be achievable by B_i in {0,1,2}
    # Min possible sum for B is 0, max is 2*K
    min_SB = max(0, min_SB)
    max_SB = min(2 * K, max_SB)

    if min_SB > max_SB:
        print(0)
        return

    # Precompute powers of 2.
    pow2 = [1] * (K + 1)
    for i in range(1, K + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD
        
    ans = 0
    
    # We iterate over m = n0 + n1, the number of positions in S1 that are not n2 or n3.
    # n2 + n3 = K - m.
    # Let j = n3. Then n2 = K - m - j.
    # Constraints:
    # 1. n2 + 2*n3 <= max_SB  => (K - m - j) + 2*j <= max_SB => K - m + j <= max_SB => j <= max_SB - K + m
    # 2. n1 + 2*n2 + 2*n3 >= min_SB
    #    n1 = m - n0 - n1? No, n1 is part of m.
    #    Let's re-derive.
    #    m = n0 + n1.
    #    n2 + n3 = K - m.
    #    Let j = n3. Then n2 = K - m - j.
    #    Constraint 1: n2 + 2*n3 <= max_SB
    #       (K - m - j) + 2*j <= max_SB
    #       K - m + j <= max_SB
    #       j <= max_SB - K + m
    #    Let R_m = max_SB - K + m.
    #    If R_m < 0, no valid j.
    #    Also j >= 0 and j <= K - m.
    #    So j in [0, min(K-m, R_m)].
    
    #    Constraint 2: n1 + 2*n2 + 2*n3 >= min_SB
    #       n1 + 2*(K - m - j) + 2*j >= min_SB
    #       n1 + 2*K - 2*m >= min_SB
    #       n1 >= min_SB - 2*K + 2*m
    #    Let min_n1 = min_SB - 2*K + 2*m.
    #    If min_n1 < 0, min_n1 = 0.
    #    Also n1 <= m (since n1 <= n0+n1 = m).
    #    So n1 in [max(0, min_n1), m].
    
    #    The number of ways to choose which positions are n2/n3 vs n0/n1 is C(K, m).
    #    The number of ways to choose which of the m positions are n1 vs n0 is C(m, n1).
    #    The number of ways to choose which of the K-m positions are n3 vs n2 is C(K-m, j).
    #    So the term for fixed m, j, n1 is:
    #       C(K, m) * C(m, n1) * C(K-m, j)
    #    = K! / (m! (K-m)!) * m! / (n1! (m-n1)!) * (K-m)! / (j! (K-m-j)!)
    #    = K! / (n1! (m-n1)! j! (K-m-j)!)
    #    = K! / (n1! n0! n3! n2!) which is the multinomial coefficient.
    
    #    We sum over m, j, n1.
    #    Sum_{m=0}^K C(K, m) * [ Sum_{j=0}^{min(K-m, R_m)} C(K-m, j) * Sum_{n1=max(0, min_n1)}^m C(m, n1) ]
    
    #    Let S1(m, j_max) = Sum_{j=0}^{j_max} C(K-m, j).
    #    Let P(m, n1_min) = Sum_{n1=n1_min}^m C(m, n1).
    
    #    We can compute these sums using the symmetry trick to minimize the number of terms.
    
    for m in range(K + 1):
        # Calculate R_m
        R_m = max_SB - K + m
        max_j = K - m
        if R_m < max_j:
            max_j = R_m
            
        if max_j < 0:
            continue
            
        # Calculate min_n1
        min_n1 = min_SB - 2 * K + 2 * m
        if min_n1 < 0:
            min_n1 = 0
            
        if min_n1 > m:
            continue
            
        # Compute S1_part = Sum_{j=0}^{max_j} C(K-m, j)
        # Use symmetry if max_j > (K-m)/2
        rem = K - m
        if max_j > rem // 2:
            # Sum_{j=0}^{max_j} C(rem, j) = 2^rem - Sum_{j=max_j+1}^rem C(rem, j)
            # Sum_{j=max_j+1}^rem C(rem, j) = Sum_{i=0}^{rem-max_j-1} C(rem, i)
            L_sym = rem - max_j - 1
            sum_sym = 0
            for i in range(L_sym + 1):
                term = (fact[rem] * inv_fact[i]) % MOD * inv_fact[rem-i] % MOD
                sum_sym = (sum_sym + term) % MOD
            S1_part = (pow2[rem] - sum_sym) % MOD
        else:
            S1_part = 0
            for j in range(max_j + 1):
                term = (fact[rem] * inv_fact[j]) % MOD * inv_fact[rem-j] % MOD
                S1_part = (S1_part + term) % MOD
                
        # Compute P_part = Sum_{n1=min_n1}^m C(m, n1)
        if min_n1 == 0:
            P_part = pow2[m]
        else:
            if m - min_n1 < min_n1:
                # Sum_{n1=min_n1}^m C(m, n1) = 2^m - Sum_{n1=0}^{min_n1-1} C(m, n1)
                L_sym = min_n1 - 1
                sum_sym = 0
                for i in range(L_sym + 1):
                    term = (fact[m] * inv_fact[i]) % MOD * inv_fact[m-i] % MOD
                    sum_sym = (sum_sym + term) % MOD
                P_part = (pow2[m] - sum_sym) % MOD
            else:
                P_part = 0
                for n1 in range(min_n1, m + 1):
                    term = (fact[m] * inv_fact[n1]) % MOD * inv_fact[m-n1] % MOD
                    P_part = (P_part + term) % MOD
                    
        # Term for this m
        term = (fact[K] * inv_fact[m]) % MOD * inv_fact[K-m] % MOD
        term = term * S1_part % MOD * P_part % MOD
        ans = (ans + term) % MOD
        
    print(ans)

solve()