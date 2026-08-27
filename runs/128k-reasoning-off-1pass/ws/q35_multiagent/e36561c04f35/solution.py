import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    try:
        T = int(next(iterator))
    except StopIteration:
        return

    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            A = []
            for _ in range(N):
                A.append(int(next(iterator)))
        except StopIteration:
            break
            
        # dp[i] is the min cost to clear the suffix A[i:]
        # We use a list for dp. dp[N] = 0.
        # We process from right to left.
        
        dp = [0] * (N + 1)
        
        # next_occ[v] will store the index of the next occurrence of value v
        # We can use a dictionary or an array since values are up to N.
        # Using a dictionary for sparsity/simplicity, or array for speed.
        # Given constraints, array is fine.
        next_occ = {}
        
        # We can precompute next occurrences or compute on the fly.
        # Computing on the fly: store the last seen index for each value.
        # But we need the *next* occurrence for the current i.
        # So we can iterate backwards and maintain the last seen index.
        
        last_seen = {}
        
        for i in range(N - 1, -1, -1):
            val = A[i]
            
            # Option 1: Delete A[i] alone
            # Cost is 1 (delete) + dp[i+1] (clear the rest)
            # Note: The problem allows deleting a prefix of identical elements.
            # If we clear A[i+1:] first, A[i] is at the front.
            # So we can delete it in 1 op.
            res = 1 + dp[i+1]
            
            # Option 2: Group A[i] with a subsequent occurrence of the same value
            if val in last_seen:
                j = last_seen[val]
                # If we group A[i] with A[j], we bring A[j] to A[i]'s position.
                # The cost is (j - i) swaps to bring A[j] to i.
                # Then we delete the block. The cost to clear the rest (after j) is dp[j+1].
                # The elements between i and j are effectively handled by the structure of the DP.
                # The recurrence dp[i] = min(dp[i], dp[j+1] + (j - i)) is standard for this problem.
                cost_group = dp[j+1] + (j - i)
                if cost_group < res:
                    res = cost_group
            
            dp[i] = res
            last_seen[val] = i
            
        results.append(str(dp[0]))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()