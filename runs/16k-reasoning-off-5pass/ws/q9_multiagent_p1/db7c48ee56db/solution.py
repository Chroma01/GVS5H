import sys

# Increase recursion depth to handle cases where K is large (though constraints limit combinations)
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Edge case: K=0 (though constraints say K>=1)
    if K == 0:
        print(0)
        return
    
    # Edge case: K=N, XOR sum of all elements
    if K == N:
        ans = 0
        for x in A:
            ans ^= x
        print(ans)
        return

    # We need to choose K distinct elements to maximize XOR sum.
    # Constraint: C(N, K) <= 10^6. This allows us to iterate through all combinations.
    # We use a recursive backtracking approach.
    
    max_xor = 0
    
    # Recursive function:
    # idx: current index in A
    # count: number of elements selected so far
    # current_xor: XOR sum of selected elements
    def backtrack(idx, count, current_xor):
        nonlocal max_xor
        
        # Pruning: Check if there are enough remaining elements to complete the selection
        # Remaining elements available: N - idx
        # Elements needed: K - count
        if N - idx < K - count:
            return
        
        # Base case: Selected exactly K elements
        if count == K:
            if current_xor > max_xor:
                max_xor = current_xor
            return
        
        # Branch 1: Include A[idx]
        # We proceed if we haven't reached K yet
        if count + 1 <= K:
            backtrack(idx + 1, count + 1, current_xor ^ A[idx])
        
        # Branch 2: Exclude A[idx]
        # We can only exclude if there are enough remaining elements after this index
        # to fill the quota.
        if N - (idx + 1) >= K - count:
            backtrack(idx + 1, count, current_xor)

    # Start recursion
    backtrack(0, 0, 0)
    
    print(max_xor)

if __name__ == '__main__':
    solve()