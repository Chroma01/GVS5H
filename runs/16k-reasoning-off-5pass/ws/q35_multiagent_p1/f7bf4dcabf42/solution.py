import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    
    MOD = 998244353
    
    # dp[mask] = number of strings of current length that result in this LCS row state
    # mask is an N-bit integer where bit i (0-indexed) corresponds to S[i]
    # The value of the LCS row at position i+1 is the number of set bits in mask from bit 0 to i.
    # Specifically, if mask has bits b_0, b_1, ..., b_{N-1}, then:
    # dp_row[0] = 0
    # dp_row[i+1] = dp_row[i] + b_i
    
    dp = [0] * (1 << N)
    dp[0] = 1  # Empty string has LCS row all zeros
    
    # Precompute transitions for each mask and each character
    # Since N is small (<=10), we can compute on the fly or precompute.
    # Let's compute on the fly for simplicity, it's fast enough.
    
    for _ in range(M):
        new_dp = [0] * (1 << N)
        
        for mask in range(1 << N):
            if dp[mask] == 0:
                continue
            
            # Reconstruct the previous LCS row from the mask
            # prev_row[i] is the LCS value for S[0...i-1]
            prev_row = [0] * (N + 1)
            for i in range(N):
                if (mask >> i) & 1:
                    prev_row[i+1] = prev_row[i] + 1
                else:
                    prev_row[i+1] = prev_row[i]
            
            # Try all 26 characters
            for char_code in range(26):
                c = chr(ord('a') + char_code)
                
                # Compute new LCS row
                curr_row = [0] * (N + 1)
                for i in range(1, N + 1):
                    if S[i-1] == c:
                        curr_row[i] = prev_row[i-1] + 1
                    else:
                        curr_row[i] = max(curr_row[i-1], prev_row[i])
                
                # Convert new row back to mask
                new_mask = 0
                for i in range(N):
                    if curr_row[i+1] > curr_row[i]:
                        new_mask |= (1 << i)
                
                new_dp[new_mask] = (new_dp[new_mask] + dp[mask]) % MOD
        
        dp = new_dp
    
    # Aggregate results by LCS length (popcount of mask)
    ans = [0] * (N + 1)
    for mask in range(1 << N):
        if dp[mask] > 0:
            lcs_len = bin(mask).count('1')
            ans[lcs_len] = (ans[lcs_len] + dp[mask]) % MOD
    
    print(' '.join(map(str, ans)))

solve()