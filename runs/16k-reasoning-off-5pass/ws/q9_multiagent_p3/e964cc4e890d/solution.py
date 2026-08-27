import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    S = input_data[1]

    MOD = 998244353

    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    # Check boundary conditions
    # If S starts with 'W', vertex 1 is White. It has no incoming edges from 2 (since 1->2).
    # It can only receive edges from other Whites (impossible) or Blacks (W->B edges).
    # So if S[0] == 'W', vertex 1 is a source with no incoming edges -> Not strongly connected.
    # Similarly, if S[2N-1] == 'B', vertex 2N is Black. It has no outgoing added edges (W->B).
    # It only has incoming from 2N-1. So it's a sink -> Not strongly connected.
    if S[0] == 'W' or S[2*N - 1] == 'B':
        print(0)
        return

    # Identify cut points
    # A cut point k (1 <= k < 2N) is valid if the prefix 1..k has equal number of W and B.
    # Let's count W and B.
    # We need to find indices k where count_W == count_B.
    
    cnt_w = 0
    cnt_b = 0
    cut_points = []
    
    # We iterate 1 to 2N-1
    for i in range(2 * N):
        char = S[i]
        if char == 'W':
            cnt_w += 1
        else:
            cnt_b += 1
        
        if cnt_w == cnt_b:
            # This is a potential cut point. The index is i+1 (1-based)
            # But we only care about k < 2N.
            if i + 1 < 2 * N:
                cut_points.append(i + 1)
    
    # If no cut points, the graph is always strongly connected (given boundary checks passed)
    if not cut_points:
        # Total ways to pair N W and N B is N!
        print(fact[N])
        return

    # We need to compute the size of the union of "bad" sets A_k.
    # A_k is the set of pairings where no edge crosses the cut k.
    # This implies the pairing is internal to [1, k] and [k+1, 2N].
    # Number of ways for a specific cut k is (N_k!)^2, where N_k is the number of W in 1..k.
    # Since N_k = cnt_w at cut point, let's call it w_k.
    # We need |Union A_k|.
    # By PIE: Sum_{U non-empty subset of cuts} (-1)^{|U|-1} * Ways(U)
    # Ways(U) = Product over segments defined by U of (len_seg!)^2.
    
    # Let the cut points be z_1, z_2, ..., z_m.
    # These divide the string into m+1 segments.
    # Let L_1, L_2, ..., L_{m+1} be the number of W (and B) in each segment.
    # L_1 = w_{z_1}
    # L_2 = w_{z_2} - w_{z_1}
    # ...
    # L_{m+1} = N - w_{z_m}
    
    # We want to compute S = Sum_{U subset of {1..m}} (-1)^{|U|} * Ways(U)
    # Then Bad = Ways(empty) - S = (Total N!) - S? 
    # Wait, Ways(empty) corresponds to U = empty set, which is the term with sign +1 in the sum S?
    # No, in PIE for Union: |Union| = Sum_{U != empty} (-1)^{|U|-1} Ways(U)
    # = - Sum_{U != empty} (-1)^{|U|} Ways(U)
    # = - ( Sum_{U subset} (-1)^{|U|} Ways(U) - Ways(empty) )
    # = Ways(empty) - Sum_{U subset} (-1)^{|U|} Ways(U)
    # So we need to compute TotalSum = Sum_{U subset} (-1)^{|U|} Ways(U).
    # Then Bad = Ways(empty) - TotalSum.
    # And Answer = Total_Ways - Bad = N! - (Ways(empty) - TotalSum) = TotalSum.
    # Wait, Total_Ways is N!. Ways(empty) is also N! (since empty set of cuts means no restriction, just one big segment of length N).
    # So Answer = TotalSum.
    
    # Let's verify with Sample 1: N=2, BWBW.
    # Cuts at 2. z_1 = 2.
    # Segments: [1,2] (len 1), [3,4] (len 1). L_1=1, L_2=1.
    # U subsets:
    # {}: Ways = (1+1)!^2 = 4. Sign +.
    # {1}: Ways = 1!^2 * 1!^2 = 1. Sign -.
    # TotalSum = 4 - 1 = 3.
    # Answer = 3? But sample output is 1.
    # Where is the error?
    # Ah, "Ways(empty)" in the context of the sum S is the term where we don't cut anywhere.
    # That corresponds to the graph being connected? No.
    # The term Ways(empty) in the sum S corresponds to the case where we consider the whole range [1, 2N] as one segment.
    # The number of ways to pair [1, 2N] internally is N!.
    # So Ways(empty) = N!.
    # The formula derived: Answer = TotalSum.
    # For Sample 1: TotalSum = 3. Answer should be 1.
    # Why?
    # Let's re-evaluate the PIE logic.
    # We want to count pairings that have NO cut.
    # Total pairings = N!.
    # Bad pairings = Union A_k.
    # |Union A_k| = Sum_{U != empty} (-1)^{|U|-1} Ways(U).
    # Let T = Sum_{U subset} (-1)^{|U|} Ways(U).
    # Then |Union A_k| = - (T - Ways(empty)) = Ways(empty) - T.
    # Answer = Total - |Union| = N! - (N! - T) = T.
    # So the answer IS T.
    # Why did Sample 1 give 3?
    # L_1 = 1, L_2 = 1.
    # Ways({}) = (1+1)!^2 = 4.
    # Ways({1}) = 1!^2 * 1!^2 = 1.
    # T = 4 - 1 = 3.
    # But N! = 2! = 2.
    # Contradiction: Ways(empty) should be N! = 2.
    # Why did I calculate 4?
    # Because I used (L_1 + L_2)!^2 = 2!^2 = 4.
    # But the number of ways to pair N W and N B is N!, not (N!)^2.
    # Ah! The number of ways to pair a segment of length 2k (k W, k B) is k!.
    # My previous assumption was (k!)^2. That was wrong.
    # If we have k W and k B, the number of bijections is k!.
    # So Ways(U) = Product (len_seg!)^2 is WRONG.
    # It should be Product (len_seg!).
    # Let's re-calculate Sample 1 with correct formula.
    # L_1 = 1, L_2 = 1.
    # Ways({}) = (1+1)! = 2.
    # Ways({1}) = 1! * 1! = 1.
    # T = 2 - 1 = 1. Correct!
    
    # So the formula is:
    # Answer = Sum_{U subset} (-1)^{|U|} * Product_{seg in U} (len_seg!)
    
    # Now we need to compute this sum efficiently.
    # Let dp[i] be the sum of signed products for the first i segments.
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * ...?
    # No, the recurrence is:
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)! / ...?
    # Actually, we can just iterate.
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)!? No.
    # Let's use the property:
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)! is not right.
    # Correct recurrence:
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)!
    # Wait, the "merge" term is tricky.
    # Let's define dp[i] as the sum for the first i segments.
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)!
    # This is still dependent on future.
    # However, notice that the term (L_i + ...)! is just the factorial of the sum of lengths.
    # Let's reverse the DP or use a different state.
    # Actually, we can compute this in O(m) by maintaining the current sum.
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)!
    # No, let's look at the structure again.
    # T = Sum_{U} (-1)^{|U|} Prod (len!)
    # This is equivalent to:
    # T = (L_1 + L_2 + ... + L_{m+1})! - Sum_{k} (L_k!) * (Sum of rest)! + ...
    # This is exactly the expansion of the inclusion-exclusion principle for the union of events.
    # But there is a simpler way:
    # T = dp[m+1] where dp[i] is computed as:
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)!
    # Wait, if we process from left to right:
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)!
    # This is not working because of the future dependency.
    # But wait! The "merge" option means we don't cut at the boundary between i and i+1.
    # So the segment length increases.
    # Let's define dp[i] as the sum of signed products for the first i segments, where the last segment is "open" (merged with previous).
    # No, that's not standard.
    # Let's try a different approach.
    # T = Sum_{U} (-1)^{|U|} Prod (len!)
    # This is equal to:
    # T = (L_1 + L_2 + ...)! - Sum_{k} (L_k!) * (Sum_{j != k} L_j)! + ...
    # This is exactly the coefficient of x^N in some generating function?
    # Actually, there is a known result for this specific problem (Codeforces 1150C? No).
    # The answer is simply:
    # Answer = (L_1 + L_2 + ... + L_{m+1})! - Sum_{k=1}^{m} (L_k!) * (L_{k+1} + ... + L_{m+1})! + ...
    # This is exactly what we are computing.
    # And it turns out that T = dp[m+1] where:
    # dp[i] = dp[i-1] * (-1) * (L_i!) + dp[i-1] * (L_i + L_{i+1} + ...)!
    # Wait, if we define dp[i] as the sum for the suffix?
    # Let's compute from right to left.
    # Let S[i] = Sum_{U subset of {i..m}} (-1)^{|U|} Prod (len!)
    # S[m+1] = 1 (empty set, product 1? No, product of lengths of segments in the suffix).
    # If we take empty set from suffix, we merge all remaining segments into one.
    # So S[m+1] = (L_{m+1})! ? No.
    # Let's restart the DP definition.
    # We have segments 1..m+1.
    # We want to choose a subset of boundaries to cut.
    # If we cut at boundary i (between seg i and i+1), we multiply by -1 and split.
    # If we don't cut, we merge.
    # Let dp[i] be the sum of signed products for the suffix of segments i..m+1.
    # dp[i] = (L_i + L_{i+1} + ... + L_{m+1})!  (Case: no cuts in suffix)
    #       + Sum_{k=i}^{m} ( - (L_k!) * dp[k+1] ) ? No.
    # If we cut at the first available boundary after i (which is boundary i, between i and i+1):
    # Then we have term: - (L_i!) * (ways for suffix i+1..m+1).
    # But wait, if we cut at boundary i, the segment i is isolated.
    # The remaining segments are i+1..m+1.
    # So dp[i] = (Sum_{j=i}^{m+1} L_j)! - Sum_{k=i}^{m} (L_k!) * dp[k+1]?
    # No, if we cut at boundary k (between k and k+1), the term is - (L_k!) * (ways for suffix k+1).
    # But we can also cut at multiple boundaries.
    # So:
    # dp[i] = (Sum_{j=i}^{m+1} L_j)! - Sum_{k=i}^{m} (L_k!) * dp[k+1]
    # Base case: dp[m+2] = 0? No.
    # If i = m+1 (last segment), dp[m+1] = (L_{m+1})!.
    # Let's check for 2 segments L1, L2.
    # dp[3] = 0? No, dp[m+1] should be (L_{m+1})!.
    # dp[2] = (L2)! - (L2)! * dp[3]?
    # Let's redefine.
    # dp[i] = Sum_{U subset of boundaries in {i..m}} (-1)^{|U|} Prod (len!)
    # Boundaries are between i and i+1, ..., m and m+1.
    # If U is empty: Prod = (L_i + ... + L_{m+1})!.
    # If U is not empty, let k be the smallest index in U.
    # Then we cut at k. Term is - (L_k!) * (ways for suffix k+1).
    # So dp[i] = (Sum_{j=i}^{m+1} L_j)! - Sum_{k=i}^{m} (L_k!) * dp[k+1].
    # Base case: dp[m+2] = 0?
    # If i = m+1: dp[m+1] = (L_{m+1})! - Sum_{k=m+1}^{m} ... = (L_{m+1})!. Correct.
    # If i = m: dp[m] = (L_m + L_{m+1})! - (L_m!) * dp[m+1] = (L_m+L_{m+1})! - (L_m!) (L_{m+1})!. Correct.
    # So we can compute dp[1] by iterating backwards.
    
    # Compute L array
    L = []
    current_w = 0
    last_w = 0
    for z in cut_points:
        # We need w at z.
        # We can precompute prefix sums of W.
        pass
    
    # Precompute prefix sums of W
    pref_w = [0] * (2 * N + 1)
    for i in range(2 * N):
        pref_w[i+1] = pref_w[i] + (1 if S[i] == 'W' else 0)
        
    # Compute L
    # cut_points are indices k where pref_w[k] == k/2 (since equal W and B)
    # Actually, we just collected cut_points.
    # L_1 = pref_w[cut_points[0]]
    # L_2 = pref_w[cut_points[1]] - pref_w[cut_points[0]]
    # ...
    # L_{m+1} = N - pref_w[cut_points[-1]]
    
    m = len(cut_points)
    L = []
    if m > 0:
        prev = 0
        for z in cut_points:
            w_count = pref_w[z]
            L.append(w_count - prev)
            prev = w_count
        L.append(N - prev)
    
    # Compute dp backwards
    # dp[i] corresponds to suffix starting at segment i (1-based index in L)
    # We need dp[1].
    # dp array size m+3.
    dp = [0] * (m + 3)
    
    # Total length of suffix
    current_suffix_len = 0
    
    # Iterate from last segment to first
    for i in range(m, -1, -1):
        # Segment index i (0-based in L) corresponds to segment i+1 in 1-based
        # We want dp[i+1] in 1-based, which is dp[i] in 0-based logic?
        # Let's use 0-based index for L: 0 to m.
        # dp[i] = sum for suffix starting at L[i].
        # dp[m] = (L[m])!
        # dp[i] = (Sum_{j=i}^{m} L[j])! - Sum_{k=i}^{m-1} (L[k]!) * dp[k+1]
        
        # Update current_suffix_len
        current_suffix_len += L[i]
        term1 = fact[current_suffix_len]
        
        term2 = 0
        for k in range(i, m):
            term2 = (term2 + (fact[L[k]] * dp[k+1])) % MOD
        
        dp[i] = (term1 - term2) % MOD
        
    # The answer is dp[0]
    ans = dp[0]
    print((ans + MOD) % MOD)

solve()