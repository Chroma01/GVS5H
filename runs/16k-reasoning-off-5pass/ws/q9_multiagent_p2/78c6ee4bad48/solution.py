import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        N = int(n_str)
        
        X = []
        for _ in range(N):
            X.append(int(next(iterator)))
    except StopIteration:
        return

    # x_1 is the first coordinate, which is invariant
    x1 = X[0]
    
    # Calculate differences d_1, d_2, ..., d_{N-1}
    # In 0-based indexing for the list D:
    # D[i] corresponds to the difference between the (i+1)-th and (i+2)-th pieces in sorted order.
    # This corresponds to d_{i+1} in 1-based notation.
    D = []
    for i in range(N - 1):
        D.append(X[i+1] - X[i])
    
    # Separate differences into two independent sets based on index parity
    # We can swap D[i] and D[i+2], so elements at even indices stay in even positions,
    # and elements at odd indices stay in odd positions.
    odds = []
    evens = []
    
    for i in range(len(D)):
        if i % 2 == 0:
            odds.append(D[i])
        else:
            evens.append(D[i])
            
    # Sort both lists to minimize the weighted sum
    odds.sort()
    evens.sort()
    
    # Reconstruct the minimal sum
    # Sum = N * x_1 + sum_{k=1}^{N-1} (N - k) * d_k
    # In 0-based index i for D (where i = k-1):
    # Weight = N - (i + 1) = N - 1 - i
    
    total_sum = N * x1
    
    # We need to place sorted odds at indices 0, 2, 4... and evens at 1, 3, 5...
    # However, since we sorted them, we just iterate through the original positions
    # and pick the next available value from the sorted lists.
    
    odd_idx = 0
    even_idx = 0
    
    for i in range(len(D)):
        weight = N - 1 - i
        if i % 2 == 0:
            val = odds[odd_idx]
            odd_idx += 1
        else:
            val = evens[even_idx]
            even_idx += 1
        
        total_sum += weight * val
        
    print(total_sum)

if __name__ == '__main__':
    solve()