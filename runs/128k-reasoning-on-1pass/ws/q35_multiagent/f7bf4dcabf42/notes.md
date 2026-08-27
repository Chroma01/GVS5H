
## ideation
```python
import sys

# Increase recursion depth just in case, though not needed here
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
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
    
    # Number of states is 2^N
    num_states = 1 << N
    
    # mask_dp[mask] will store the LCS values for each prefix of S
    # mask_dp[mask][i] corresponds to LCS(S[0...i-1], T)
    # Size is (N+1)
    mask_dp = [ [0]*(N+1) for _ in range(num_states) ]
    
    for mask in range(num_states):
        current_val = 0
        for i in range(N):
            if (mask >> i) & 1:
                current_val += 1
            mask_dp[mask][i+1] = current_val
            
    # Precompute transitions
    # trans_counts[mask] will be a list of (next_mask, frequency)
    trans_counts = [None] * num_states
    
    for mask in range(num_states):
        curr_dp = mask_dp[mask]
        counts = {}
        
        # Try all 26 characters
        for char_code in range(26):
            c = chr(ord('a') + char_code)
            
            # Compute next_dp array
            next_dp = [0] * (N+1)
            # next_dp[0] is always 0
            
            for i in range(N):
                # S[i] is the character at index i (0-indexed)
                # We are computing LCS for S[0...i] and new T
                if S[i] == c:
                    next_dp[i+1] = curr_dp[i] + 1
                else:
                    # max(LCS(S[0...i], old T), LCS(S[0...i-1], new T))
                    # curr_dp[i+1] is LCS(S[0...i], old T)
                    # next_dp[i] is LCS(S[0...i-1], new T)
                    val1 = curr_dp[i+1]
                    val2 = next_dp[i]
                    next_dp[i+1] = val1 if val1 > val2 else val2
            
            # Convert next_dp to next_mask
            next_mask = 0
            for i in range(N):
                if next_dp[i+1] > next_dp[i]:
                    next_mask |= (1 << i)
            
            counts[next_mask] = counts.get(next_mask, 0) + 1
        
        trans_counts[mask] = list(counts.items())

    # DP over M steps
    # dp_state[mask] = number of strings T of current length that result in state mask
    dp_state = [0] * num_states
    dp_state[0] = 1
    
    for step in range(M):
        new_dp_state = [0] * num_states
        for mask in range(num_states):
            count = dp_state[mask]
            if count == 0:
                continue
            
            # Iterate over possible next states
            for next_mask, freq in trans_counts[mask]:
                # Add count * freq to new_dp_state[next_mask]
                # Using modulo arithmetic
                new_dp_state[next_mask] = (new_dp_state[next_mask] + count * freq) % MOD
        
        dp_state = new_dp_state

    # Collect answers
    ans = [0] * (N+1)
    for mask in range(num_states):
        count = dp_state[mask]
        if count == 0:
            continue
        # Popcount gives the LCS length
        k = bin(mask).count('1')
        ans[k] = (ans[k] + count) % MOD
        
    print(*(ans))

if __name__ == '__main__':
    solve()
```

## worker: finalize
The key insight is that the LCS profile of S with a string T can be represented by a bitmask of length N, where the i-th bit is 1 if LCS(S[0..i], T) > LCS(S[0..i-1], T). This profile uniquely determines the LCS values dp[i] = LCS(S[0..i-1], T) for all i.

The transition when appending character c to T follows the standard LCS recurrence:
- If S[i] == c: next_dp[i+1] = dp[i] + 1
- If S[i] != c: next_dp[i+1] = max(dp[i+1], next_dp[i])

The popcount of the final mask equals dp[N], which is the total LCS length. The algorithm runs in O(M · 2^N · 26) time, which is well within limits for N ≤ 10, M ≤ 100.

Verified against all three sample inputs.
