import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:1+N]))
    
    # Maximum possible sum is 2 * 10^7
    MAX_SUM = 20000000
    
    # Precompute f(x) for all x from 1 to MAX_SUM
    # f(x) is the odd part of x, i.e., x divided by the highest power of 2 dividing x.
    # We can compute this using a sieve-like method.
    # f(x) = x >> (number of trailing zeros)
    # Alternatively, f(x) = f(x // 2) if x is even, else x.
    # We can use dynamic programming:
    # f[1] = 1
    # for i from 2 to MAX_SUM:
    #   if i is even: f[i] = f[i // 2]
    #   else: f[i] = i
    
    f = [0] * (MAX_SUM + 1)
    f[1] = 1
    for i in range(2, MAX_SUM + 1):
        if i % 2 == 0:
            f[i] = f[i // 2]
        else:
            f[i] = i
    
    # Count frequencies of each value in A
    from collections import Counter
    cnt = Counter(A)
    
    # Get distinct values sorted
    distinct_vals = sorted(cnt.keys())
    D = len(distinct_vals)
    
    total_sum = 0
    
    # Iterate over all pairs of distinct values (u, v) with u <= v
    for i in range(D):
        u = distinct_vals[i]
        count_u = cnt[u]
        
        # Pair with itself: (i, j) where A_i = A_j = u, i <= j
        # Number of such pairs: count_u * (count_u + 1) // 2
        sum_self = u + u
        if sum_self <= MAX_SUM:
            total_sum += f[sum_self] * (count_u * (count_u + 1) // 2)
        
        # Pairs with other values v > u
        for j in range(i + 1, D):
            v = distinct_vals[j]
            count_v = cnt[v]
            sum_uv = u + v
            if sum_uv <= MAX_SUM:
                total_sum += f[sum_uv] * count_u * count_v
            else:
                # Since distinct_vals is sorted, all subsequent v will also give sum > MAX_SUM
                break
    
    print(total_sum)

solve()