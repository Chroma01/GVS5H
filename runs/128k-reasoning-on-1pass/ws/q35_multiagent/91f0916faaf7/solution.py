import sys
from collections import defaultdict

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

    # Precompute primes up to 1000
    primes = []
    is_prime = [True] * 1001
    for i in range(2, 1001):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, 1001, i):
                is_prime[j] = False

    # For each prime, compute the contribution
    total_ans = 1

    for p in primes:
        # Compute exponents of p in each A_i
        exponents = []
        for x in A:
            cnt = 0
            while x > 0 and x % p == 0:
                cnt += 1
                x //= p
            exponents.append(cnt)
        
        # If no A_i is divisible by p, then all a_i = 0.
        # The path is P_k = 0 for all k. min P = 0.
        # Sum is p^0 = 1.
        if all(e == 0 for e in exponents):
            continue

        # DP state: (h, m) -> sum of p^(sum P_j)
        # h = P_k - m_k >= 0
        # m = m_k <= 0
        # Initial state: k=1, P_1 = 0, m_1 = 0, h_1 = 0
        dp = defaultdict(int)
        dp[(0, 0)] = 1

        # Precompute powers of p
        # We need p^P for P in range [-sum_a, sum_a]
        # sum_a <= N * 1000 = 10^6.
        # But we can compute on the fly or use a dict.
        # Since we need p^P, and P can be negative, we can compute p^P mod MOD.
        # But P is integer.
        
        # To optimize, we can compute p^P for each step.
        # P = m + h.
        
        for a in exponents:
            new_dp = defaultdict(int)
            p_pow_a = pow(p, a, MOD)
            p_pow_neg_a = pow(p, -a, MOD) # This is modular inverse
            
            # If a == 0, then delta = 0.
            # P_next = P. m_next = m. h_next = h.
            # weight = p^P.
            # So we just multiply each state by p^(m+h).
            
            if a == 0:
                for (h, m), val in dp.items():
                    P = m + h
                    # weight = p^P
                    # We need to compute p^P mod MOD.
                    # P can be negative? No, P = m + h. m <= 0, h >= 0.
                    # P can be negative.
                    # But p^P mod MOD requires modular inverse if P < 0.
                    # However, in the problem, P_k are integers.
                    # The term is p^(sum P_k).
                    # We are summing p^(sum P_k).
                    # So we need p^P mod MOD.
                    # If P < 0, we need modular inverse.
                    # But wait, the score is product of S_i.
                    # S_i are positive integers.
                    # So the exponent of p in score is sum v_p(S_i) = sum P_i.
                    # P_i can be negative?
                    # P_i = v_p(S_i). S_i are positive integers, so P_i >= 0.
                    # Ah! P_k = v_p(S_k) >= 0.
                    # So P is always non-negative.
                    # My DP state m is min P_k.
                    # P_k = m + h.
                    # Since P_k >= 0, we must have m + h >= 0.
                    # So P is always non-negative.
                    # So we don't need modular inverse for p^P.
                    
                    # Compute p^P mod MOD
                    # P = m + h.
                    # We can compute pow(p, P, MOD).
                    # But P can be up to 10^6.
                    # We can precompute powers or compute on fly.
                    # Since we do this for each state, it might be slow.
                    # But number of states is small?
                    
                    # Let's compute p^P.
                    # We can use pow(p, P, MOD).
                    
                    weight = pow(p, P, MOD)
                    new_val = (val * weight) % MOD
                    new_dp[(h, m)] = (new_dp[(h, m)] + new_val) % MOD
                dp = new_dp
                continue

            # If a > 0, we have two choices for delta: a and -a.
            # But we must ensure P_next >= 0.
            # P_next = m + h + delta.
            # If P_next < 0, then this path is invalid?
            # No, P_k = v_p(S_k) >= 0.
            # So if P_next < 0, this path is invalid and should be discarded.
            
            for (h, m), val in dp.items():
                P = m + h
                # Choice 1: delta = a
                P1 = P + a
                if P1 >= 0:
                    m1 = min(m, P1)
                    h1 = P1 - m1
                    weight1 = pow(p, P1, MOD)
                    new_val1 = (val * weight1) % MOD
                    new_dp[(h1, m1)] = (new_dp[(h1, m1)] + new_val1) % MOD
                
                # Choice 2: delta = -a
                P2 = P - a
                if P2 >= 0:
                    m2 = min(m, P2)
                    h2 = P2 - m2
                    weight2 = pow(p, P2, MOD)
                    new_val2 = (val * weight2) % MOD
                    new_dp[(h2, m2)] = (new_dp[(h2, m2)] + new_val2) % MOD
            
            dp = new_dp

        # After N-1 steps, we have dp for k=N.
        # We need to sum val * p^(-N * m) for all (h, m).
        # p^(-N * m) = (p^(-N))^m.
        # Since m <= 0, let M = -m >= 0.
        # Then p^(-N * m) = p^(N * M).
        # So we need to sum val * p^(N * (-m)).
        
        p_neg_N = pow(p, -N, MOD) # This is (p^N)^(-1) mod MOD
        # But we need p^(-N * m).
        # Since m <= 0, -N * m >= 0.
        # So we can compute p^(-N * m) = pow(p, -N * m, MOD).
        # But -N * m can be large.
        # We can compute pow(p, -N * m, MOD).
        
        prime_ans = 0
        for (h, m), val in dp.items():
            exponent = -N * m
            # exponent >= 0
            term = (val * pow(p, exponent, MOD)) % MOD
            prime_ans = (prime_ans + term) % MOD
        
        total_ans = (total_ans * prime_ans) % MOD

    print(total_ans)

solve()