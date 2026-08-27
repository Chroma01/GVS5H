import sys

# Increase recursion depth just in case, though not strictly needed here
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
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    if N == 0:
        print(0)
        return

    # The problem asks for sum_{i=1}^N sum_{j=i}^N f(A_i + A_j).
    # f(x) is x with all factors of 2 removed.
    # We derived that the sum over all pairs (i, j) (including i > j) can be computed in O(V) time,
    # where V = max(A_i + A_j) approx 2*10^7.
    # Specifically, sum_{i, j} f(A_i + A_j) = sum_{k=0}^{24} (2 * (T_k - T_{k+1})) / 2^k,
    # where T_k = sum_{(i, j): A_i + A_j is divisible by 2^k} A_i.
    # T_k can be computed by grouping A_i by their value modulo 2^k.
    # T_k = sum_{r=0}^{2^k-1} count[(2^k - r) % 2^k] * sum[r].
    # The maximum value of A_i is 10^7, so max sum is 2*10^7 < 2^25.
    # We iterate k from 0 to 24. T_25 is implicitly 0.
    
    # Precompute powers of 2
    MODS = [1 << k for k in range(26)]
    
    # We will compute T_k for k in 0..24.
    # T_25 is 0.
    
    # To optimize, we can maintain the count and sum arrays incrementally?
    # No, the modulus changes, so the indices change.
    # But we can just recompute.
    
    # Precompute sum of A to handle k=0 quickly?
    # sum_A = sum(A)
    # T_0 = N * sum_A
    
    # Let's write the loop.
    
    # Precompute T_k values
    T = [0] * 26
    
    # k=0
    # MOD = 1
    # r=0
    # count[0] = N, sum[0] = sum(A)
    # T[0] = count[0] * sum[0] = N * sum(A)
    
    sum_A = sum(A)
    T[0] = N * sum_A
    
    # For k >= 1
    for k in range(1, 25):
        MOD = MODS[k]
        
        # We need count and sum arrays of size MOD
        # Initialize with 0
        # Using a list comprehension is fast
        cnt = [0] * MOD
        s_val = [0] * MOD
        
        # Populate cnt and s_val
        # This loop runs N times
        for x in A:
            r = x % MOD
            cnt[r] += 1
            s_val[r] += x
        
        # Compute T_k
        # T_k = sum_{r=0}^{MOD-1} cnt[(MOD - r) % MOD] * s_val[r]
        # Note: (MOD - r) % MOD is 0 if r=0, else MOD-r.
        # We can iterate r from 0 to MOD-1.
        
        t_k = 0
        
        # Optimization: iterate r
        # For r=0, target is 0.
        # For r>0, target is MOD-r.
        
        # Let's just use a simple loop, it's fast enough in Python for 3.3e7 ops total over all k.
        # But wait, sum(2^k) is 3.3e7. Doing a loop of size 2^k inside the loop over k
        # means total iterations is sum(2^k) = 2^25.
        # So the inner loop runs 3.3e7 times in total across all k.
        # This is acceptable.
        
        # To make it faster, we can avoid the modulo.
        
        term0 = cnt[0] * s_val[0]
        t_k = term0
        
        # For r from 1 to MOD-1
        # target = MOD - r
        # We can iterate r from 1 to MOD-1
        # But iterating in reverse might be cache friendly? Not in Python.
        
        # Let's just loop.
        for r in range(1, MOD):
            t_k += cnt[MOD - r] * s_val[r]
            
        T[k] = t_k
        
    # Now compute the answer
    # Ans = sum_{k=0}^{24} (2 / 2^k) * (T[k] - T[k+1])
    # Note: T[25] = 0
    
    my_formula = 0
    for k in range(25):
        diff = T[k] - T[k+1]
        if diff != 0:
            # Add 2 * diff / 2^k
            # Since diff is integer, and 2^k divides 2*diff?
            # Wait, diff is sum of A_i. A_i are integers.
            # The term is (2 * diff) // (2^k).
            # Is it guaranteed to be integer?
            # Yes, because 2 * diff is sum of (A_i + A_j) for pairs with nu_2=k.
            # And A_i + A_j is divisible by 2^k.
            # So 2 * diff is divisible by 2^k.
            
            my_formula += (2 * diff) >> k
            
    # Compute Diag = sum_{i=1}^N f(A_i)
    diag = 0
    for x in A:
        # f(x) = x // (x & -x)
        diag += x // (x & -x)
        
    # The sum over i <= j is (sum_{i, j} + sum_{i=j}) / 2
    ans = (my_formula + diag) // 2
    print(ans)

if __name__ == '__main__':
    solve()