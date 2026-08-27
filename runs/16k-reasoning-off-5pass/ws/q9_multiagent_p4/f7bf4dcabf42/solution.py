import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

def solve():
    # Read input
    try:
        input_data = sys.stdin.read().split()
    except Exception:
        return

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

    # Generate all valid states
    # A state is a tuple (v0, v1, ..., vN) where 0 <= v0 <= v1 <= ... <= vN <= N
    # v_i represents the LCS length between S[:i] and the current prefix of the generated string T.
    
    states = []
    
    def generate_states(current_seq, start_val):
        if len(current_seq) == N + 1:
            states.append(tuple(current_seq))
            return
        for v in range(start_val, N + 1):
            current_seq.append(v)
            generate_states(current_seq, v)
            current_seq.pop()
            
    generate_states([], 0)
    
    num_states = len(states)
    state_to_idx = {s: i for i, s in enumerate(states)}
    idx_to_state = {i: s for i, s in enumerate(states)}
    
    # Precompute transitions
    # trans[char_code][u] = v
    # char_code: 0-25 corresponding to 'a'-'z'
    trans = [[0] * num_states for _ in range(26)]
    
    for char_code in range(26):
        c = chr(ord('a') + char_code)
        for u in range(num_states):
            s = idx_to_state[u]
            # s is (v0, v1, ..., vN)
            # Compute new state when appending character c to T
            # Logic: new_v[i] = LCS(S[:i], T_old + c)
            # If S[i-1] == c, new_v[i] = max(v[i], v[i-1] + 1)
            # Else, new_v[i] = v[i]
            
            # We can compute this in-place or create a new list
            new_s = list(s)
            # v0 is always 0, so we start from i=1
            for i in range(1, N + 1):
                if S[i-1] == c:
                    new_s[i] = max(s[i], s[i-1] + 1)
                else:
                    new_s[i] = s[i]
            
            v = tuple(new_s)
            trans[char_code][u] = state_to_idx[v]

    # DP
    # dp[u] = number of ways to reach state u after processing some prefix of T
    # Initialize: state (0, 0, ..., 0) with count 1
    start_state = tuple([0] * (N + 1))
    start_idx = state_to_idx[start_state]
    
    dp = [0] * num_states
    dp[start_idx] = 1
    
    for _ in range(M):
        new_dp = [0] * num_states
        for u in range(num_states):
            if dp[u] == 0:
                continue
            count = dp[u]
            for char_code in range(26):
                v = trans[char_code][u]
                new_dp[v] = (new_dp[v] + count) % MOD
        dp = new_dp
        
    # Aggregate results
    # ans[k] = sum of dp[u] for all u where u[N] == k
    ans = [0] * (N + 1)
    for u in range(num_states):
        s = idx_to_state[u]
        k = s[N]
        ans[k] = (ans[k] + dp[u]) % MOD
        
    print(*(ans))

if __name__ == '__main__':
    solve()