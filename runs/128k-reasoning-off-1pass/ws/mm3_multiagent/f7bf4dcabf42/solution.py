import sys
from collections import deque

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2].strip()
    
    # State is the vector L[0..N] where L[i] = LCS length between S[0..i) and processed prefix.
    # We enumerate all reachable states via BFS.
    initial_state = tuple([0] * (N + 1))
    states = set()
    states.add(initial_state)
    queue = deque([initial_state])
    while queue:
        state = queue.popleft()
        for c in range(26):
            ch = chr(ord('a') + c)
            L = list(state)
            # Update LCS DP: scan from right to left
            for i in range(N - 1, -1, -1):
                if S[i] == ch and L[i] + 1 > L[i + 1]:
                    L[i + 1] = L[i] + 1
            new_state = tuple(L)
            if new_state not in states:
                states.add(new_state)
                queue.append(new_state)
    
    state_list = list(states)
    state_to_idx = {s: i for i, s in enumerate(state_list)}
    n_states = len(state_list)
    
    # Precompute transitions
    trans = [[0] * 26 for _ in range(n_states)]
    for idx, state in enumerate(state_list):
        for c in range(26):
            ch = chr(ord('a') + c)
            L = list(state)
            for i in range(N - 1, -1, -1):
                if S[i] == ch and L[i] + 1 > L[i + 1]:
                    L[i + 1] = L[i] + 1
            trans[idx][c] = state_to_idx[tuple(L)]
    
    # DP over M steps
    dp = [0] * n_states
    dp[state_to_idx[initial_state]] = 1
    for _ in range(M):
        new_dp = [0] * n_states
        for idx in range(n_states):
            if dp[idx]:
                val = dp[idx]
                for c in range(26):
                    new_dp[trans[idx][c]] = (new_dp[trans[idx][c]] + val) % MOD
        dp = new_dp
    
    # Aggregate answers by final LCS length
    ans = [0] * (N + 1)
    for idx, state in enumerate(state_list):
        k = state[N]
        ans[k] = (ans[k] + dp[idx]) % MOD
    
    print(' '.join(str(ans[k]) for k in range(N + 1)))

if __name__ == "__main__":
    solve()