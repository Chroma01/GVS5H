import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    
    MOD = 998244353
    
    # Precompute transitions for each mask and each character 'a' to 'z'
    # There are 2^N states (masks of length N)
    num_states = 1 << N
    
    # trans[mask][char_index] = new_mask
    # char_index: 0 for 'a', 1 for 'b', ..., 25 for 'z'
    trans = [[0] * 26 for _ in range(num_states)]
    
    for mask in range(num_states):
        # Reconstruct dp array from mask
        # dp[j] for j in 0..N
        # dp[0] = 0
        # dp[j] = dp[j-1] + (1 if bit (j-1) of mask is set else 0)
        dp = [0] * (N + 1)
        for j in range(1, N + 1):
            if (mask >> (j - 1)) & 1:
                dp[j] = dp[j-1] + 1
            else:
                dp[j] = dp[j-1]
        
        for c_idx in range(26):
            c = chr(ord('a') + c_idx)
            # Compute new_dp for LCS(S[0..j-1], T + c)
            # new_dp[j] = LCS(S[0..j-1], T + c)
            # Standard recurrence:
            # new_dp[0] = 0
            # for j from 1 to N:
            #   if S[j-1] == c:
            #       new_dp[j] = dp[j-1] + 1
            #   else:
            #       new_dp[j] = max(new_dp[j-1], dp[j])
            
            new_dp = [0] * (N + 1)
            for j in range(1, N + 1):
                if S[j-1] == c:
                    new_dp[j] = dp[j-1] + 1
                else:
                    new_dp[j] = max(new_dp[j-1], dp[j])
            
            # Convert new_dp back to mask
            new_mask = 0
            for j in range(1, N + 1):
                if new_dp[j] > new_dp[j-1]:
                    new_mask |= (1 << (j - 1))
            
            trans[mask][c_idx] = new_mask
    
    # DP over M steps
    # dp_count[mask] = number of ways to reach this mask after processing some prefix of T
    dp_count = [0] * num_states
    dp_count[0] = 1  # Initial state: no characters processed, mask=0
    
    for step in range(M):
        new_dp_count = [0] * num_states
        for mask in range(num_states):
            if dp_count[mask] == 0:
                continue
            count = dp_count[mask]
            for c_idx in range(26):
                new_mask = trans[mask][c_idx]
                new_dp_count[new_mask] = (new_dp_count[new_mask] + count) % MOD
        dp_count = new_dp_count
    
    # Sum up counts by popcount (LCS length)
    ans = [0] * (N + 1)
    for mask in range(num_states):
        if dp_count[mask] == 0:
            continue
        # LCS length is the number of set bits in mask
        lcs_len = bin(mask).count('1')
        ans[lcs_len] = (ans[lcs_len] + dp_count[mask]) % MOD
    
    # Print answers
    print(' '.join(map(str, ans)))

solve()