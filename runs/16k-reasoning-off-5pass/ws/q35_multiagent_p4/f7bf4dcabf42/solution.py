import sys

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    
    MOD = 998244353
    
    # The state is represented by a tuple of length N+1: (dp[0], dp[1], ..., dp[N])
    # where dp[j] = LCS(S[0..j-1], current_T_prefix)
    # dp[0] = 0 always, and dp[j] - dp[j-1] in {0, 1}
    # So the state is determined by which j in {1, ..., N} have dp[j] > dp[j-1]
    # We can represent this as a bitmask of length N, where bit (j-1) is 1 if dp[j] > dp[j-1]
    
    # Precompute all valid states (masks)
    # A mask is valid if it represents a non-decreasing sequence with steps 0 or 1
    # Actually, any mask from 0 to 2^N - 1 is valid because:
    # dp[j] = number of set bits in mask among first j bits
    # This automatically satisfies dp[0]=0 and dp[j]-dp[j-1] in {0,1}
    
    num_states = 1 << N
    
    # Precompute the dp vector from a mask
    def mask_to_dp(mask):
        dp = [0] * (N + 1)
        for j in range(1, N + 1):
            # bit (j-1) tells us if dp[j] > dp[j-1]
            if mask & (1 << (j - 1)):
                dp[j] = dp[j-1] + 1
            else:
                dp[j] = dp[j-1]
        return dp
    
    # Precompute transitions: for each mask and each character, compute next mask
    # Transitions: trans[mask][char_index] = next_mask
    trans = [[0] * 26 for _ in range(num_states)]
    
    for mask in range(num_states):
        dp = mask_to_dp(mask)
        for c_idx in range(26):
            c = chr(ord('a') + c_idx)
            # Compute new_dp after appending character c
            new_dp = list(dp)  # copy
            # Standard LCS row update:
            # new_dp[j] = max(new_dp[j-1], new_dp[j]) for all j
            # Then if S[j-1] == c, new_dp[j] = max(new_dp[j], dp[j-1] + 1)
            # Note: we need to use the old dp values for the second part
            
            # First pass: new_dp[j] = max(new_dp[j-1], new_dp[j])
            for j in range(1, N + 1):
                new_dp[j] = max(new_dp[j-1], new_dp[j])
            
            # Second pass: if S[j-1] == c, update using old dp
            for j in range(1, N + 1):
                if S[j-1] == c:
                    new_dp[j] = max(new_dp[j], dp[j-1] + 1)
            
            # Convert new_dp to mask
            new_mask = 0
            for j in range(1, N + 1):
                if new_dp[j] > new_dp[j-1]:
                    new_mask |= (1 << (j - 1))
            
            trans[mask][c_idx] = new_mask
    
    # DP: dp_count[mask] = number of strings of current length that lead to this state
    dp_count = [0] * num_states
    initial_mask = 0  # dp = [0, 0, ..., 0]
    dp_count[initial_mask] = 1
    
    for step in range(M):
        new_dp_count = [0] * num_states
        for mask in range(num_states):
            if dp_count[mask] == 0:
                continue
            count = dp_count[mask]
            for c_idx in range(26):
                next_mask = trans[mask][c_idx]
                new_dp_count[next_mask] = (new_dp_count[next_mask] + count) % MOD
        dp_count = new_dp_count
    
    # Compute answers: for each k, sum dp_count[mask] where dp[N] == k
    # dp[N] for a mask is the number of set bits in the mask
    ans = [0] * (N + 1)
    for mask in range(num_states):
        if dp_count[mask] == 0:
            continue
        # Count set bits in mask
        k = bin(mask).count('1')
        ans[k] = (ans[k] + dp_count[mask]) % MOD
    
    # Output
    print(' '.join(map(str, ans)))

solve()