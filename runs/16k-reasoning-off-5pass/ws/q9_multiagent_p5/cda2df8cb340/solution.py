import sys

# Increase recursion depth just in case, though not used here
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

    # Precompute f(x) for single elements to handle the i=j case later
    # f(x) is the odd part of x (x divided by the highest power of 2 dividing it)
    def get_odd_part(x):
        while (x & 1) == 0:
            x >>= 1
        return x

    sum_f_single = 0
    for x in A:
        sum_f_single += get_odd_part(x)

    # Total sum of A_i
    sum_A = sum(A)
    
    # The formula derived:
    # Sum_{i,j} f(A_i + A_j) = Sum_{i,j} (A_i + A_j) - Sum_{k=1 to K} (1/2^k) * Sum_{i,j: 2^k | (A_i+A_j)} (A_i + A_j)
    # Note: Sum_{i,j} (A_i + A_j) = N * sum_A + N * sum_A = 2 * N * sum_A
    
    # We will compute the ordered sum first.
    # Let TotalOrdered = 2 * N * sum_A
    # Then we subtract contributions for each k >= 1.
    
    # Max possible sum is 2 * 10^7. We need to check k such that 2^k <= 2 * 10^7.
    # 2^24 = 16,777,216. 2^25 = 33,554,432. So k goes up to 24.
    
    max_val = 2 * 10**7
    K = 25 # Sufficiently large
    
    current_total_ordered = 2 * N * sum_A
    
    # We need to compute S_k = Sum_{i,j: 2^k | (A_i+A_j)} (A_i + A_j)
    # We group A by residue modulo 2^k.
    # For a fixed k, let M = 2^k.
    # We need counts and sums for each residue r in [0, M-1].
    
    for k in range(1, K + 1):
        M = 1 << k
        if M > 2 * max(A):
            # If 2^k is larger than the maximum possible sum, no pair can be divisible by 2^k
            # except if sum is 0, but A_i >= 1.
            break
            
        # Group by residue
        # Using a dictionary: residue -> [count, sum_of_values]
        groups = {}
        
        for x in A:
            r = x % M
            if r not in groups:
                groups[r] = [0, 0]
            groups[r][0] += 1
            groups[r][1] += x
            
        # Calculate S_k
        # We iterate over residues r present in groups.
        # We need to pair with residue target = (M - r) % M.
        # To avoid double counting or missing, we can iterate all r and add contribution.
        # Since we iterate all 'r', we will encounter both (r, t) and (t, r).
        # This correctly sums over ordered pairs.
        
        S_k = 0
        
        for r, (cnt_r, sum_r) in groups.items():
            t = (M - r) % M
            if t in groups:
                cnt_t, sum_t = groups[t]
                
                # Contribution from pairs where A_i % M == r and A_j % M == t
                # Sum of (A_i + A_j) for these pairs:
                # Sum = sum_{i in r} sum_{j in t} (A_i + A_j)
                #     = cnt_r * sum_t + cnt_t * sum_r + cnt_r * cnt_t * (r + t)
                # Note: r + t is a multiple of M. Specifically, if r != 0, r+t = M. If r=0, t=0, r+t=0.
                
                term_val = (r + t)
                
                contribution = cnt_r * sum_t + cnt_t * sum_r + cnt_r * cnt_t * term_val
                S_k += contribution
        
        # Subtract S_k / 2^k from total
        # Since we are working with integers, and the math guarantees divisibility:
        # The term being subtracted is exactly S_k // M
        current_total_ordered -= S_k // M

    # Now we have Sum_{i,j} f(A_i + A_j) for ordered pairs (i, j) where 1 <= i, j <= N.
    # We need Sum_{i=1}^N Sum_{j=i}^N f(A_i + A_j).
    # Let S_ordered = current_total_ordered.
    # The sum for i <= j is (S_ordered + Sum_{i=1}^N f(A_i + A_i)) / 2.
    # Because S_ordered = Sum_{i<j} + Sum_{j<i} + Sum_{i=j}
    # And Sum_{i<j} = Sum_{j<i} due to symmetry of f(A_i+A_j).
    # So S_ordered = 2 * Sum_{i<j} + Sum_{i=j}
    # We want Sum_{i<=j} = Sum_{i<j} + Sum_{i=j} = (S_ordered - Sum_{i=j})/2 + Sum_{i=j} = (S_ordered + Sum_{i=j})/2.
    
    ans = (current_total_ordered + sum_f_single) // 2
    print(ans)

if __name__ == '__main__':
    solve()