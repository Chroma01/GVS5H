import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    iterator = iter(data)
    N = int(next(iterator))
    X = int(next(iterator))
    
    foods = []
    for i in range(N):
        V = int(next(iterator))
        A = int(next(iterator))
        C = int(next(iterator))
        foods.append((V, A, C))
    
    # Compute upper bound for binary search
    sums = [0, 0, 0, 0]  # 1-indexed
    for V, A, C in foods:
        sums[V] += A
    
    max_k = min(sums[1], sums[2], sums[3])
    
    if max_k == 0:
        print(0)
        return
    
    # Cap K at 5000 for DP feasibility
    cap_k = 5000
    upper = min(max_k, cap_k)
    
    def feasible(K):
        if K == 0:
            return True
        if K > cap_k:
            return False
        
        # dp[i][j][0] = min calories for vit1 >= i, vit2 >= j, vit3 < K
        # dp[i][j][1] = min calories for vit1 >= i, vit2 >= j, vit3 >= K
        # Initialize with infinity
        INF = float('inf')
        dp0 = [[INF] * (K + 1) for _ in range(K + 1)]
        dp1 = [[INF] * (K + 1) for _ in range(K + 1)]
        
        dp0[0][0] = 0
        
        for V, A, C in foods:
            # Create new DP tables for the next iteration
            new_dp0 = [row[:] for row in dp0]
            new_dp1 = [row[:] for row in dp1]
            
            for i in range(K + 1):
                for j in range(K + 1):
                    if dp0[i][j] == INF and dp1[i][j] == INF:
                        continue
                    
                    cur_cal0 = dp0[i][j]
                    cur_cal1 = dp1[i][j]
                    
                    if V == 1:
                        ni = min(i + A, K)
                        nj = j
                        nc = C
                        
                        if cur_cal0 + nc < new_dp0[ni][nj]:
                            new_dp0[ni][nj] = cur_cal0 + nc
                        if cur_cal1 + nc < new_dp1[ni][nj]:
                            new_dp1[ni][nj] = cur_cal1 + nc
                            
                    elif V == 2:
                        ni = i
                        nj = min(j + A, K)
                        nc = C
                        
                        if cur_cal0 + nc < new_dp0[ni][nj]:
                            new_dp0[ni][nj] = cur_cal0 + nc
                        if cur_cal1 + nc < new_dp1[ni][nj]:
                            new_dp1[ni][nj] = cur_cal1 + nc
                            
                    elif V == 3:
                        # For vitamin 3, we need to track the exact amount to know if it reaches K.
                        # But we don't have that information in the state.
                        # This approach is flawed.
                        pass
        
        # The above approach is incorrect because we don't track the exact amount of vitamin 3.
        # We need a 3D DP or a different formulation.
        # Let's restart with a 3D DP.
        
        # dp[i][j][k] = min calories to get at least i of vit1, j of vit2, k of vit3, with i,j,k in [0, K]
        # Initialize with infinity
        dp = [[[INF] * (K + 1) for _ in range(K + 1)] for _ in range(K + 1)]
        dp[0][0][0] = 0
        
        for V, A, C in foods:
            # Create new DP tables for the next iteration
            new_dp = [[[INF] * (K + 1) for _ in range(K + 1)] for _ in range(K + 1)]
            
            for i in range(K + 1):
                for j in range(K + 1):
                    for k in range(K + 1):
                        if dp[i][j][k] == INF:
                            continue
                        
                        cur_cal = dp[i][j][k]
                        
                        if V == 1:
                            ni = min(i + A, K)
                            nj = j
                            nk = k
                            nc = C
                            
                            if cur_cal + nc < new_dp[ni][nj][nk]:
                                new_dp[ni][nj][nk] = cur_cal + nc
                                
                        elif V == 2:
                            ni = i
                            nj = min(j + A, K)
                            nk = k
                            nc = C
                            
                            if cur_cal + nc < new_dp[ni][nj][nk]:
                                new_dp[ni][nj][nk] = cur_cal + nc
                                
                        elif V == 3:
                            ni = i
                            nj = j
                            nk = min(k + A, K)
                            nc = C
                            
                            if cur_cal + nc < new_dp[ni][nj][nk]:
                                new_dp[ni][nj][nk] = cur_cal + nc
            
            dp = new_dp
        
        # Check if dp[K][K][K] <= X
        return dp[K][K][K] <= X
    
    # Binary search
    low = 0
    high = upper
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        if feasible(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
            
    print(ans)

solve()