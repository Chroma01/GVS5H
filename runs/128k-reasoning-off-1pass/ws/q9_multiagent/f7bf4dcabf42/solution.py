import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

def solve():
    # Read input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    
    MOD = 998244353
    
    # Map char to 0-25
    char_to_int = {chr(ord('a') + i): i for i in range(26)}
    
    # Precompute next_occurrence[i][c]
    # next_occ[i][c] stores the index of the first occurrence of char c strictly after i.
    # i ranges from 0 to N. (N means no characters after)
    next_occ = [[-1] * 26 for _ in range(N + 1)]
    
    last_seen = [-1] * 26
    
    # Fill from right to left
    for i in range(N - 1, -1, -1):
        char_idx = char_to_int[S[i]]
        for c in range(26):
            next_occ[i][c] = last_seen[c]
        last_seen[char_idx] = i
        
    num_states = 1 << N
    
    # Precompute transitions to speed up
    # can_extend[mask][c] is True if appending char c can extend the LCS for the given mask
    # new_mask[mask][c] is the new set of possible ending indices if extended
    can_extend = [[False] * 26 for _ in range(num_states)]
    new_mask = [[0] * 26 for _ in range(num_states)]
    
    for mask in range(num_states):
        for c in range(26):
            if mask == 0:
                can_extend[mask][c] = False
                new_mask[mask][c] = 0
                continue
                
            temp_mask = mask
            found = False
            union_mask = 0
            
            # Iterate bits of the mask
            while temp_mask > 0:
                lsb = temp_mask & -temp_mask
                idx = lsb.bit_length() - 1
                
                nxt = next_occ[idx][c]
                if nxt != -1:
                    found = True
                    union_mask |= (1 << nxt)
                
                temp_mask ^= lsb
            
            can_extend[mask][c] = found
            new_mask[mask][c] = union_mask

    # DP State:
    # dp[j][mask] = number of strings of current length such that:
    #   - The LCS length with S is exactly j.
    #   - The set of possible ending indices of this LCS in S is represented by 'mask'.
    
    # Initialize
    # dp[0][0] = 1 (Length 0 string, LCS 0, empty mask)
    dp = [[0] * num_states for _ in range(N + 1)]
    dp[0][0] = 1
    
    # DP Iteration
    for length in range(M):
        next_dp = [[0] * num_states for _ in range(N + 1)]
        
        for j in range(N + 1):
            for mask in range(num_states):
                count = dp[j][mask]
                if count == 0:
                    continue
                
                # Try all 26 characters
                for c in range(26):
                    if can_extend[mask][c]:
                        # Extend LCS
                        new_j = j + 1
                        new_m = new_mask[mask][c]
                        if new_j <= N:
                            next_dp[new_j][new_m] = (next_dp[new_j][new_m] + count) % MOD
                    else:
                        # Cannot extend
                        next_dp[j][mask] = (next_dp[j][mask] + count) % MOD
        
        dp = next_dp
    
    # After M steps, sum up counts for each j
    ans = [0] * (N + 1)
    for j in range(N + 1):
        total = 0
        for mask in range(num_states):
            total = (total + dp[j][mask]) % MOD
        ans[j] = total
    
    # Output
    print(*(ans))

if __name__ == '__main__':
    solve()