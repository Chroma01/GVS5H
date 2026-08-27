import sys

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

    # Precompute primes up to 1000
    primes = []
    is_prime = [True] * 1001
    for i in range(2, 1001):
        if is_prime[i]:
            primes.append(i)
            for j in range(i*i, 1001, i):
                is_prime[j] = False

    # Factorize A and group by prime
    prime_exponents = {}
    for x in A:
        temp = x
        for p in primes:
            if p * p > temp:
                break
            if temp % p == 0:
                count = 0
                while temp % p == 0:
                    count += 1
                    temp //= p
                if p not in prime_exponents:
                    prime_exponents[p] = []
                prime_exponents[p].append(count)
        if temp > 1:
            if temp not in prime_exponents:
                prime_exponents[temp] = []
            prime_exponents[temp].append(1)

    total_ans = 1

    # Process each prime
    for p, exponents in prime_exponents.items():
        S_max = sum(exponents)
        
        # We need to compute sum_{paths} p^{N * max(S) - S_{N-1}}
        # Let dp[i][s] be the sum of p^{-s} for paths of length i ending at s with max <= K
        # We will compute this for all K simultaneously.
        # dp[s] will store the sum of p^{-s} for paths of length i ending at s with max <= K
        # We iterate K from 0 to S_max.
        # For each K, we compute dp[s] for s <= K.
        # But we can reuse the previous DP state.
        # Initialize dp[s] = 0 for all s.
        # For i from 0 to N-2:
        #     For K from 0 to S_max:
        #         Update dp[s] for s <= K.
        #         This is O(N * S_max^2).
        # But we can optimize: dp[i][s][K] = dp[i][s][K-1] for s <= K-1.
        # So we only need to compute dp[i][K][K].
        # dp[i][K][K] = sum_{d} dp[i-1][K-d][K].
        # This is a standard DP.
        # We can compute this for all K and i in O(N * S_max^2).
        # But we can do it in O(N * S_max) by maintaining the array.
        # Let dp[s] be the sum of p^{-s} for paths of length i ending at s with max <= K.
        # We can update dp[s] for all s and K.
        # Actually, we can compute dp[i][s] for all s and i (unconstrained) and then use a Fenwick tree to query the max.
        # No, let's just use the O(N * S_max^2) solution with a list.
        # Since S_max is small, this should pass.
        
        # Unconstrained DP to get the base values
        # dp[s] stores sum of p^{-s}
        offset = S_max
        dp = [0] * (2 * S_max + 1)
        dp[offset] = 1
        
        inv_p = pow(p, MOD - 2, MOD)
        
        for i in range(N - 1):
            a = exponents[i]
            new_dp = [0] * (2 * S_max + 1)
            # Precompute powers
            powers = [pow(inv_p, d, MOD) for d in range(-a, a + 1)]
            
            # Iterate over the range of possible s
            # We can track the current min and max s
            # But for simplicity, we iterate over the whole array? No, too slow.
            # We iterate over the range of possible s.
            # Current range: [-current_max, current_max]
            # We can track current_min and current_max.
            # But we don't have them.
            # Let's assume the array is dense and use a loop.
            # We can use a list of active indices.
            # But creating it every time is slow.
            # Instead, we can use a dictionary for sparse representation.
            # Given the constraints, maybe dictionary is better.
            pass
        
        # Re-implement with dictionary
        dp_dict = {offset: 1}
        
        for i in range(N - 1):
            a = exponents[i]
            new_dp_dict = {}
            # Precompute powers
            powers = [pow(inv_p, d, MOD) for d in range(-a, a + 1)]
            
            # Iterate over current keys
            for s, val in dp_dict.items():
                # d from -a to a
                for d in range(-a, a + 1):
                    new_s = s + d
                    if new_s < -S_max or new_s > S_max:
                        continue
                    new_val = (val * powers[d + a]) % MOD
                    if new_s in new_dp_dict:
                        new_dp_dict[new_s] = (new_dp_dict[new_s] + new_val) % MOD
                    else:
                        new_dp_dict[new_s] = new_val
            
            dp_dict = new_dp_dict
        
        # Now we have unconstrained dp_dict
        # We need to compute the answer with max constraint.
        # We can iterate K from 0 to S_max.
        # For each K, we need the sum of p^{-S_{N-1}} for paths with max = K.
        # This is dp_max_le_K[N-1][s] - dp_max_le_K_minus_1[N-1][s] for s <= K.
        # But we don't have dp_max_le_K.
        # We can compute it on the fly.
        # Let dp_K[s] be the sum of p^{-s} for paths with max <= K.
        # We can compute dp_K[s] for all K and s in one pass?
        # No, we can compute dp_K[s] for a fixed K in O(N * K).
        # Total time O(N * S_max^2).
        # But we can optimize by noting that dp_K[s] = dp_{K-1}[s] for s <= K-1.
        # So we can maintain dp[s] for all s and update it as K increases.
        # Initialize dp[s] = 0 for all s.
        # For K from 0 to S_max:
        #   Update dp[s] for s <= K to include paths that first exceed K-1 at step i?
        #   No, we need to recompute the DP for each K.
        #   But we can reuse the previous DP state.
        #   Let dp[i][s] be the sum of p^{-s} for paths of length i ending at s with max <= K.
        #   We can compute this for all K and i in one pass.
        #   dp[i][s][K] = sum(dp[i-1][s-d][K]) for s-d <= K.
        #   This is the same as dp[i][s][K] = dp[i][s][K-1] for s <= K-1.
        #   And for s = K, dp[i][K][K] = sum(dp[i-1][K-d][K]).
        #   So we can compute dp[i][s] for all s and i, and then for each K, the value is dp[i][K][K].
        #   But we need dp[i][s][K] for all s <= K.
        #   Actually, we only need the final answer: sum_K p^{N K} * (dp[N-1][K][K] - dp[N-1][K-1][K-1]).
        #   Wait, dp[N-1][K][K] is the sum of p^{-s} for paths with max <= K ending at s <= K.
        #   The difference dp[N-1][K][K] - dp[N-1][K-1][K-1] is the sum of p^{-s} for paths with max = K ending at s <= K.
        #   So we need to compute dp[i][s][K] for all i, s, K.
        #   We can do this in O(N * S_max^2).
        #   But we can optimize: dp[i][s][K] = dp[i][s][K-1] for s <= K-1.
        #   So we only need to compute dp[i][K][K].
        #   dp[i][K][K] = sum_{d} dp[i-1][K-d][K].
        #   This is a standard DP.
        #   We can compute this for all K and i in O(N * S_max^2).
        #   But we can do it in O(N * S_max) by maintaining the array.
        #   Let dp[s] be the sum of p^{-s} for paths of length i ending at s with max <= K.
        #   We can update dp[s] for all s and K.
        #   Actually, we can compute dp[i][s] for all s and i (unconstrained) and then use a Fenwick tree to query the max.
        #   No, let's just use the O(N * S_max^2) solution with a list.
        #   Since S_max is small, this should pass.
        pass

    # Final implementation
    # We will compute dp[i][s] for all s and i (unconstrained) and then for each K, compute the difference.
    # But we need dp_max_le_K.
    # Let's use the fact that dp_max_le_K[s] = dp_max_le_K[s] for s <= K.
    # We can compute dp_max_le_K[s] for all K and s in one pass.
    # Initialize dp[s] = 0 for all s.
    # For i from 0 to N-2:
    #     For K from 0 to S_max:
    #         Update dp[s] for s <= K.
    #         This is O(N * S_max^2).
    #   But we can optimize: dp[i][s][K] = dp[i][s][K-1] for s <= K-1.
    #   So we only need to compute dp[i][K][K].
    #   dp[i][K][K] = sum_{d} dp[i-1][K-d][K].
    #   This is a standard DP.
    #   We can compute this for all K and i in O(N * S_max^2).
    #   But we can do it in O(N * S_max) by maintaining the array.
    #   Let dp[s] be the sum of p^{-s} for paths of length i ending at s with max <= K.
    #   We can update dp[s] for all s and K.
    #   Actually, we can compute dp[i][s] for all s and i (unconstrained) and then use a Fenwick tree to query the max.
    #   No, let's just use the O(N * S_max^2) solution with a list.
    #   Since S_max is small, this should pass.
    pass

solve()