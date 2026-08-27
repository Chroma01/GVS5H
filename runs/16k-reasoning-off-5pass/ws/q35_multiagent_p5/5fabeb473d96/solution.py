import sys

# Increase recursion depth just in case, though we try to avoid deep recursion
sys.setrecursionlimit(300000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    # A is 1-indexed in problem, but we'll store 0-indexed or adjust
    # A_2, ..., A_N
    # Let's store A[i] for i in 2..N
    # We can use an array of size N+1
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(next(iterator))

    queries = []
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        if u > v:
            u, v = v, u
        queries.append((u, v))

    MOD = 998244353

    # Precompute factorials and inverse factorials for combinations if needed
    # But we mainly need factorials for (N-1)! and divisions by i, i-1, etc.
    # We can precompute factorials and modular inverses for 1..N
    
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    finv = [1] * (N + 1)
    
    for i in range(2, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, 1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    # finv[i] = 1/i!
    finv[N] = inv[N] # This is actually 1/N!
    # Wait, inv[i] computed above is 1/i! ? No.
    # inv[N] = 1/N!
    # inv[i] = inv[i+1] * (i+1) => 1/i! = 1/(i+1)! * (i+1). Correct.
    # So inv[i] is 1/i!
    
    # We need 1/i, 1/(i-1), etc.
    # 1/i = i! / (i-1)! * 1/i ? No.
    # 1/i = inv[i] * fact[i-1] % MOD
    
    # Let's precompute modular inverse for each number 1..N
    mod_inv = [1] * (N + 1)
    for i in range(2, N + 1):
        mod_inv[i] = pow(i, MOD - 2, MOD)

    total_trees = fact[N-1] # (N-1)!
    
    # For each query (u, v) with u < v:
    # Sum over i=2 to N of A[i] * Count(i, u, v)
    # Count(i, u, v) = Number of trees where edge i is on path u-v.
    # Edge i is on path iff exactly one of u, v is in subtree of i.
    # P(u in T_i) = 1/i if i < u, else 0 if i > u (since u < i, u cannot be in T_i unless u=i? No, u < i means u is not in T_i because T_i contains i and descendants > i).
    # Wait, if i < u, u CAN be in T_i. If i > u, u CANNOT be in T_i (since u < i, u is not a descendant of i).
    # If i == u, u is in T_i (root of subtree).
    
    # Case 1: i < u < v
    # P(u in T_i) = 1/i
    # P(v in T_i) = 1/i
    # P(both in T_i) = P(i anc u and i anc v)
    # Known result: P(i anc u and i anc v) = 1 / (i * (i-1)) ? 
    # Let's re-verify with N=4, i=2, u=3, v=4. Prob = 1/3.
    # 1/(2*1) = 1/2. No.
    # 1/(2*2) = 1/4. No.
    # 1/3 = 1 / (i * (i+1)/2)? No.
    
    # Correct formula from literature for Random Recursive Trees:
    # P(i is ancestor of j) = 1/i.
    # P(i is ancestor of j and i is ancestor of k) for i < j < k:
    # = 1 / (i * (i-1)) ? No.
    # It is 1 / (i * (i-1)) is for specific structures?
    
    # Let's use the property:
    # P(i anc u and i anc v) = P(i anc u) * P(i anc v | i anc u)
    # Given i is anc of u, the subtree T_i contains u.
    # The probability that v is in T_i given i is anc of u is:
    # It is known that this probability is 1/i ? No.
    
    # Actually, there is a simpler way.
    # The number of trees where i is an ancestor of j is (N-1)! / i.
    # The number of trees where i is an ancestor of both u and v (i < u < v) is (N-1)! / (i * (i-1)) ?
    # Let's check N=4, i=2, u=3, v=4. Count = 2. Total = 6.
    # 6 / (2*1) = 3. No.
    # 6 / (2*2) = 1.5. No.
    # 6 / 3 = 2. So divisor is 3.
    # 3 = i * (i+1)/2 ? 2*3/2 = 3. Yes.
    # So P(both) = 1 / (i * (i+1)/2) ?
    # Let's check i=1. P(1 anc u and 1 anc v) = 1.
    # 1 / (1*2/2) = 1. Yes.
    # Let's check i=2, u=3, v=5 in N=5.
    # Total trees = 24.
    # P(2 anc 3) = 1/2. Count = 12.
    # P(2 anc 5) = 1/2. Count = 12.
    # P(2 anc 3 and 2 anc 5)?
    # If 2 is anc of 3, 3 is in T_2.
    # If 2 is anc of 5, 5 is in T_2.
    # Count = 24 / (2*3/2) = 24/3 = 8.
    # Let's verify manually for N=5, i=2, u=3, v=5.
    # This is getting complex.
    
    # Alternative: Use the formula for the number of trees where edge i separates u and v.
    # If i < u < v:
    # Count = 2 * (N-1)! / i - 2 * (N-1)! / (i * (i-1)) ? No.
    
    # Let's use the following derived formula which is standard for this problem:
    # For i < u < v:
    # P(edge i on path) = 2/i - 2/(i*(i-1)) ?
    # For i=2, u=3, v=4: 2/2 - 2/2 = 0. No, prob is 1/3.
    
    # Correct Formula:
    # P(edge i on path) = P(u in T_i) + P(v in T_i) - 2 * P(both in T_i)
    # P(u in T_i) = 1/i
    # P(v in T_i) = 1/i
    # P(both in T_i) = 1 / (i * (i-1)) ? No.
    
    # Let's look at the counts again.
    # N=4, i=2, u=3, v=4.
    # P(both) = 1/3.
    # P(u in) = 1/2. P(v in) = 1/2.
    # P(exactly one) = 1/2 + 1/2 - 2*(1/3) = 1 - 2/3 = 1/3.
    # So P(edge on path) = 1/3.
    # Formula for P(both) = 1/3 = 1 / (i * (i+1)/2) ?
    # i=2, i*(i+1)/2 = 3. Yes.
    # i=1, i*(i+1)/2 = 1. P(both) = 1. Yes.
    
    # So P(both in T_i) = 2 / (i * (i+1)) ?
    # i=2: 2/6 = 1/3. Yes.
    # i=1: 2/2 = 1. Yes.
    
    # So for i < u < v:
    # P(edge on path) = 2/i - 2 * (2 / (i * (i+1))) = 2/i - 4/(i(i+1))
    # = (2(i+1) - 4) / (i(i+1)) = (2i - 2) / (i(i+1)) = 2(i-1) / (i(i+1))
    
    # Let's check i=2: 2(1) / (2*3) = 2/6 = 1/3. Correct.
    # Let's check i=1: 2(0) / ... = 0. But P(edge 1 on path) for u=2, v=3?
    # Edge 1 is (1, P_1)? No, edge i is (i, P_i).
    # For i=1, there is no edge 1. i starts from 2.
    
    # Case 2: u < i < v
    # u is not in T_i (since u < i).
    # v is in T_i iff i is ancestor of v.
    # P(v in T_i) = 1/i.
    # P(u in T_i) = 0.
    # P(both in T_i) = 0.
    # P(exactly one) = 1/i.
    
    # Case 3: u < v < i
    # Neither u nor v is in T_i.
    # P(exactly one) = 0.

    # So:
    # If i < u < v: Prob = 2(i-1) / (i(i+1))
    # If u < i < v: Prob = 1/i
    # If u < v < i: Prob = 0
    # If i == u: 
    # u is in T_u. v is in T_u iff u is ancestor of v.
    # P(v in T_u) = 1/u.
    # P(u in T_u) = 1.
    # P(both in T_u) = P(v in T_u) = 1/u.
    # P(exactly one) = 1 + 1/u - 2/u = 1 - 1/u = (u-1)/u.
    
    # If i == v:
    # v is in T_v. u is in T_v iff v is ancestor of u? No, u < v, so u cannot be in T_v.
    # P(u in T_v) = 0.
    # P(v in T_v) = 1.
    # P(both in T_v) = 0.
    # P(exactly one) = 1.
    
    # Summary:
    # i < u < v: 2(i-1) / (i(i+1))
    # i == u: (u-1)/u
    # u < i < v: 1/i
    # i == v: 1
    # i > v: 0

    # We need to compute Sum_{i=2}^N A[i] * Prob(i, u, v) * (N-1)!
    # Let's precompute the coefficients for each i.
    # But Q is large, so we need to answer queries fast.
    # The answer is sum of A[i] * C[i] where C[i] depends on u, v.
    # C[i] is non-zero only for i <= v.
    # We can use a Fenwick tree or Segment Tree?
    # The coefficients are:
    # For i < u: 2(i-1)/(i(i+1))
    # For i == u: (u-1)/u
    # For u < i < v: 1/i
    # For i == v: 1
    # For i > v: 0
    
    # Let's define:
    # Term1 = Sum_{i=2}^{u-1} A[i] * 2(i-1)/(i(i+1))
    # Term2 = A[u] * (u-1)/u
    # Term3 = Sum_{i=u+1}^{v-1} A[i] * 1/i
    # Term4 = A[v] * 1
    # Total = (Term1 + Term2 + Term3 + Term4) * (N-1)!
    
    # We can precompute prefix sums for:
    # 1. A[i] * 2(i-1)/(i(i+1))
    # 2. A[i] * 1/i
    
    # Precompute:
    # P1[i] = Sum_{k=2}^i A[k] * 2(k-1)/(k(k+1))
    # P2[i] = Sum_{k=2}^i A[k] * 1/k
    
    # Then:
    # Term1 = P1[u-1]
    # Term2 = A[u] * (u-1)/u
    # Term3 = P2[v-1] - P2[u]
    # Term4 = A[v]
    
    # Note: P1 and P2 are modulo MOD.
    
    # Precompute modular inverses for 1..N
    # We already have mod_inv
    
    # Precompute P1 and P2
    P1 = [0] * (N + 1)
    P2 = [0] * (N + 1)
    
    curr1 = 0
    curr2 = 0
    
    for i in range(2, N + 1):
        # Term for P1: A[i] * 2(i-1) / (i(i+1))
        # = A[i] * 2 * (i-1) * inv[i] * inv[i+1]
        term1 = (A[i] * 2) % MOD
        term1 = (term1 * mod_inv[i]) % MOD
        term1 = (term1 * mod_inv[i+1]) % MOD
        term1 = (term1 * (i - 1)) % MOD
        
        curr1 = (curr1 + term1) % MOD
        P1[i] = curr1
        
        # Term for P2: A[i] * 1/i
        term2 = (A[i] * mod_inv[i]) % MOD
        curr2 = (curr2 + term2) % MOD
        P2[i] = curr2

    # Process queries
    results = []
    for u, v in queries:
        # Term1: sum i=2 to u-1
        t1 = P1[u-1]
        
        # Term2: i=u
        t2 = (A[u] * mod_inv[u]) % MOD
        t2 = (t2 * (u - 1)) % MOD
        
        # Term3: sum i=u+1 to v-1
        t3 = (P2[v-1] - P2[u]) % MOD
        
        # Term4: i=v
        t4 = A[v]
        
        total = (t1 + t2) % MOD
        total = (total + t3) % MOD
        total = (total + t4) % MOD
        
        ans = (total * total_trees) % MOD
        results.append(str(ans))
        
    print('\n'.join(results))

solve()