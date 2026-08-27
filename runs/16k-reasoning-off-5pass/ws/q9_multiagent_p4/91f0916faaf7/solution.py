import sys

# Increase recursion depth just in case, though we will use iterative DP
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N - 1):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    MOD = 998244353

    # Collect all prime factors from all A_i
    # We need to process each prime independently
    # Map: prime -> list of exponents in A_1, A_2, ..., A_{N-1}
    prime_exponents = {}
    
    for x in A:
        d = 2
        temp = x
        while d * d <= temp:
            if temp % d == 0:
                count = 0
                while temp % d == 0:
                    count += 1
                    temp //= d
                if d not in prime_exponents:
                    prime_exponents[d] = []
                prime_exponents[d].append(count)
            d += 1
        if temp > 1:
            if temp not in prime_exponents:
                prime_exponents[temp] = []
            prime_exponents[temp].append(1)
            
    total_ans = 1
    
    # For each prime, calculate the contribution
    # Contribution = Sum over all valid paths of (Product of p^(x_k) for k=1..N)
    # = Sum over all valid paths of p^(Sum_{k=1}^N x_k)
    # where x_k are exponents of prime p in S_k.
    # Constraints: |x_k - x_{k+1}| = c_k, min(x_k) = 0.
    # Let P_k be a path sum such that x_k = P_{k-1} - min(P).
    # We sum p^(Sum P_{k-1} - N * min(P)).
    # Using DP state d = current_P - min_P (which is x_k):
    # Transition Up (+c): d -> d + c. Multiplier p^(d+c).
    # Transition Down (-c): d -> 0. Multiplier p^0 = 1.
    
    for p, exponents in prime_exponents.items():
        # exponents is a list of length N-1
        # dp[d] stores the sum of p^(sum Q) for paths ending with diff d
        # Max possible d is sum(exponents)
        max_d = sum(exponents)
        dp = [0] * (max_d + 1)
        dp[0] = 1
        
        for c in exponents:
            new_dp = [0] * (max_d + 1)
            
            # Optimization: track current max d to avoid iterating zeros
            # However, with max_d <= 10000, iterating full array is fast enough.
            # We iterate up to max_d.
            
            for d in range(len(dp)):
                if dp[d] == 0:
                    continue
                
                val = dp[d]
                
                # Option 1: Up (+c)
                # New diff = d + c
                # Multiplier = p^(d+c)
                if d + c <= max_d:
                    term = val * pow(p, d + c, MOD)
                    new_dp[d + c] = (new_dp[d + c] + term) % MOD
                
                # Option 2: Down (-c)
                # New diff = 0
                # Multiplier = p^0 = 1
                term = val
                new_dp[0] = (new_dp[0] + term) % MOD
            
            dp = new_dp
        
        total_ans = (total_ans * sum(dp)) % MOD

    print(total_ans)

if __name__ == '__main__':
    solve()