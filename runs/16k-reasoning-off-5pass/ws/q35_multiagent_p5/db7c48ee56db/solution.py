import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # We need to find the maximum XOR sum of any K distinct elements from A.
    # Constraint: binom(N, K) <= 10^6.
    # We can use recursive backtracking with pruning to iterate through all combinations.
    
    max_xor = 0
    
    # Recursive function to generate combinations
    # index: current index in A we are considering
    # count: number of elements selected so far
    # current_xor: XOR sum of selected elements so far
    def backtrack(index, count, current_xor):
        nonlocal max_xor
        
        # Base case: if we have selected K elements
        if count == K:
            if current_xor > max_xor:
                max_xor = current_xor
            return
        
        # If we have processed all elements but haven't selected K, this path is invalid
        if index == N:
            return
            
        # Pruning: if remaining elements are not enough to fill the remaining spots
        remaining_elements = N - index
        needed_elements = K - count
        if remaining_elements < needed_elements:
            return
        
        # Option 1: Include A[index]
        # We must include it if we don't have enough elements otherwise
        # But we can always choose to include or exclude, subject to pruning
        # Include A[index]
        backtrack(index + 1, count + 1, current_xor ^ A[index])
        
        # Option 2: Exclude A[index]
        # Only possible if we can still form a valid combination without it
        # i.e., remaining elements after excluding (N - index - 1) must be >= needed_elements
        if (N - index - 1) >= needed_elements:
            backtrack(index + 1, count, current_xor)

    # Start the backtracking
    # Initial state: index 0, count 0, current_xor 0
    backtrack(0, 0, 0)
    
    print(max_xor)

if __name__ == '__main__':
    solve()