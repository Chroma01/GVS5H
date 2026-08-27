import sys

def solve():
    MOD = 998244353
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    M = int(next(it))
    S = next(it).strip()
    
    # Precompute transitions for all masks and all 26 characters
    size = 1 << N
    trans = [[0] * 26 for _ in range(size)]
    # Also precompute popcounts for masks
    popcnt = [0] * size
    for mask in range(size):
        popcnt[mask] = bin(mask).count('1')
    
    for mask in range(size):
        # Reconstruct dp from mask
        dp = [0] * (N + 1)
        for i in range(1, N + 1):
            if (mask >> (i - 1)) & 1:
                dp[i] = dp[i-1] + 1
            else:
                dp[i] = dp[i-1]
        # For each character, compute new state
        for c in range(26):
            ch = chr(ord('a') + c)
            new_dp = [0] * (N + 1)
            # Process from right to left
            for i in range(N, 0, -1):
                if S[i-1] == ch:
                    new_dp[i] = max(dp[i], new_dp[i-1] + 1)  # Wait: new_dp[i-1] is already computed? No, we go from N down to 1, so new_dp[i-1] is the new value for i-1? Let's check: we want old dp[i-1] (value from previous column). Since we are going downward, we haven't updated i-1 yet? Actually we are going from N to 1, so when at i, we have already updated indices i+1..N. We have not yet updated i-1. So new_dp[i-1] is still 0 (the initial value). That's wrong.
                    # We need to use old dp[i-1]. So we should use a separate array or use the old dp.
                    pass
    # The above attempt is flawed. Let's rewrite properly.

    # We need to use the old dp values for the transition. Since N is small, we can just copy old_dp and compute new_dp using old_dp values.
    # Let's restart precomputation.
    
    # Actually, we can precompute by simulating the update using a copy of dp.
    trans = [[0] * 26 for _ in range(size)]
    for mask in range(size):
        # Build dp from mask
        dp = [0] * (N + 1)
        for i in range(1, N + 1):
            dp[i] = dp[i-1] + ((mask >> (i - 1)) & 1)
        for c in range(26):
            ch = chr(ord('a') + c)
            old_dp = dp[:]  # copy
            new_dp = [0] * (N + 1)
            # Process i from N down to 1
            for i in range(N, 0, -1):
                if S[i-1] == ch:
                    new_dp[i] = max(old_dp[i], old_dp[i-1] + 1)
                else:
                    new_dp[i] = max(old_dp[i], old_dp[i-1])
            # Build new mask
            new_mask = 0
            for i in range(1, N + 1):
                if new_dp[i] > new_dp[i-1]:
                    new_mask |= (1 << (i - 1))
            trans[mask][c] = new_mask
    
    # DP over M steps
    cur = [0] * size
    cur[0] = 1
    for _ in range(M):
        nxt = [0] * size
        for mask in range(size):
            v = cur[mask]
            if v == 0:
                continue
            for c in range(26):
                nxt[trans[mask][c]] = (nxt[trans[mask][c]] + v) % MOD
        cur = nxt
    
    ans = [0] * (N + 1)
    for mask in range(size):
        k = popcnt[mask]
        ans[k] = (ans[k] + cur[mask]) % MOD
    
    print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()