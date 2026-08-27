import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
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

    # Frequency map for distinct values in A
    # Using a dictionary to handle potentially large values with sparse counts
    freq_map = {}
    for x in A:
        freq_map[x] = freq_map.get(x, 0) + 1
    
    distinct_values = list(freq_map.keys())
    distinct_counts = [freq_map[v] for v in distinct_values]
    
    # Precompute f(x) for all x in A to handle the diagonal term later
    # f(x) is the odd part of x (x divided by 2 until it becomes odd)
    # We can compute this on the fly or precompute. Since we need sum_f_A, let's do it.
    # Optimization: f(2*x) == f(x). So sum_{i} f(2*A_i) == sum_{i} f(A_i).
    
    def get_f(x):
        # While x is even, divide by 2
        # This is equivalent to x >> (x & -x).bit_length() - 1 if x > 0
        # But simple loop is fast enough for 10^7
        while (x & 1) == 0:
            x >>= 1
        return x
    
    # Calculate sum of f(A_i) for the diagonal correction
    sum_f_A = 0
    for x in A:
        sum_f_A += get_f(x)
    
    # We need to calculate S_ordered = sum_{i, j} f(A_i + A_j)
    # Using the derived formula based on 2-adic valuation:
    # S_ordered = N_0 + sum_{k=1}^{max_k} 2^{k-1} * N_k
    # where N_k is the number of ordered pairs (i, j) such that (A_i + A_j) % 2^k == 0
    
    # Max sum is 2 * 10^7. 2^24 = 16,777,216. 2^25 = 33,554,432.
    # So we need to check up to k=24 or 25. Let's go up to 25 to be safe.
    max_k = 25 
    
    ans_ordered = 0
    
    # Pre-calculate powers of 2
    powers_of_2 = [1 << k for k in range(max_k + 1)]
    
    # Iterate k from 0 to max_k
    for k in range(max_k + 1):
        mod = powers_of_2[k]
        
        # Build frequency map for current modulus
        # We use a dictionary for sparse lookups.
        # Complexity per k: O(D) where D is number of distinct values.
        # Total Complexity: O(D * max_k) approx 2*10^5 * 25 = 5*10^6 operations.
        
        mod_counts = {}
        for val, count in zip(distinct_values, distinct_counts):
            rem = val % mod
            if rem in mod_counts:
                mod_counts[rem] += count
            else:
                mod_counts[rem] = count
        
        # Calculate N_k
        # N_k = sum_{r in mod_counts} mod_counts[r] * mod_counts[(mod - r) % mod]
        # This counts ordered pairs (i, j).
        
        n_k = 0
        for r, count_r in mod_counts.items():
            target = (mod - r) % mod
            count_target = mod_counts.get(target, 0)
            n_k += count_r * count_target
        
        # Add to total answer according to the formula
        if k == 0:
            ans_ordered += n_k
        else:
            ans_ordered += (1 << (k - 1)) * n_k
            
    # The problem asks for sum_{i=1}^N sum_{j=i}^N f(A_i + A_j)
    # This is the sum over unordered pairs (with replacement).
    # Relation to ordered sum:
    # S_target = (S_ordered + sum_{i} f(2*A_i)) / 2
    # Since f(2*x) == f(x), sum_{i} f(2*A_i) == sum_{i} f(A_i)
    
    total_ans = (ans_ordered + sum_f_A) // 2
    
    print(total_ans)

if __name__ == '__main__':
    solve()