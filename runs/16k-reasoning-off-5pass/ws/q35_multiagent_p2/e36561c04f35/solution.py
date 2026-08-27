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
            
        # dp[i] is the min cost to empty the prefix A[0...i-1] (length i)
        # dp[0] = 0
        dp = [0] * (N + 1)
        
        # last_pos stores the last seen 1-based index of each value
        last_pos = {}
        
        for i in range(1, N + 1):
            val = A[i-1]
            
            # Option 1: Delete A[i-1] individually (or as part of a single-element deletion)
            # Cost is dp[i-1] + 1
            dp[i] = dp[i-1] + 1
            
            # Option 2: If val appeared before at index j (1-based),
            # we can potentially group A[i-1] with the occurrence at j.
            # The cost is dp[j-1] + (i - j)
            if val in last_pos:
                j = last_pos[val]
                cost = dp[j-1] + (i - j)
                if cost < dp[i]:
                    dp[i] = cost
            
            # Update last position
            last_pos[val] = i
            
        results.append(str(dp[N]))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()