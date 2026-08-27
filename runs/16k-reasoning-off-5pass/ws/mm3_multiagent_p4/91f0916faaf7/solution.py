import sys
from collections import defaultdict

MOD = 998244353

def solve():
    input = sys.stdin.read().split()
    N = int(input[0])
    A = list(map(int, input[1:N]))
    
    if N == 1:
        print(1)
        return
    
    # Collect exponents for each prime across all A_i
    prime_to_exponents = defaultdict(list)
    for a in A:
        n = a
        d = 2
        while d * d <= n:
            if n % d == 0:
                cnt = 0
                while n % d == 0:
                    n //= d
                    cnt += 1
                prime_to_exponents[d].append(cnt)
            d += 1
        if n > 1:
            prime_to_exponents[n].append(1)
    
    total = 1
    
    for p, e_list in prime_to_exponents.items():
        K = len(e_list)
        total_sum = sum(e_list)
        # Maximum possible d value: sum of all e_i (if all steps are up)
        max_d = total_sum
        # Maximum exponent in p^{d} during DP: we may compute p^{d} for d up to total_sum
        # Also need p^{-N*m} where m can be as low as -total_sum, so -N*m <= N*total_sum
        max_exp = N * total_sum + 100
        
        # Precompute powers of p up to max_exp
        pow_p = [1] * (max_exp + 1)
        for i in range(1, max_exp + 1):
            pow_p[i] = (pow_p[i-1] * p) % MOD
        
        # DP state: (h, m) where h = d - m >= 0, m <= 0
        # Value: sum of p^{D} for paths reaching this state
        # D is the sum of all d_j so far (d_0, d_1, ..., d_i)
        dp = defaultdict(int)
        dp[(0, 0)] = 1  # initial: d=0, m=0, D=0
        
        for e in e_list:
            new_dp = defaultdict(int)
            for (h, m), w in dp.items():
                d = m + h
                # Up step: add e
                h_up = h + e
                d_up = d + e
                new_dp[(h_up, m)] = (new_dp[(h_up, m)] + w * pow_p[d_up]) % MOD
                
                # Down step: subtract e
                if h >= e:
                    h_down = h - e
                    d_down = d - e
                    new_dp[(h_down, m)] = (new_dp[(h_down, m)] + w * pow_p[d_down]) % MOD
                else:
                    # h < e, new minimum is d - e
                    h_down = 0
                    m_down = d - e
                    d_down = d - e
                    new_dp[(h_down, m_down)] = (new_dp[(h_down, m_down)] + w * pow_p[d_down]) % MOD
            
            dp = new_dp
        
        # Sum over final states: weight * p^{-N*m}
        G_p = 0
        for (h, m), w in dp.items():
            exp_val = (-m) * N
            G_p = (G_p + w * pow_p[exp_val]) % MOD
        
        total = (total * G_p) % MOD
    
    print(total)

if __name__ == "__main__":
    solve()