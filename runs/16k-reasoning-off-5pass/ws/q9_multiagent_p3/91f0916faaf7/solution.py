import sys

# Increase recursion depth just in case, though we use iterative DP
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
    MAX_VAL = 1000
    primes = []
    is_prime = [True] * (MAX_VAL + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, MAX_VAL + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, MAX_VAL + 1, i):
                is_prime[j] = False
    
    # Precompute prime factorization for numbers up to 1000
    # factors[x] will be a list of (prime, exponent)
    factors = [[] for _ in range(MAX_VAL + 1)]
    for p in primes:
        for i in range(p, MAX_VAL + 1, p):
            count = 0
            temp = i
            while temp % p == 0:
                count += 1
                temp //= p
            if count > 0:
                factors[i].append((p, count))

    total_score = 1
    
    # For each prime, calculate its contribution
    for p in primes:
        # Identify which A_i have this prime factor
        # We need to process the sequence of exponents e_i = v_p(A_i)
        # If e_i > 0, we have a choice of sign (+e_i or -e_i)
        # If e_i == 0, the difference is 0 (no choice)
        
        # Let's collect the exponents and their indices
        # We need to sum over all 2^(count of non-zero e_i) sign patterns
        # For each pattern, we compute the sum of exponents in the sequence S
        
        # Let's define the state as we iterate through the sequence
        # We need to track the minimum value of the prefix sum of deltas relative to the start
        # Actually, we can use DP.
        # Let dp[i][min_val] = sum of (p^(sum of x_1...x_i)) for sequences of length i
        # where the minimum value in x_1...x_i is exactly min_val.
        # However, min_val can be negative.
        # The range of min_val is bounded by the sum of absolute values of e_j.
        # Max sum of e_j is roughly (N-1) * 10 (since 2^10 > 1000). N=1000.
        # So range is roughly -10000 to 10000. This is too large for a direct DP table if we are not careful.
        # But wait, we don't need the exact min_val in the state if we normalize.
        
        # Alternative approach:
        # For a fixed sign pattern, the sequence of exponents x is determined by x_1 = k.
        # x_i = k + delta_i, where delta_1 = 0, delta_{i+1} = delta_i + s_i * e_i.
        # Condition: min(x) = 0 => k + min(delta) = 0 => k = -min(delta).
        # Since x_i >= 0 is guaranteed by k = -min(delta), this is the unique solution for a pattern.
        # Contribution = p^(sum(x)) = p^(N*k + sum(delta)).
        # We need to sum this over all valid sign patterns.
        # A sign pattern is valid if it produces a sequence of integers (always true) and we just sum the contributions.
        # Wait, is there any constraint on the signs?
        # The problem says "f(S_i/S_{i+1}) = A_i".
        # This implies S_i/S_{i+1} = u/v with u*v = A_i and gcd(u,v)=1.
        # This means v_p(u) + v_p(v) = e_i and v_p(u)*v_p(v) = 0.
        # So v_p(u) = e_i, v_p(v) = 0 OR v_p(u) = 0, v_p(v) = e_i.
        # This corresponds to x_i - x_{i+1} = e_i or x_i - x_{i+1} = -e_i.
        # So yes, for each i with e_i > 0, we have exactly 2 choices.
        # For e_i = 0, we have 1 choice (diff = 0).
        # So we just sum p^(N*k + sum(delta)) over all 2^M patterns, where M is count of non-zero e_i.
        
        # We can use DP to compute this sum without iterating all 2^M patterns.
        # State: dp[i][current_delta_sum][min_delta] ?
        # No, we need sum(delta) and min(delta).
        # Let's shift the min_delta to be non-negative.
        # Let min_delta be the minimum value encountered so far.
        # Let current_sum be the sum of deltas so far.
        # We want to compute sum over all paths of p^(N * (-min_delta) + current_sum).
        # = p^(current_sum) * (p^(-min_delta))^N.
        # Let's define state as (i, current_sum, min_delta).
        # Since current_sum can be large, we can't use it as a direct index.
        # However, notice that current_sum = sum of signed e_j.
        # The term is p^(current_sum - N * min_delta).
        # Let's rewrite the exponent: E = current_sum - N * min_delta.
        # We want to sum p^E.
        # Notice that min_delta is non-increasing (it can only decrease or stay same).
        # current_sum changes by +e_i or -e_i.
        # The range of current_sum is roughly [-10000, 10000].
        # The range of min_delta is roughly [-10000, 0].
        # This is still potentially large (20000 * 10000 states).
        # But N is up to 1000. The number of steps is 1000.
        # Is there a way to optimize?
        
        # Observation: The value of min_delta only matters relative to the current_sum.
        # Actually, let's look at the structure.
        # We are summing p^(sum(x)).
        # Let's consider the contribution of each prime independently.
        # Let's try to map the state to something smaller.
        # Notice that the "shape" of the sequence of deltas is determined by the signs.
        # The value of min_delta is determined by the prefix minimums.
        # Let's define dp[i][m] = sum of p^(sum of x_1...x_i) for sequences of length i
        # where the minimum value in the sequence is exactly m (relative to x_1=0? No, absolute).
        # But we can normalize. Let's say we fix the minimum to be 0.
        # Then x_i = y_i + k, where min(y) = 0.
        # Then sum(x) = N*k + sum(y).
        # And k = -min(delta).
        # So we need to sum p^(N*(-min(delta)) + sum(delta)).
        # Let's define a DP where we track (current_sum, min_delta).
        # But current_sum and min_delta are correlated.
        # Actually, we can just track (current_sum, min_delta) but notice that min_delta <= 0.
        # Let m = -min_delta (so m >= 0).
        # We want to sum p^(current_sum + N*m).
        # Transitions:
        # From state (s, m) at step i:
        # Next e = e_{i+1}.
        # Option 1: new_s = s + e. new_m = m if s+e >= -m else -(s+e).
        # Option 2: new_s = s - e. new_m = m if s-e >= -m else -(s-e).
        # Wait, if s+e < -m, then the new minimum is s+e, so new_m = -(s+e).
        # If s+e >= -m, the minimum doesn't change, so new_m = m.
        # This looks like we can just track (s, m).
        # The range of s is [-10000, 10000]. The range of m is [0, 10000].
        # This is 2*10^7 states. With N=1000, total operations 2*10^10. Too slow.
        
        # We need a better approach.
        # Let's reconsider the problem.
        # We are summing p^(sum(x)) over all valid sequences x.
        # A sequence x is valid if x_i - x_{i+1} = +/- e_i and min(x) = 0.
        # This is equivalent to: x_i = k + delta_i, where delta_1=0, delta_{i+1} = delta_i +/- e_i, and k = -min(delta).
        # So we sum p^(N*k + sum(delta)) = p^(N*(-min(delta)) + sum(delta)).
        # Let's define f(i, s, m) = sum of p^(sum(delta_1...delta_i)) for sequences of length i
        # ending with delta_i = s, and min(delta_1...delta_i) = -m.
        # Then the answer is sum over all valid final states of p^(N*m + s).
        # Wait, the term is p^(N*m + s).
        # Notice that s = delta_i.
        # The transitions:
        # f(i, s, m) -> f(i+1, s+e, m') + f(i+1, s-e, m')
        # where m' = m if s+e >= -m else -(s+e).
        # This is still the same complexity.
        
        # Is there a property we missed?
        # Maybe the number of distinct values of (s, m) reachable is small?
        # Or maybe we can swap the order of summation?
        # Sum over all sign patterns of p^(N*(-min(delta)) + sum(delta)).
        # Let's consider the contribution of each "valley" (where the minimum is achieved).
        # Actually, let's look at the constraints again.
        # N <= 1000. A_i <= 1000.
        # The maximum possible sum of e_i is 1000 * 10 = 10000.
        # But maybe the number of reachable states (s, m) is not that large?
        # Or maybe we can use the fact that we only care about the final sum.
        
        # Let's try a different DP state.
        # Instead of tracking absolute s and m, let's track the relative values.
        # But the absolute values matter for the exponent.
        
        # Let's re-evaluate the complexity.
        # The number of steps is N.
        # At each step, we have a set of reachable (s, m) pairs.
        # How many such pairs?
        # s is the current sum. m is the magnitude of the minimum.
        # Note that m = -min(s_1, ..., s_i).
        # Also s_i = s_{i-1} +/- e_{i-1}.
        # So s_i is always a linear combination of e_j with coefficients in {0, 1, -1}.
        # The number of such combinations is 2^i.
        # But many might map to the same (s, m).
        # However, we need to sum p^(N*m + s).
        # Let's try to compute this using a map or dictionary for the DP states.
        # Since N is small (1000), maybe the number of distinct (s, m) pairs is not too large?
        # Let's simulate for a worst case: e_i = 10 for all i.
        # s grows by 10 or -10. m grows if s drops below -m.
        # The number of distinct s values is roughly 2*N*10 = 20000.
        # For each s, m is determined? No.
        # Example: path +10, -10, +10 -> s=10, m=0.
        # path -10, +10, -10 -> s=-10, m=10.
        # path -10, -10, +10 -> s=-10, m=20.
        # It seems m is determined by the minimum prefix sum.
        # So the state is just (s, m).
        # Is the number of reachable (s, m) pairs small?
        # In the worst case, s can be anything in [-10000, 10000].
        # And m can be anything in [0, 10000].
        # But they are coupled. m = -min(s_1, ..., s_i).
        # So m >= -s_k for some k <= i.
        # This doesn't restrict the number of pairs much.
        
        # Wait, N <= 1000. Time limit is usually 2s.
        # 2*10^7 operations is acceptable in C++, but in Python it might be tight.
        # However, we only process primes. There are 168 primes up to 1000.
        # But most primes don't divide many A_i.
        # For a prime p, let M_p be the number of A_i divisible by p.
        # If M_p is small, the number of steps where we have a choice is small.
        # If M_p is large, then p is small (like 2, 3, 5).
        # For p=2, M_p could be ~1000.
        # But for p=2, e_i is usually small (1 or 2).
        # Let's check the constraints again.
        # Maybe we can optimize the DP.
        # Notice that the transitions are linear.
        # We are summing p^(N*m + s).
        # Let's define DP[i][s] = sum of p^(sum(delta)) * p^(N * m) ?
        # No, m depends on the history.
        # But notice that m only changes when s drops below the current minimum.
        # Let's define DP[i][s] = sum of p^(sum(delta)) * p^(N * m) for all paths ending at s with min = -m.
        # When we transition from s to s+e:
        # If s+e >= -m, then m stays same. Contribution: p^(N*m) * p^(sum) -> p^(N*m) * p^(sum+e).
        # If s+e < -m, then new m' = -(s+e). Contribution: p^(N*m') * p^(sum+e).
        # The problem is that the term p^(N*m) is different for different histories with the same s.
        # So we cannot just store one value per s.
        # We need to store a distribution of m for each s.
        # But m is determined by the minimum.
        # Actually, for a fixed s, m can take multiple values?
        # Yes. Example: e=[10, 10].
        # Path +10, -10 -> s=0, min=-10? No.
        # Start 0.
        # +10 -> s=10, min=0.
        # -10 -> s=0, min=0.
        # Path -10, +10 -> s=0, min=-10.
        # So for s=0, we can have m=0 or m=10.
        # So we need DP[i][s][m].
        # This is the same as before.
        
        # Is there a way to reduce the state space?
        # Notice that m is always one of the values {-s_k} for some k <= i.
        # So m is always a value that appeared as a prefix sum (negated).
        # The number of such values is at most i.
        # So for each s, we have at most i possible values of m.
        # Total states: sum_{i=1}^N (range of s) * i.
        # Range of s is 20000. i is 1000. Total 2*10^7.
        # This is the same complexity.
        # But in practice, the number of reachable (s, m) pairs might be much smaller than the theoretical bound.
        # Also, we can use a dictionary to store only reachable states.
        # Given N=1000 and A_i=1000, let's hope the number of reachable states is manageable.
        # We can use a dictionary: dp[s] = {m: value}.
        # Or better: dp[s] = list of (m, value).
        # Since we process primes one by one, and for each prime we do N steps.
        # Let's implement this with a dictionary.
        
        # Optimization:
        # Instead of (s, m), let's use (s, m) but note that m is always >= 0.
        # And s can be negative.
        # We can shift s by adding a large constant to make it non-negative index if needed, but dict handles negative keys.
        
        # Let's refine the DP state and transitions.
        # dp[s] = dictionary mapping m -> sum of p^(sum(delta))
        # Initially: dp[0] = {0: 1} (s=0, m=0, sum=1)
        # For each e in exponents:
        #   new_dp = defaultdict(lambda: defaultdict(int))
        #   for s, m_dict in dp.items():
        #       for m, val in m_dict.items():
        #           # Option 1: +e
        #           ns = s + e
        #           if ns >= -m:
        #               nm = m
        #           else:
        #               nm = -ns
        #           new_dp[ns][nm] = (new_dp[ns][nm] + val) % MOD
        #           
        #           # Option 2: -e
        #           ns = s - e
        #           if ns >= -m:
        #               nm = m
        #           else:
        #               nm = -ns
        #           new_dp[ns][nm] = (new_dp[ns][nm] + val) % MOD
        #   dp = new_dp
        #
        # Finally, sum over all s, m: val * p^(N*m + s).
        # Wait, the term is p^(N*m + s).
        # In the DP, we stored p^(sum(delta)).
        # So we multiply by p^(N*m + s).
        # Note: s here is the final delta_N.
        # And m is the final min magnitude.
        # The exponent is N*m + s.
        # Wait, is it N*m + s?
        # sum(x) = N*k + sum(delta) = N*(-m) + sum(delta).
        # So exponent is sum(delta) - N*m.
        # My previous derivation: k = -min(delta) = -(-m) = m?
        # Let's recheck.
        # min(delta) = -m.
        # k = -min(delta) = m.
        # x_i = k + delta_i = m + delta_i.
        # sum(x) = N*m + sum(delta).
        # Yes, exponent is N*m + sum(delta).
        # So we need to multiply by p^(N*m + s).
        # Wait, s in the DP is sum(delta).
        # So term is val * p^(N*m + s).
        
        # Complexity check:
        # Number of states (s, m).
        # s is sum of +/- e. m is max prefix sum magnitude.
        # For e_i=10, s ranges in [-10000, 10000]. m ranges in [0, 10000].
        # But they are correlated.
        # If s is large positive, m is likely small.
        # If s is large negative, m is likely large.
        # The number of pairs (s, m) might be O(N * max_e).
        # max_e is 10. N is 1000. So 10000 states?
        # If so, 1000 * 10000 = 10^7 operations per prime.
        # With 168 primes, total 1.6 * 10^9. Too slow for Python.
        # We need a faster way.
        
        # Is there a pattern?
        # Notice that the transitions are symmetric.
        # Maybe we can use the fact that we only care about the final sum.
        # Let's reconsider the problem structure.
        # We are summing p^(sum(x)) over all valid x.
        # Valid x means x_i - x_{i+1} = +/- e_i and min(x) = 0.
        # This is equivalent to: x_i = m + delta_i, where delta_1=0, delta_{i+1} = delta_i +/- e_i, and m = -min(delta).
        # We want sum_{patterns} p^(N*m + sum(delta)).
        # Let's define F(i, s, m) = sum of p^(sum(delta)) for patterns of length i ending at s with min=-m.
        # We want sum_{s, m} F(N, s, m) * p^(N*m + s).
        # Notice that the term p^(N*m + s) can be factored out if we group by m?
        # No, s varies.
        # But notice that for a fixed m, the possible values of s are constrained.
        # s = sum(delta). min(delta) = -m.
        # This means all prefix sums are >= -m, and at least one is -m.
        # Let's change variables. Let y_i = delta_i + m.
        # Then y_i >= 0, and min(y) = 0.
        # y_{i+1} = y_i + e_i or y_i - e_i.
        # We want sum p^(N*m + sum(y_i) - N*m) = sum p^(sum(y_i)).
        # Wait, sum(delta) = sum(y_i) - N*m.
        # So exponent is N*m + sum(y_i) - N*m = sum(y_i).
        # So we just need to sum p^(sum(y_i)) over all sequences y of length N such that:
        # y_1 = m (since delta_1=0 => y_1=m).
        # y_{i+1} = y_i +/- e_i.
        # y_i >= 0 for all i.
        # min(y) = 0.
        # But m is not fixed! m is determined by the sequence.
        # Actually, for a fixed pattern of signs, m is fixed (it's the max of the "dip" below 0).
        # But we are summing over patterns.
        # Let's rephrase:
        # We want to sum p^(sum(y_i)) over all sequences y such that:
        # y_1 >= 0, y_{i+1} = y_i +/- e_i, y_i >= 0, and min(y) = 0.
        # Wait, if min(y) = 0, then there exists some k such that y_k = 0.
        # And y_1 = m.
        # But m is not part of the sequence definition in this new view.
        # The sequence y is defined by y_1 and the signs.
        # But y_1 is not fixed.
        # Actually, the original problem has x_1 = k.
        # x_i = k + delta_i.
        # min(x) = 0 => k = -min(delta).
        # So x_1 = -min(delta).
        # Let m = -min(delta). Then x_1 = m.
        # And x_i = m + delta_i.
        # The condition min(x)=0 is satisfied by construction.
        # The condition x_i >= 0 is satisfied.
        # The transitions are x_{i+1} = x_i +/- e_i.
        # So we are looking for sequences x such that:
        # x_1 >= 0, x_{i+1} = x_i +/- e_i, x_i >= 0, and min(x) = 0.
        # And we sum p^(sum(x)).
        # This is much simpler!
        # We don't need to track m explicitly.
        # We just need to track the current value x_i and the minimum value seen so far.
        # But we know min(x) must be 0 at the end.
        # So we can compute the sum of p^(sum(x)) for all sequences with min(x) >= 0, and then subtract those with min(x) >= 1?
        # No, because the condition is min(x) = 0.
        # Let S be the set of sequences with x_i >= 0.
        # We want sum_{x in S, min(x)=0} p^(sum(x)).
        # Let T_k be the set of sequences with x_i >= k.
        # Then we want sum_{x in T_0} p^(sum(x)) - sum_{x in T_1} p^(sum(x)).
        # Because if min(x) >= 1, then x_i >= 1 for all i.
        # If min(x) = 0, then x_i >= 0 and not (x_i >= 1).
        # So the answer is (Sum for min>=0) - (Sum for min>=1).
        # Now, for a fixed k, the problem is:
        # Count sequences x such that x_i >= k, x_{i+1} = x_i +/- e_i.
        # Let y_i = x_i - k. Then y_i >= 0.
        # y_{i+1} = y_i +/- e_i.
        # This is the same problem as before but with x_1 >= k.
        # Wait, the starting condition is x_1 >= k.
        # But x_1 is not fixed.
        # Actually, the recurrence is x_{i+1} = x_i +/- e_i.
        # This means x_i = x_1 + sum_{j=1}^{i-1} s_j * e_j.
        # Let delta_i = sum_{j=1}^{i-1} s_j * e_j (with delta_1 = 0).
        # Then x_i = x_1 + delta_i.
        # Condition x_i >= k => x_1 + delta_i >= k => x_1 >= k - delta_i.
        # So x_1 >= max_i (k - delta_i) = k - min_i(delta_i).
        # Let m = min_i(delta_i). Then x_1 >= k - m.
        # Since we want to sum p^(sum(x)), and sum(x) = N*x_1 + sum(delta).
        # For a fixed pattern (signs), the minimum m is fixed.
        # The valid x_1 are integers >= k - m.
        # But wait, the problem says "good sequence" implies x_i are positive integers.
        # And min(x) = 0.
        # In the decomposition x_i = x_1 + delta_i, we have min(x) = x_1 + min(delta).
        # We require min(x) = 0 => x_1 = -min(delta).
        # So for a fixed pattern, there is exactly ONE valid sequence x.
        # So we don't need to sum over x_1.
        # We just need to sum p^(sum(x)) over all patterns.
        # And sum(x) = N*(-min(delta)) + sum(delta).
        # This brings us back to the original formulation.
        # So the "min>=0" trick doesn't simplify it because the starting point is fixed by the min condition.
        
        # Let's go back to the DP with (s, m).
        # Is it possible that the number of states is small enough?
        # Let's try to implement it efficiently.
        # We can use a dictionary for dp[s] = {m: val}.
        # But we can optimize the inner loop.
        # Notice that for a fixed s, the possible values of m are limited.
        # Also, we can process the primes.
        # For primes that don't divide any A_i, the contribution is 1 (since e_i=0 for all i, only 1 pattern, delta=0, min=0, sum=0, term p^0=1).
        # So we only process primes that divide at least one A_i.
        # For such primes, the number of non-zero e_i is at most N-1.
        # Let's hope the number of reachable states is small.
        # We can use a dictionary and only store reachable states.
        # Also, we can prune states that are not reachable.
        # Let's try to code this.
        
        # One more optimization:
        # Instead of storing {m: val}, we can store a list of (m, val) and merge them.
        # But dict is faster.
        
        # Let's refine the DP state representation.
        # dp = {s: {m: val}}
        # Initial: dp = {0: {0: 1}}
        # For e in exponents:
        #   new_dp = defaultdict(lambda: defaultdict(int))
        #   for s, m_dict in dp.items():
        #       for m, val in m_dict.items():
        #           # +e
        #           ns = s + e
        #           nm = m if ns >= -m else -ns
        #           new_dp[ns][nm] = (new_dp[ns][nm] + val) % MOD
        #           # -e
        #           ns = s - e
        #           nm = m if ns >= -m else -ns
        #           new_dp[ns][nm] = (new_dp[ns][nm] + val) % MOD
        #   dp = new_dp
        
        # Finally, ans = sum(val * pow(p, N*m + s, MOD) for s, m_dict in dp.items() for m, val in m_dict.items())
        
        # Let's hope this passes.
        pass

    # Implementation
    # We need to handle the case where A_i = 1 (e_i = 0).
    # If e_i = 0, then ns = s, nm = m.
    # So the state doesn't change, but we multiply by p^0 = 1.
    # So we can skip e_i = 0.
    
    # Let's collect exponents for each prime.
    prime_exponents = {}
    for i, a in enumerate(A):
        if a == 1:
            continue
        for p, e in factors[a]:
            if p not in prime_exponents:
                prime_exponents[p] = []
            prime_exponents[p].append(e)
            
    # Now run DP for each prime
    for p, es in prime_exponents.items():
        # es is the list of exponents for this prime
        # We need to process them in order
        # dp[s] = {m: val}
        dp = {0: {0: 1}}
        
        for e in es:
            if e == 0:
                continue
            new_dp = {}
            # Use a list of items to avoid modification issues
            for s, m_dict in dp.items():
                # We need to create new entries
                # To optimize, we can collect updates and apply
                # But dict is fine.
                for m, val in m_dict.items():
                    # Option +e
                    ns = s + e
                    if ns >= -m:
                        nm = m
                    else:
                        nm = -ns
                    # Update new_dp
                    if ns not in new_dp:
                        new_dp[ns] = {}
                    if nm not in new_dp[ns]:
                        new_dp[ns][nm] = 0
                    new_dp[ns][nm] = (new_dp[ns][nm] + val) % MOD
                    
                    # Option -e
                    ns = s - e
                    if ns >= -m:
                        nm = m
                    else:
                        nm = -ns
                    if ns not in new_dp:
                        new_dp[ns] = {}
                    if nm not in new_dp[ns]:
                        new_dp[ns][nm] = 0
                    new_dp[ns][nm] = (new_dp[ns][nm] + val) % MOD
            dp = new_dp
        
        # Calculate contribution
        term = 0
        for s, m_dict in dp.items():
            for m, val in m_dict.items():
                # Exponent: N*m + s
                exp = (N * m + s)
                term = (term + val * pow(p, exp, MOD)) % MOD
        total_score = (total_score * term) % MOD

    print(total_score)

solve()