import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    X = [int(next(it)) for _ in range(N)]

    # Compute gaps between consecutive pieces
    gaps = [X[i+1] - X[i] for i in range(N-1)]
    # gaps has N-1 elements, indices 0..N-2
    # gap at index k (0-indexed) is the gap to the right of piece k
    # after operations, gaps at even indices (0,2,4,...) and odd indices (1,3,5,...) can be permuted independently

    even_gaps = []  # gaps at indices 0,2,4,...
    odd_gaps = []   # gaps at indices 1,3,5,...
    for i, g in enumerate(gaps):
        if i % 2 == 0:
            even_gaps.append(g)
        else:
            odd_gaps.append(g)
    even_gaps.sort()
    odd_gaps.sort()

    # Now we need to assign the sorted gaps to positions to minimize weighted sum.
    # Final piece positions: Y_0, Y_1, ..., Y_{N-1}
    # Y_0 = X[0]
    # Y_k = Y_{k-1} + gap_{k-1}  for k >= 1
    # Sum = N*X[0] + (N-1)*gap_0 + (N-2)*gap_1 + ... + 1*gap_{N-2}
    # We want to minimize this by choosing how to assign the even and odd gaps.
    # The weight for gap at position i (i from 0 to N-2) is (N-1-i).
    # Weight is decreasing in i. So we want to assign smaller gaps to larger weights.
    # However, even gaps must be placed at even positions and odd gaps at odd positions.
    # Within even positions (0,2,4,...), the weights are (N-1), (N-3), (N-5), ... which is decreasing.
    # So to minimize, we assign the smallest even gap to the largest weight, i.e., to the smallest even index.
    # That means: for even positions sorted by index ascending (0,2,4,...), assign even_gaps sorted ascending.
    # Wait, check: position 0 has weight N-1 (largest), position 2 has weight N-3, ...
    # So smaller index -> larger weight. So we want smallest gap at smallest index.
    # So we assign even_gaps[0] to position 0, even_gaps[1] to position 2, ...
    # Similarly for odd positions: position 1 has weight N-2, position 3 has weight N-4, ...
    # So smaller index -> larger weight. Assign odd_gaps sorted ascending to positions 1,3,5,...
    
    # Construct the optimal gap sequence
    opt_gaps = [0] * (N-1)
    e_idx = 0
    o_idx = 0
    for i in range(N-1):
        if i % 2 == 0:
            opt_gaps[i] = even_gaps[e_idx]
            e_idx += 1
        else:
            opt_gaps[i] = odd_gaps[o_idx]
            o_idx += 1
    
    # Reconstruct positions and compute sum
    total = 0
    # Instead of building array, compute sum directly
    # Sum = N * X[0] + sum_{i=0}^{N-2} (N-1-i) * opt_gaps[i]
    # But careful: X[0] is fixed? Wait, can we change X[0]? 
    # The operation only affects pieces i+1 and i+2, not pieces i and i+3.
    # So the first and last pieces in any block of 4 are fixed by the block boundaries.
    # More generally, pieces at positions 0 and N-1 might be fixed? Let's check.
    # Actually, any piece can be involved as the "i-th" or "(i+3)-th" piece, but they don't move.
    # The pieces that move are the middle two. So pieces at the very ends (index 0 and index N-1) 
    # can only serve as the fixed endpoints, they never move.
    # Indeed, operation on [i, i+1, i+2, i+3] moves i+1 and i+2 only.
    # So X[0] and X[N-1] are invariant.
    # All other pieces can be moved.
    # So we fix Y_0 = X[0] and Y_{N-1} = X[N-1] is also invariant? 
    # Wait, can X[N-1] move? To move it, it would need to be i+1 or i+2 in some operation.
    # But i+1 <= N-1 means i <= N-2, so i+3 <= N+1, but i+3 must be <= N, so i <= N-3.
    # So i+1 <= N-2, i+2 <= N-1. So the last piece (index N-1) can only be i+3, never i+1 or i+2.
    # So it never moves. Similarly first piece (index 0) can only be i, never i+1 or i+2.
    # So X[0] and X[N-1] are fixed.
    # Therefore the total span X[N-1] - X[0] is fixed, and the sum of gaps is fixed.
    # We are just permuting the gaps.
    # So the sum is N*X[0] + sum_{i=0}^{N-2} (N-1-i) * opt_gaps[i]
    
    # But we need to be careful: when we sum, we need the sum of all pieces.
    # Y_0 = X[0]
    # Y_1 = X[0] + opt_gaps[0]
    # Y_2 = X[0] + opt_gaps[0] + opt_gaps[1]
    # ...
    # Y_k = X[0] + sum_{j=0}^{k-1} opt_gaps[j]
    # Sum_{k=0}^{N-1} Y_k = N*X[0] + sum_{k=1}^{N-1} sum_{j=0}^{k-1} opt_gaps[j]
    #                 = N*X[0] + sum_{j=0}^{N-2} opt_gaps[j] * (N-1-j)
    # This matches the formula above.
    
    total = N * X[0]
    for i in range(N-1):
        total += (N-1-i) * opt_gaps[i]
    
    print(total)

if __name__ == "__main__":
    solve()