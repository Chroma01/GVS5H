import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:N+1]))
    
    # dp[i] represents the maximum score obtainable from the prefix A[0..i-1]
    # We use 0-based indexing for A, so A[i] corresponds to the (i+1)-th element.
    # dp[i] = max score for first i elements (A[0] to A[i-1])
    
    # Base cases
    # dp[0] = 0 (no elements)
    # dp[1] = 0 (one element, can't form any pair)
    
    # For the optimized DP, we maintain running maximums for odd and even indices.
    # When considering pairing A[i] with A[j] (j < i), we require that the number of elements
    # between j and i is even, i.e., i - j - 1 is even, so i - j is odd.
    # This means j and i have different parity (if we use 0-based indexing for A).
    
    # Let's use 0-based indexing for A: A[0], A[1], ..., A[N-1]
    # dp[i] = max score for prefix of length i (A[0] to A[i-1])
    # To compute dp[i], we can:
    # 1. Not pair A[i-1]: dp[i] = dp[i-1]
    # 2. Pair A[i-1] with A[j] where j < i-1 and (i-1) - j is odd, i.e., i and j have different parity.
    #    The score is dp[j] + |A[i-1] - A[j]|
    
    # We maintain:
    # max_odd_minus: max(dp[j] - A[j]) for j odd
    # max_odd_plus: max(dp[j] + A[j]) for j odd
    # max_even_minus: max(dp[j] - A[j]) for j even
    # max_even_plus: max(dp[j] + A[j]) for j even
    
    dp = [0] * (N + 1)
    
    # Initialize running maximums to negative infinity
    max_odd_minus = float('-inf')
    max_odd_plus = float('-inf')
    max_even_minus = float('-inf')
    max_even_plus = float('-inf')
    
    for i in range(1, N + 1):
        # i is the length of the prefix, so we're considering A[i-1]
        # If i is even, we can pair A[i-1] with A[j] where j is odd (0-based index)
        # If i is odd, we can pair A[i-1] with A[j] where j is even (0-based index)
        
        candidate = float('-inf')
        
        if i % 2 == 0:
            # i is even, so j (0-based index) is odd
            if max_odd_minus != float('-inf'):
                candidate = max(candidate, max_odd_minus + A[i-1])
            if max_odd_plus != float('-inf'):
                candidate = max(candidate, max_odd_plus - A[i-1])
        else:
            # i is odd, so j (0-based index) is even
            if max_even_minus != float('-inf'):
                candidate = max(candidate, max_even_minus + A[i-1])
            if max_even_plus != float('-inf'):
                candidate = max(candidate, max_even_plus - A[i-1])
        
        dp[i] = max(dp[i-1], candidate)
        
        # Update running maximums for j = i-1 (0-based index)
        # The value to store is dp[j] = dp[i-1]
        val = dp[i-1]
        idx = i - 1  # 0-based index
        
        if idx % 2 == 1:
            # j is odd
            max_odd_minus = max(max_odd_minus, val - A[idx])
            max_odd_plus = max(max_odd_plus, val + A[idx])
        else:
            # j is even
            max_even_minus = max(max_even_minus, val - A[idx])
            max_even_plus = max(max_even_plus, val + A[idx])
    
    print(dp[N])

solve()