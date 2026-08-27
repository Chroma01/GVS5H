import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    
    MOD = 998244353
    
    # Precompute transitions for each bitmask state and each character
    # State is a bitmask of length N, where bit i (0-indexed) corresponds to position i in S (1-indexed in LCS DP)
    # Bit i is 1 if LCS(S[0:i], T) > LCS(S[0:i-1], T), i.e., the i-th value in the LCS row is greater than the (i-1)-th
    
    # Decode bitmask to LCS row: L[0] = 0, L[i] = L[i-1] + (1 if bit i-1 is set else 0)
    # Actually, let's use 0-indexed bits for positions 0 to N-1 in S.
    # Bit i corresponds to whether L[i+1] > L[i] in the LCS row of length N+1.
    # So L[0] = 0, L[1] = L[0] + (bit 0), L[2] = L[1] + (bit 1), etc.
    
    # Encode LCS row to bitmask: bit i = 1 if L[i+1] > L[i], else 0.
    
    # Precompute transitions
    # transitions[state][char_index] = next_state
    transitions = [[0] * 26 for _ in range(1 << N)]
    
    for state in range(1 << N):
        # Decode state to LCS row
        L = [0] * (N + 1)
        for i in range(N):
            if (state >> i) & 1:
                L[i + 1] = L[i] + 1
            else:
                L[i + 1] = L[i]
        
        # For each character, compute next state
        for char_code in range(26):
            c = chr(ord('a') + char_code)
            # Compute new LCS row
            new_L = [0] * (N + 1)
            for i in range(1, N + 1):
                if S[i - 1] == c:
                    new_L[i] = L[i - 1] + 1
                else:
                    new_L[i] = max(new_L[i - 1], L[i])
            
            # Encode new_L to bitmask
            new_state = 0
            for i in range(N):
                if new_L[i + 1] > new_L[i]:
                    new_state |= (1 << i)
            
            transitions[state][char_code] = new_state
    
    # DP: dp[state] = number of ways to reach this state after processing some prefix of T
    dp = [0] * (1 << N)
    dp[0] = 1  # Initial state: all zeros
    
    for m in range(M):
        new_dp = [0] * (1 << N)
        for state in range(1 << N):
            if dp[state] == 0:
                continue
            for char_code in range(26):
                next_state = transitions[state][char_code]
                new_dp[next_state] = (new_dp[next_state] + dp[state]) % MOD
        dp = new_dp
    
    # Compute answers for each k
    ans = [0] * (N + 1)
    for state in range(1 << N):
        if dp[state] == 0:
            continue
        # Compute LCS length from state
        lcs_len = 0
        for i in range(N):
            if (state >> i) & 1:
                lcs_len += 1
        ans[lcs_len] = (ans[lcs_len] + dp[state]) % MOD
    
    print(' '.join(map(str, ans)))

solve()