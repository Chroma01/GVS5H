import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    
    MOD = 998244353
    
    # S is 0-indexed. 
    # State mask: N bits. bit i (0 to N-1) is 1 if v[i+1] == v[i] + 1, else 0.
    # v[0] is always 0. v[k] = sum of bits 0 to k-1.
    
    # dp[mask] = count of ways to reach this state
    dp = {0: 1}
    
    # Precompute S characters
    S_chars = list(S)
    
    # Precompute transitions for each character to avoid recomputing logic inside the loop
    # transitions[char_code][mask] -> new_mask
    # Since N is small (<=10), we can precompute this table.
    # There are 26 characters and 2^N states.
    
    transitions = {}
    for char_code in range(26):
        char = chr(ord('a') + char_code)
        trans_map = {}
        for mask in range(1 << N):
            # Reconstruct vector v from mask
            v = [0] * (N + 1)
            current_val = 0
            for i in range(N):
                if (mask >> i) & 1:
                    current_val += 1
                v[i+1] = current_val
            
            # Compute v' based on char
            # Recurrence: v'[i] = max(v'[i-1], v[i] + (1 if S[i-1] == char else 0))
            # Note: The standard LCS recurrence for updating the row when adding a character c to T is:
            # new_dp[i] = max(new_dp[i-1], old_dp[i] + (1 if S[i-1] == c else 0))
            # Here v corresponds to old_dp (LCS of S[0..i-1] and T_prefix)
            # v_new corresponds to new_dp (LCS of S[0..i-1] and T_prefix + c)
            
            v_new = [0] * (N + 1)
            prev_v_prime = 0
            
            for i in range(1, N + 1):
                match = (S_chars[i-1] == char)
                candidate = v[i] + (1 if match else 0)
                if candidate > prev_v_prime:
                    v_new[i] = candidate
                else:
                    v_new[i] = prev_v_prime
                prev_v_prime = v_new[i]
            
            # Convert v_new back to mask
            new_mask = 0
            for i in range(N):
                if v_new[i+1] == v_new[i] + 1:
                    new_mask |= (1 << i)
            
            trans_map[mask] = new_mask
        transitions[char_code] = trans_map

    # Iterate M times for each character of the generated string T
    for step in range(M):
        new_dp = {}
        
        # Try all 26 lowercase English letters
        for char_code in range(26):
            trans_map = transitions[char_code]
            
            # For each existing state, compute the transition
            for mask, count in dp.items():
                new_mask = trans_map[mask]
                
                if new_mask not in new_dp:
                    new_dp[new_mask] = 0
                new_dp[new_mask] = (new_dp[new_mask] + count) % MOD
        
        dp = new_dp

    # Collect answers
    # ans[k] is the number of strings with LCS length exactly k
    ans = [0] * (N + 1)
    
    for mask, count in dp.items():
        lcs_len = 0
        for i in range(N):
            if (mask >> i) & 1:
                lcs_len += 1
        ans[lcs_len] = (ans[lcs_len] + count) % MOD
        
    # Print results
    print(*(ans))

if __name__ == '__main__':
    solve()