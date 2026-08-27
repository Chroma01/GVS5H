import sys

# Increase recursion depth just in case, though we use an iterative approach
sys.setrecursionlimit(200005)

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

    MOD = 998244353

    # dp[k] will store the coefficient of z^k in H_v(z)
    # Initially for v=0, H_0(z) = 0, so all dp are 0
    dp = [0] * (K + 1)
    
    total_ans = 0

    # Iterate through each element A[i]
    for x in A:
        # We need to update dp to represent H_v(z) = (1 + x*z) * (H_{v-1}(z) + 1)
        # Let P(z) = H_{v-1}(z) + 1
        # P[0] = dp[0] + 1
        # P[k] = dp[k] for k >= 1
        
        # We compute new_dp = (1 + x*z) * P(z)
        # new_dp[0] = P[0]
        # new_dp[k] = P[k] + x * P[k-1] for k >= 1
        
        # Calculate new_dp coefficients
        # new_dp[0] = dp[0] + 1
        # new_dp[k] = dp[k] + x * dp[k-1] for k >= 1
        
        # We can compute this in-place by iterating backwards to avoid overwriting needed values
        # However, creating a new list is cleaner and O(K) is small enough.
        
        new_dp = [0] * (K + 1)
        
        # new_dp[0]
        val0 = (dp[0] + 1) % MOD
        new_dp[0] = val0
        
        # new_dp[k] for k >= 1
        for k in range(1, K + 1):
            # P[k] is dp[k]
            # P[k-1] is dp[k-1]
            term1 = dp[k]
            term2 = (x * dp[k-1]) % MOD
            new_dp[k] = (term1 + term2) % MOD
            
        dp = new_dp
        
        # Add the coefficient of z^K to the total answer
        total_ans = (total_ans + dp[K]) % MOD

    print(total_ans)

if __name__ == '__main__':
    solve()