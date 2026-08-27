import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Edge case: if M=1, there are no inversions possible (all elements 0)
    if M == 1:
        print(0)
        return

    # Group indices by value for efficient retrieval
    # pos[v] contains a list of indices i such that A[i] == v
    pos = [[] for _ in range(M)]
    for i in range(N):
        pos[A[i]].append(i)

    # Fenwick Tree (Binary Indexed Tree) implementation
    # 1-based indexing for BIT
    bit = [0] * (N + 1)

    def update(idx, delta):
        while idx <= N:
            bit[idx] += delta
            idx += idx & (-idx)

    def query(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s

    # Calculate initial inversion count for k=0
    # Inversion count is sum of (number of elements to the left that are greater)
    # We iterate j from 0 to N-1. Count i < j such that A[i] > A[j].
    # This is (number of elements processed so far) - (number of elements <= A[j] processed so far).
    
    initial_inversions = 0
    current_idx = 0
    
    # Clear BIT
    for i in range(N + 1):
        bit[i] = 0

    for x in A:
        # query(x) gives count of numbers <= x seen so far
        # current_idx is count of numbers seen so far
        greater = current_idx - query(x)
        initial_inversions += greater
        update(x + 1, 1) # BIT is 1-based, values are 0..M-1
        current_idx += 1

    # Prepare for the loop
    # We need to track the set of indices that have value M-1 in the current sequence B^(k).
    # B^(k)[i] = (A[i] + k) % M.
    # B^(k)[i] == M-1  <==>  (A[i] + k) % M == M-1  <==>  A[i] == (M - 1 - k) % M.
    
    # The BIT we maintain will store 1 at index i if B^(k)[i] != M-1.
    # Initially (k=0), B^(0)[i] = A[i]. So we mark 1 if A[i] != M-1.
    
    # Reset BIT to reflect k=0 state (1 if A[i] != M-1)
    for i in range(N + 1):
        bit[i] = 0
        
    # Mark positions where A[i] != M-1
    for i in range(N):
        if A[i] != M - 1:
            update(i + 1, 1)
            
    # We will store answers for k=0 to M-1
    results = []
    results.append(initial_inversions)
    
    # We need to efficiently find indices where A[i] == target_value.
    # We have 'pos' array for this.
    
    # Loop k from 0 to M-2 to compute answers for k+1
    # In each iteration k:
    # 1. Identify indices i where B^(k)[i] == M-1. These are i where A[i] == (M - 1 - k) % M.
    # 2. For each such i:
    #    - It contributes to inversions with elements to its left (j < i) that are NOT M-1.
    #      (Because B^(k)[j] < M-1 and B^(k)[i] = M-1 => j < i is NOT an inversion. 
    #       Wait, definition: i < j is inversion if B[i] > B[j].
    #       Here we look at pairs involving i where B[i] = M-1.
    #       Case 1: j < i. Pair (j, i). Inversion if B[j] > B[i]. Since B[i]=M-1, B[j] > M-1 is impossible.
    #       So no inversions with j < i when B[i] = M-1.
    #       Case 2: j > i. Pair (i, j). Inversion if B[i] > B[j]. Since B[i]=M-1, this is true if B[j] < M-1.
    #       So for each i with B[i]=M-1, we lose inversions with all j > i where B[j] != M-1.
    #    - When moving to k+1, B[i] becomes 0.
    #       Case 1: j < i. Pair (j, i). New B[j] = B[j]+1 (if not wrap), New B[i] = 0.
    #       Inversion if New B[j] > New B[i] => B[j]+1 > 0. Since B[j] >= 0, this is always true (unless B[j] was M-1, but we only consider non-M-1).
    #       Wait, if B[j] was M-1, it would have been processed in a previous step or is being processed now?
    #       Only one value wraps per step. So B[j] != M-1.
    #       So for each j < i with B[j] != M-1, we GAIN an inversion.
    #       Case 2: j > i. Pair (i, j). New B[i] = 0, New B[j] = B[j]+1.
    #       Inversion if 0 > B[j]+1. Impossible.
    #       So we LOSE inversions with all j > i where B[j] != M-1.
    #
    # Summary for each i where B[i] == M-1:
    #   Gain: count of j < i where B[j] != M-1.
    #   Loss: count of j > i where B[j] != M-1.
    #   Delta = Gain - Loss.
    #   Note: Loss = (Total non-M-1) - (Gain + count of i itself if it was non-M-1? No, i is M-1).
    #   Actually, Loss = (Total non-M-1 in array) - (Gain).
    #   So Delta = Gain - (Total - Gain) = 2*Gain - Total.
    
    # 3. Update the BIT.
    #    The BIT currently has 1s where B[k][i] != M-1.
    #    After shift, B[k+1][i] = (B[k][i] + 1) % M.
    #    We need BIT to have 1s where B[k+1][i] != M-1.
    #    B[k+1][i] == M-1 <==> B[k][i] == M-2.
    #    So we need to set BIT[i] = 0 for all i where B[k][i] == M-2.
    #    These are i where A[i] == (M - 2 - k) % M.
    
    current_total_non_M_minus_1 = N - len(pos[M-1])
    
    # Pre-calculate counts for each value to avoid repeated lookups?
    # We have pos array.
    
    for k in range(M - 1):
        # Identify target value for wrapping in current step k
        # We need indices i where B[k][i] == M-1
        # B[k][i] = (A[i] + k) % M
        # (A[i] + k) % M == M-1 => A[i] == (M - 1 - k) % M
        
        target_val = (M - 1 - k) % M
        indices_to_wrap = pos[target_val]
        
        # Calculate delta
        delta = 0
        for i in indices_to_wrap:
            # i is 0-based index in A
            # BIT is 1-based.
            # Gain: query(i) -> count of non-M-1 in 0..i-1 (indices 1..i in BIT)
            # Wait, query(i) in BIT (1-based) sums indices 1..i.
            # Index i in A corresponds to i+1 in BIT.
            # So count in 0..i-1 is query(i).
            gain = query(i)
            
            # Loss: total_non - gain
            # Because i itself is M-1 (so 0 in BIT), it is not counted in gain.
            # The set of non-M-1 elements is partitioned into {j < i} and {j > i}.
            # query(i) gives {j < i}.
            # total - query(i) gives {j > i}.
            loss = current_total_non_M_minus_1 - gain
            
            delta += (gain - loss)
        
        initial_inversions += delta
        results.append(initial_inversions)
        
        # Update BIT for next step
        # We need to zero out indices where B[k][i] == M-2
        # B[k][i] == M-2 => (A[i] + k) % M == M-2 => A[i] == (M - 2 - k) % M
        
        next_target_val = (M - 2 - k) % M
        indices_to_zero = pos[next_target_val]
        
        for i in indices_to_zero:
            # Set BIT[i+1] to 0
            # update(i+1, -1)
            update(i + 1, -1)
            
        # Update total count
        current_total_non_M_minus_1 -= len(indices_to_zero)

    # Print results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()