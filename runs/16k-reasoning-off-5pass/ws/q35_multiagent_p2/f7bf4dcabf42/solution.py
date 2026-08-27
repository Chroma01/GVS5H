import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    
    MOD = 998244353
    
    # Precompute transitions: for each mask and each character, what is the next mask?
    # mask represents the LCS row state.
    # Bit j (0-indexed) of mask is 1 if dp[j+1] > dp[j], i.e., if the LCS value increases at position j+1.
    # dp[j] = popcount(mask & ((1 << j) - 1))
    
    num_states = 1 << N
    transitions = [[0] * 26 for _ in range(num_states)]
    
    for mask in range(num_states):
        # Reconstruct the previous row dp[0..N]
        # dp[0] = 0
        # dp[j] = number of set bits in mask in positions 0 to j-1
        dp_prev = [0] * (N + 1)
        for j in range(1, N + 1):
            # Count bits in mask from position 0 to j-1
            # mask & ((1 << j) - 1) gives the lower j bits
            dp_prev[j] = bin(mask & ((1 << j) - 1)).count('1')
        
        # For each character c, compute the new row
        for char_code in range(26):
            c = chr(ord('a') + char_code)
            dp_curr = [0] * (N + 1)
            for j in range(1, N + 1):
                # dp_curr[j] = max(dp_prev[j], dp_prev[j-1] + (1 if S[j-1] == c else 0))
                match = 1 if S[j-1] == c else 0
                dp_curr[j] = max(dp_prev[j], dp_prev[j-1] + match)
            
            # Convert dp_curr back to a mask
            # Bit j (0-indexed) is 1 if dp_curr[j+1] > dp_curr[j]
            new_mask = 0
            for j in range(N):
                if dp_curr[j+1] > dp_curr[j]:
                    new_mask |= (1 << j)
            
            transitions[mask][char_code] = new_mask
    
    # DP: dp[step][mask] = number of strings of length 'step' resulting in state 'mask'
    # We only need the previous step, so we can use two arrays
    dp = [0] * num_states
    dp[0] = 1  # Initial state: empty string, mask = 0
    
    for step in range(M):
        new_dp = [0] * num_states
        for mask in range(num_states):
            if dp[mask] == 0:
                continue
            count = dp[mask]
            for char_code in range(26):
                next_mask = transitions[mask][char_code]
                new_dp[next_mask] = (new_dp[next_mask] + count) % MOD
        dp = new_dp
    
    # Collect results: for each k, sum dp[mask] for all masks with popcount k
    ans = [0] * (N + 1)
    for mask in range(num_states):
        if dp[mask] == 0:
            continue
        k = bin(mask).count('1')
        ans[k] = (ans[k] + dp[mask]) % MOD
    
    # Print the answers
    print(' '.join(map(str, ans)))

solve()