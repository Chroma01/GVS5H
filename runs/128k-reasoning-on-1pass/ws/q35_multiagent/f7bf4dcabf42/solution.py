import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        S = next(iterator)
    except StopIteration:
        return

    MOD = 998244353
    
    num_states = 1 << N
    
    # mask_dp[mask][i] = LCS(S[0..i-1], T) for the profile represented by mask
    mask_dp = [[0] * (N + 1) for _ in range(num_states)]
    
    for mask in range(num_states):
        current_val = 0
        for i in range(N):
            if (mask >> i) & 1:
                current_val += 1
            mask_dp[mask][i + 1] = current_val
    
    # Precompute transitions: for each mask and each character, compute next mask
    trans_counts = [None] * num_states
    
    for mask in range(num_states):
        curr_dp = mask_dp[mask]
        counts = {}
        
        for char_code in range(26):
            c = chr(ord('a') + char_code)
            
            next_dp = [0] * (N + 1)
            
            for i in range(N):
                if S[i] == c:
                    next_dp[i + 1] = curr_dp[i] + 1
                else:
                    val1 = curr_dp[i + 1]
                    val2 = next_dp[i]
                    next_dp[i + 1] = val1 if val1 > val2 else val2
            
            next_mask = 0
            for i in range(N):
                if next_dp[i + 1] > next_dp[i]:
                    next_mask |= (1 << i)
            
            counts[next_mask] = counts.get(next_mask, 0) + 1
        
        trans_counts[mask] = list(counts.items())
    
    # DP over M steps
    dp_state = [0] * num_states
    dp_state[0] = 1
    
    for step in range(M):
        new_dp_state = [0] * num_states
        for mask in range(num_states):
            count = dp_state[mask]
            if count == 0:
                continue
            
            for next_mask, freq in trans_counts[mask]:
                new_dp_state[next_mask] = (new_dp_state[next_mask] + count * freq) % MOD
        
        dp_state = new_dp_state
    
    # Collect answers by popcount of mask
    ans = [0] * (N + 1)
    for mask in range(num_states):
        count = dp_state[mask]
        if count == 0:
            continue
        k = bin(mask).count('1')
        ans[k] = (ans[k] + count) % MOD
    
    print(*(ans))

if __name__ == '__main__':
    solve()