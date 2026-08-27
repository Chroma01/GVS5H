import sys

# Set recursion depth just in case, though we don't use recursion
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    # A is given for indices 2 to N
    # We'll store A in a 1-indexed array for convenience, so A[i] corresponds to edge weight at node i
    # A[1] is unused/0
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(next(iterator))

    # Precompute prefix sums of A to answer range sum queries in O(1)
    # Prefix[i] = A[2] + A[3] + ... + A[i]
    # We can define prefix[1] = 0
    prefix = [0] * (N + 1)
    current_sum = 0
    for i in range(2, N + 1):
        current_sum = (current_sum + A[i]) % 998244353
        prefix[i] = current_sum
    
    # Function to get sum of A[L...R] inclusive
    # Sum = prefix[R] - prefix[L-1]
    def get_range_sum(L, R):
        if L > R:
            return 0
        if L < 2:
            L = 2
        if L > R:
            return 0
        res = (prefix[R] - prefix[L-1]) % 998244353
        return res

    # Precompute (N-2)! modulo 998244353
    MOD = 998244353
    if N >= 2:
        fact_n_minus_2 = 1
        for i in range(1, N - 1):
            fact_n_minus_2 = (fact_n_minus_2 * i) % MOD
    else:
        fact_n_minus_2 = 0 # Should not happen given constraints N >= 2

    results = []
    
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        
        L = min(u, v)
        R = max(u, v)
        
        # The formula derived is:
        # Ans = (N-2)! * ( 2 * A[R] + sum(A[L...R-1]) )
        # Note: The sum is over edge indices i such that L <= i < R.
        # Edge indices are 2..N.
        
        # Calculate sum of A[i] for i in [L, R-1]
        # We need to intersect [L, R-1] with [2, N]
        sum_range_L = L
        sum_range_R = R - 1
        
        range_sum = get_range_sum(sum_range_L, sum_range_R)
        
        term = (2 * A[R] + range_sum) % MOD
        ans = (fact_n_minus_2 * term) % MOD
        
        results.append(str(ans))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()