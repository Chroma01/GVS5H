import sys

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

    # A is 0-indexed in Python: A[0], A[1], ..., A[N-1]
    # Corresponds to 1-indexed A_1, A_2, ..., A_N
    
    # Precompute D[i] = |A[2*i] - A[2*i+1]| for i from 0 to (N//2) - 1
    # This corresponds to pairs (A_1, A_2), (A_3, A_4), ...
    # Indices in A: (0,1), (2,3), ...
    D = []
    for i in range(0, N - 1, 2):
        D.append(abs(A[i] - A[i+1]))
    
    # Precompute E[i] = |A[2*i+1] - A[2*i+2]| for i from 0 to (N//2) - 1
    # This corresponds to pairs (A_2, A_3), (A_4, A_5), ...
    # Indices in A: (1,2), (3,4), ...
    E = []
    for i in range(1, N - 1, 2):
        E.append(abs(A[i] - A[i+1]))
        
    # Prefix sums for D
    # pref_D[k] = sum(D[0]...D[k-1])
    pref_D = [0] * (len(D) + 1)
    for i in range(len(D)):
        pref_D[i+1] = pref_D[i] + D[i]
        
    # Suffix sums for E
    # suff_E[k] = sum(E[k]...E[end])
    suff_E = [0] * (len(E) + 1)
    for i in range(len(E) - 1, -1, -1):
        suff_E[i] = suff_E[i+1] + E[i]
        
    ans = 0
    
    if N % 2 == 0:
        # Case N is even
        # Strategy 1: (1,2), (3,4), ...
        score1 = pref_D[len(D)]
        
        # Strategy 2: (2,3), (4,5), ... and (1, N)
        # Pairs are E[0], E[1], ..., E[N/2 - 2]
        # Number of E terms is N/2 - 1
        # Indices in E: 0 to N/2 - 2
        # Sum is suff_E[0] - suff_E[N/2 - 1]
        # Wait, suff_E[k] sums from k to end.
        # We want sum from 0 to N/2 - 2.
        # Total E length is N/2. Indices 0 to N/2 - 1.
        # We exclude the last one (index N/2 - 1).
        # So sum is suff_E[0] - suff_E[N/2 - 1]
        
        num_E = len(E)
        # We need sum of E[0]...E[num_E - 2]
        # If num_E == 0 (N=2), this range is empty.
        if num_E > 1:
            score2 = suff_E[0] - suff_E[num_E - 1]
        else:
            score2 = 0
            
        score2 += abs(A[0] - A[N-1])
        
        ans = max(score1, score2)
        
    else:
        # Case N is odd
        # Survivor must be at odd index k (1-based): 1, 3, ..., N
        # In 0-based: 0, 2, ..., N-1
        
        # For a survivor at 0-based index k (which is even):
        # Left part: 0 to k-1. Length k. Pairs (0,1), (2,3)...
        # Number of pairs = k // 2.
        # Sum = pref_D[k // 2]
        
        # Right part: k+1 to N-1. Length N - 1 - k.
        # Pairs start at k+1.
        # The first pair is (k+1, k+2).
        # In E array, index 0 corresponds to (1,2) i.e., (A[1], A[2]).
        # We need pairs starting at index k+1.
        # The index in E corresponding to pair starting at A[i] (where i is odd) is (i-1)//2.
        # Here start index is k+1 (which is even? No, k is even, so k+1 is odd).
        # So the pair is (A[k+1], A[k+2]).
        # The index in E is ( (k+1) - 1 ) // 2 = k // 2.
        # We need sum of E from index k//2 to end.
        # Sum = suff_E[k // 2]
        
        # Let's verify with k=0 (Survivor A[0])
        # Left: 0 pairs. pref_D[0] = 0. Correct.
        # Right: start at 1. Pair (1,2). E index 0.
        # suff_E[0]. Correct.
        
        # Let's verify with k=N-1 (Survivor A[N-1])
        # Left: (N-1)//2 pairs. pref_D[(N-1)//2]. Correct.
        # Right: start at N. No pairs. suff_E[(N-1)//2].
        # Length of E is (N-1)//2. So index (N-1)//2 is out of bounds?
        # E indices: 0 to (N-1)//2 - 1.
        # If k = N-1, k//2 = (N-1)//2.
        # suff_E[(N-1)//2] should be 0.
        # My suff_E array has size len(E)+1.
        # suff_E[len(E)] is 0.
        # So if k//2 == len(E), suff_E returns 0. Correct.
        
        # Iterate over possible survivors (0-based even indices)
        for k in range(0, N, 2):
            left_sum = pref_D[k // 2]
            right_sum = suff_E[k // 2]
            current_score = left_sum + right_sum
            if current_score > ans:
                ans = current_score
                
    print(ans)

if __name__ == '__main__':
    solve()