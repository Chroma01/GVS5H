import sys
from collections import Counter

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Separate known and unknown values
    known_A = []
    known_B = []
    
    for i in range(N):
        if A[i] != -1:
            known_A.append(A[i])
        if B[i] != -1:
            known_B.append(B[i])
            
    n_known_A = len(known_A)
    n_known_B = len(known_B)
    
    # Number of positions where B is unknown (Type 2 positions)
    n_B_unknown = N - n_known_B
    
    # Minimum possible S must be at least max of all known B values
    if known_B:
        S_min = max(known_B)
    else:
        S_min = 0
        
    # Candidate S values
    candidates = set()
    candidates.add(S_min)
    
    # Precompute frequency map for known_A
    freq_A = Counter(known_A)
    
    # Precompute sum_counts: number of pairs (a, b) with a in known_A, b in known_B such that a + b = S
    # This is O(N_A * N_B) which is at most O(N^2)
    sum_counts = Counter()
    for a_val in known_A:
        for b_val in known_B:
            s_val = a_val + b_val
            if s_val >= S_min:
                sum_counts[s_val] += 1
            # We only care about S >= S_min, so we can ignore smaller sums for candidate generation
            # But we still add them to candidates if they are >= S_min
            
    # Add A_i + B_j for all known pairs to candidates
    for s_val in sum_counts:
        candidates.add(s_val)
        
    # Minimum number of known A values that MUST be matched to Type 1 positions (where B is known)
    # Because Type 2 positions (B unknown) can only hold at most n_B_unknown known A values.
    # So at least n_known_A - n_B_unknown known A values must go to Type 1 positions.
    k_min = max(0, n_known_A - n_B_unknown)
    
    # If k_min is 0, we don't need to match any known A to Type 1 positions specifically.
    # But we still need to check if the required values for Type 1 positions can be filled by unknowns in A.
    # Actually, the logic is:
    # We have n_known_B Type 1 positions with required values V_req = {S - B_j}.
    # We have n_known_A known A values.
    # We want to match as many known A values to V_req as possible.
    # Let k be the number of matches.
    # The remaining n_known_A - k known A values must go to Type 2 positions.
    # There are n_B_unknown Type 2 positions.
    # So we need n_known_A - k <= n_B_unknown  =>  k >= n_known_A - n_B_unknown.
    # So we need to find if there exists a matching of size at least k_min.
    
    # To check if we can match at least k_min known A values to V_req:
    # We count the maximum number of known A values that are present in V_req (multiset intersection).
    # This is exactly sum_counts[S].
    
    for S in sorted(candidates):
        matches = sum_counts.get(S, 0)
        
        if matches >= k_min:
            print("Yes")
            return
            
    print("No")

solve()