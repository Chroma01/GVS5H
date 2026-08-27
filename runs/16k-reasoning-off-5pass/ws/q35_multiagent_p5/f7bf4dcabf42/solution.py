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

    # dp[mask] = number of strings of current length that result in the LCS profile 'mask'
    # mask is an integer where the i-th bit (0-indexed) corresponds to whether dp[i+1] > dp[i]
    # i.e., bit i is 1 if LCS(S[0..i], T) > LCS(S[0..i-1], T)
    # Since dp[0] = 0, and dp[i] - dp[i-1] is 0 or 1, the profile is fully determined by these differences.
    # The total LCS length is the number of set bits in the mask.
    
    # Initial state: empty string T, LCS with any prefix of S is 0.
    # So dp[i] = 0 for all i. Differences are all 0. Mask is 0.
    dp = {0: 1}

    # Precompute transitions for each mask and each character
    # To optimize, we can precompute the next mask for each current mask and character c.
    # But since N is small, we can compute on the fly or precompute.
    # Let's precompute for efficiency.
    
    # For a given mask, reconstruct the profile V
    # V[0] = 0
    # V[i] = V[i-1] + ((mask >> (i-1)) & 1) for i in 1..N
    
    # Then for each char c, compute new profile V'
    # V'[0] = 0
    # For i in 1..N:
    #   if S[i-1] == c:
    #       V'[i] = V[i-1] + 1
    #   else:
    #       V'[i] = max(V'[i-1], V[i])
    
    # Then convert V' to new mask.
    
    # Precompute transition table: trans[mask][char_index] -> new_mask
    # char_index: 0 for 'a', ..., 25 for 'z'
    
    trans = {}
    
    for mask in range(1 << N):
        # Reconstruct profile V
        V = [0] * (N + 1)
        for i in range(1, N + 1):
            if (mask >> (i - 1)) & 1:
                V[i] = V[i - 1] + 1
            else:
                V[i] = V[i - 1]
        
        new_mask_for_char = {}
        for char_code in range(26):
            c = chr(ord('a') + char_code)
            V_new = [0] * (N + 1)
            for i in range(1, N + 1):
                if S[i - 1] == c:
                    V_new[i] = V[i - 1] + 1
                else:
                    V_new[i] = max(V_new[i - 1], V[i])
            
            # Convert V_new to mask
            new_mask = 0
            for i in range(1, N + 1):
                if V_new[i] > V_new[i - 1]:
                    new_mask |= (1 << (i - 1))
            new_mask_for_char[char_code] = new_mask
        trans[mask] = new_mask_for_char

    # DP over M steps
    for _ in range(M):
        new_dp = {}
        for mask, count in dp.items():
            for char_code in range(26):
                next_mask = trans[mask][char_code]
                new_dp[next_mask] = (new_dp.get(next_mask, 0) + count) % MOD
        dp = new_dp

    # Aggregate results by LCS length (popcount of mask)
    ans = [0] * (N + 1)
    for mask, count in dp.items():
        k = bin(mask).count('1')
        ans[k] = (ans[k] + count) % MOD

    # Print answers
    print(' '.join(map(str, ans)))

solve()