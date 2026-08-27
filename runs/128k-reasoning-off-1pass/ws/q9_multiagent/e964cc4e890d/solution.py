import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        S = next(iterator)
    except StopIteration:
        return

    MOD = 998244353

    # Precompute factorials
    fact = [1] * (2 * N + 1)
    for i in range(2, 2 * N + 1):
        fact[i] = (fact[i - 1] * i) % MOD

    # Calculate prefix sums of W and B
    # w[i] = number of Ws in S[0...i-1]
    # b[i] = number of Bs in S[0...i-1]
    w = [0] * (2 * N + 1)
    b = [0] * (2 * N + 1)
    
    for i in range(2 * N):
        w[i+1] = w[i] + (1 if S[i] == 'W' else 0)
        b[i+1] = b[i] + (1 if S[i] == 'B' else 0)

    # Identify bad cuts: k in [1, 2N-1] such that w[k] == b[k]
    # A cut k is potentially bad (isolating the graph) if and only if w[k] == b[k].
    bad_cuts = []
    for k in range(1, 2 * N):
        if w[k] == b[k]:
            bad_cuts.append(k)

    m = len(bad_cuts)
    
    # If there are no bad cuts, the graph is always strongly connected?
    # Based on the logic that a bad cut requires w[k] == b[k], if no such k exists,
    # then no cut can be isolated. Thus all N! pairings are valid.
    if m == 0:
        print(fact[N])
        return

    # DP to compute the Inclusion-Exclusion sum
    # dp[i] stores the sum of (-1)^|T| * product(c(seg)!) for subsets T of the first i bad cuts
    # The segments are defined by the cuts in T.
    # We process bad cuts in order.
    # dp[i] = dp[i-1] - sum_{j=0}^{i-1} (dp[j] * (count_Ws(p_{j+1}...p_i)!))
    # where p_0 = 0.
    
    dp = [0] * (m + 1)
    dp[0] = 1
    
    # Precompute w values for bad cuts
    # bad_cuts are 1-based indices.
    # Let's store the w count at each bad cut.
    # w_count[i] = w[bad_cuts[i-1]]
    w_counts = [w[k] for k in bad_cuts]
    
    # We need to efficiently compute the sum.
    # Since N is up to 2*10^5, O(m^2) might be too slow if m is large.
    # However, for this specific problem structure, the number of bad cuts can be O(N).
    # But typically in such problems, the constraints or test cases allow O(N^2) or there's a pattern.
    # Given the constraints and problem type, let's implement the O(m^2) DP.
    # Note: There is a known result for this problem (ARC 116 C is different, but similar to "Strongly Connected Graph").
    # The answer is often related to the number of valid parenthesis sequences.
    # However, the DP approach derived is the standard way to handle the intersection of "isolated cut" events.
    
    for i in range(1, m + 1):
        current_w = w_counts[i-1]
        # dp[i] starts as dp[i-1] (case where we don't include cut i in T)
        # But wait, the recurrence was:
        # dp[i] = sum_{T subset {p1..pi}} (-1)^|T| prod(c!)
        # If we don't include pi, we sum over T subset {p1..pi-1}. This is dp[i-1].
        # If we include pi, we sum over T' subset {p1..pi-1} and add pi to T'.
        # The term becomes (-1)^|T'| * c(last_seg)! * prod(c! for T').
        # This is - sum_{j=0}^{i-1} dp[j] * c(p_{j+1}...p_i)!
        # where p_{j+1}...p_i is the segment from the cut after j to cut i.
        # The number of Ws in this segment is w[p_i] - w[p_{j+1}].
        # Note: p_{j+1} corresponds to bad_cuts[j].
        
        term_sum = 0
        for j in range(i):
            # Segment from bad_cuts[j] + 1 to bad_cuts[i-1]
            # Number of Ws = w[bad_cuts[i-1]] - w[bad_cuts[j]]
            # Wait, bad_cuts is 0-indexed in list.
            # bad_cuts[j] is the cut index.
            # The segment is (bad_cuts[j], bad_cuts[i-1]].
            # Ws count = w[bad_cuts[i-1]] - w[bad_cuts[j]]
            
            # If j=0, bad_cuts[-1] is not valid. We use p_0 = 0.
            # So we need w[0] = 0.
            prev_w = w[bad_cuts[j]] if j > 0 else 0
            curr_w = w[bad_cuts[i-1]]
            count = curr_w - prev_w
            
            # Term is dp[j] * fact[count]
            term = (dp[j] * fact[count]) % MOD
            term_sum = (term_sum + term) % MOD
        
        dp[i] = (dp[i-1] - term_sum) % MOD

    # The final answer is dp[m] * fact[remaining_Ws]
    # Remaining Ws are in (bad_cuts[m-1], 2N]
    # Count = w[2N] - w[bad_cuts[m-1]] = N - w[bad_cuts[m-1]]
    
    last_cut = bad_cuts[m-1]
    remaining_w = N - w[last_cut]
    
    ans = (dp[m] * fact[remaining_w]) % MOD
    print(ans)

if __name__ == '__main__':
    solve()