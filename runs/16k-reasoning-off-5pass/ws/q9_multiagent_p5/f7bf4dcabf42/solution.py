import sys

# Increase recursion depth just in case
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
    # A state is a tuple (l0, l1, ..., lN) where li is the LCS length between S[0..i-1] and the generated string.
    # Constraints: 0 <= l0 <= l1 <= ... <= lN <= N and li <= i.
    
    valid_states = []
    
    def generate_states(idx, current_lcs):
        if idx == N + 1:
            valid_states.append(tuple(current_lcs))
            return
        
        lower = current_lcs[idx-1] if idx > 0 else 0
        upper = min(idx, N)
        
        for val in range(lower, upper + 1):
            current_lcs.append(val)
            generate_states(idx + 1, current_lcs)
            current_lcs.pop()
            
    generate_states(0, [0])
    
    # Map state to index
    state_to_id = {state: i for i, state in enumerate(valid_states)}
    num_states = len(valid_states)
    
    # Precompute transitions
    # trans[u][c] = v
    trans = [[0] * 26 for _ in range(num_states)]
    
    # Helper to compute next state given current state and char c
    def get_next_state(state, c):
        l = list(state)
        new_l = [0] * (N + 1)
        
        # Standard LCS update logic for the whole vector
        # new_l[i] = LCS(S[0..i-1], T + c)
        # Recurrence:
        # new_l[i] = max(l[i], new_l[i-1])
        # if S[i-1] == c: new_l[i] = max(new_l[i], l[i-1] + 1)
        
        for i in range(1, N + 1):
            val = max(l[i], new_l[i-1])
            if S[i-1] == chr(ord('a') + c):
                val = max(val, l[i-1] + 1)
            new_l[i] = val
            
        return tuple(new_l)

    # Build transition table
    for u_idx, state in enumerate(valid_states):
        for c in range(26):
            v_state = get_next_state(state, c)
            v_idx = state_to_id[v_state]
            trans[u_idx][c] = v_idx

    # DP
    start_state = tuple([0] * (N + 1))
    start_id = state_to_id[start_state]
    
    dp = [0] * num_states
    dp[start_id] = 1
    
    # Iterate M times
    for _ in range(M):
        new_dp = [0] * num_states
        for u in range(num_states):
            if dp[u] == 0:
                continue
            count = dp[u]
            for c in range(26):
                v = trans[u][c]
                new_dp[v] = (new_dp[v] + count) % MOD
        dp = new_dp

    # Aggregate results
    ans = [0] * (N + 1)
    for u in range(num_states):
        if dp[u] > 0:
            k = valid_states[u][N]
            ans[k] = (ans[k] + dp[u]) % MOD
            
    # Output
    print(*(ans))

if __name__ == '__main__':
    solve()