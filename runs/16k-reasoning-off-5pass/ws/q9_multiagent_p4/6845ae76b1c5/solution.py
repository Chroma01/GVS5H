import sys
from bisect import bisect_right

# Increase recursion depth just in case, though not used here
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        K = int(next(iterator))
        queries = []
        for _ in range(K):
            x = int(next(iterator))
            y = int(next(iterator))
            queries.append((x, y))
    except StopIteration:
        return

    # Sort A and B
    A.sort()
    B.sort()
    
    # Precompute prefix sums for B
    # prefB[i] stores sum of B[0]...B[i-1]
    prefB = [0] * (N + 1)
    for i in range(N):
        prefB[i+1] = prefB[i] + B[i]
        
    # Precompute prefix sums for A
    prefA = [0] * (N + 1)
    for i in range(N):
        prefA[i+1] = prefA[i] + A[i]
        
    # Block size for decomposition
    # sqrt(10^5) is approx 316. We use a slightly larger block to minimize overhead
    BLOCK_SIZE = int(N**0.5) + 1
    
    # Precompute block boundaries for A
    num_blocks = (N + BLOCK_SIZE - 1) // BLOCK_SIZE
    block_starts = []
    block_ends = []
    curr = 0
    for b in range(num_blocks):
        start = curr
        end = min(curr + BLOCK_SIZE, N)
        block_starts.append(start)
        block_ends.append(end)
        curr = end
        
    results = []
    
    for x, y in queries:
        # We need to compute:
        # Sum = sum_{i=0}^{x-1} sum_{j=0}^{y-1} |A[i] - B[j]|
        #
        # For a fixed i, let p = bisect_right(B, A[i], lo=0, hi=y).
        # This p is the count of elements in B[0..y-1] such that B[j] <= A[i].
        # The elements B[0]...B[p-1] are <= A[i].
        # The elements B[p]...B[y-1] are > A[i].
        #
        # Contribution of A[i] to the sum:
        # Sum_{j=0}^{p-1} (A[i] - B[j]) + Sum_{j=p}^{y-1} (B[j] - A[i])
        # = p*A[i] - prefB[p] + (prefB[y] - prefB[p]) - (y-p)*A[i]
        # = (2*p - y)*A[i] + prefB[y] - 2*prefB[p]
        #
        # Total Sum over i=0 to x-1:
        # Sum_{i=0}^{x-1} [ (2*p_i - y)*A[i] + prefB[y] - 2*prefB[p_i] ]
        # = 2 * Sum(p_i * A[i]) - y * Sum(A[i]) + x * prefB[y] - 2 * Sum(prefB[p_i])
        #
        # We need to compute:
        # 1. sum_A = Sum(A[0..x-1]) = prefA[x]
        # 2. sum_pA = Sum(p_i * A[i])
        # 3. sum_prefB_p = Sum(prefB[p_i])
        
        sum_A = prefA[x]
        sum_pA = 0
        sum_prefB_p = 0
        
        # Total sum of B[0..y-1]
        sum_B_y = prefB[y]
        
        # Iterate blocks in A that are fully or partially within [0, x)
        for b in range(num_blocks):
            start_idx = block_starts[b]
            end_idx = block_ends[b]
            
            # Intersection with [0, x)
            real_start = start_idx
            real_end = min(end_idx, x)
            
            if real_start >= real_end:
                continue
                
            # Iterate through the elements in the block
            for i in range(real_start, real_end):
                val = A[i]
                # Find p_i: number of elements in B[0..y-1] <= val
                # bisect_right returns insertion point after all elements <= val
                p = bisect_right(B, val, lo=0, hi=y)
                
                sum_pA += p * val
                sum_prefB_p += prefB[p]
        
        # Final calculation based on derived formula:
        # Total = 2 * sum_pA - y * sum_A + x * sum_B_y - 2 * sum_prefB_p
        ans = 2 * sum_pA - y * sum_A + x * sum_B_y - 2 * sum_prefB_p
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()