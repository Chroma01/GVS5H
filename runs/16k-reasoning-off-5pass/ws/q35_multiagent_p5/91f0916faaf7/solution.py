import sys
from math import gcd
from collections import defaultdict

# Increase recursion depth just in case
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

    # Precompute valid pairs (u, v) for each A_i such that u*v = A_i and gcd(u, v) == 1.
    # These represent the possible reduced fractions S_i / S_{i+1}.
    choices = []
    for val in A:
        pairs = []
        # Iterate over divisors u of val
        for u in range(1, int(val**0.5) + 1):
            if val % u == 0:
                v = val // u
                if gcd(u, v) == 1:
                    pairs.append((u, v))
                if u != v:
                    if gcd(v, u) == 1:
                        pairs.append((v, u))
        choices.append(pairs)

    # DP state: dp[(u, v)][L] = {'sum_scores': int, 'gcd_sum': defaultdict(int)}
    # (u, v) represents the reduced fraction S_i / S_1.
    # L represents the current LCM of the denominators M_k for k=1..i.
    # M_k is the denominator of S_k / S_1 when reduced.
    # sum_scores: Sum of products s_1 * ... * s_i for all paths leading to this state.
    # gcd_sum[g]: Sum of products s_1 * ... * s_i for all paths leading to this state where gcd(s_1, ..., s_i) = g.
    
    # Initial state: i=1, S_1/S_1 = 1/1.
    # M_1 = 1 (denominator of 1/1).
    # L_1 = 1.
    # s_1 = L_1 * (1/1) = 1.
    # gcd(s_1) = 1.
    # Score = 1.
    dp = defaultdict(lambda: defaultdict(lambda: {'sum_scores': 0, 'gcd_sum': defaultdict(int)}))
    dp[(1, 1)][1]['sum_scores'] = 1
    dp[(1, 1)][1]['gcd_sum'][1] = 1

    for i in range(N - 1):
        new_dp = defaultdict(lambda: defaultdict(lambda: {'sum_scores': 0, 'gcd_sum': defaultdict(int)}))
        pairs = choices[i]
        
        for (u, v), L_dict in dp.items():
            for L, info in L_dict.items():
                current_sum_scores = info['sum_scores']
                current_gcd_sum = info['gcd_sum']
                
                if current_sum_scores == 0:
                    continue
                
                for (u_next, v_next) in pairs:
                    # New ratio S_{i+1}/S_1 = (u/v) * (v_next/u_next) = (u * v_next) / (v * u_next)
                    num = u * v_next
                    den = v * u_next
                    g = gcd(num, den)
                    u_new = num // g
                    v_new = den // g
                    
                    # M_{i+1} = v_new
                    # Update L: L_{new} = lcm(L, v_new)
                    g_lcm = gcd(L, v_new)
                    new_L = (L // g_lcm) * v_new
                    
                    # s_{i+1} = new_L * (u_new / v_new)
                    # Since s_{i+1} must be an integer, v_new divides new_L * u_new.
                    # Since gcd(u_new, v_new) = 1, v_new must divide new_L.
                    # So s_{i+1} = (new_L // v_new) * u_new
                    s_next = (new_L // v_new) * u_new
                    
                    # Update sum_scores
                    new_sum_scores = (current_sum_scores * s_next) % MOD
                    
                    # Update gcd_sum
                    # For each existing gcd g_old, new_g = gcd(g_old, s_next)
                    # The contribution to new_g is current_gcd_sum[g_old] * s_next
                    
                    if new_L not in new_dp[(u_new, v_new)]:
                        new_dp[(u_new, v_new)][new_L] = {'sum_scores': 0, 'gcd_sum': defaultdict(int)}
                    
                    target = new_dp[(u_new, v_new)][new_L]
                    target['sum_scores'] = (target['sum_scores'] + new_sum_scores) % MOD
                    
                    for g_old, val in current_gcd_sum.items():
                        new_g = gcd(g_old, s_next)
                        target['gcd_sum'][new_g] = (target['gcd_sum'][new_g] + val * s_next) % MOD

        dp = new_dp

    # Final answer is sum of gcd_sum[1] for all states
    ans = 0
    for u_v, L_dict in dp.items():
        for L, info in L_dict.items():
            ans = (ans + info['gcd_sum'].get(1, 0)) % MOD
            
    print(ans)

solve()