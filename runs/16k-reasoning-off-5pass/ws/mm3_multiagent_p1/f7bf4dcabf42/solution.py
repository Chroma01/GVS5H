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
    
    # initial state: dp[0..N] all zeros
    initial = tuple([0] * (N + 1))
    
    # BFS to collect all reachable states
    states = set()
    states.add(initial)
    queue = deque([initial])
    # Precompute S as list for faster access
    S_list = list(S)
    
    while queue:
        state = queue.popleft()
        dp = list(state)
        for ci in range(26):
            c = chr(ord('a') + ci)
            new_dp = dp[:]
            for i in range(1, N + 1):
                if S_list[i-1] == c:
                    new_dp[i] = max(new_dp[i], dp[i-1] + 1)
                new_dp[i] = max(new_dp[i], new_dp[i-1])
            new_state = tuple(new_dp)
            if new_state not in states:
                states.add(new_state)
                queue.append(new_state)
    
    # map states to indices
    state_list = list(states)
    state_to_idx = {s: i for i, s in enumerate(state_list)}
    num_states = len(state_list)
    
    # transition counts: trans[i][j] = number of characters that cause transition from i to j
    trans = [[0] * num_states for _ in range(num_states)]
    for state in state_list:
        idx_from = state_to_idx[state]
        dp = list(state)
        for ci in range(26):
            c = chr(ord('a') + ci)
            new_dp = dp[:]
            for i in range(1, N + 1):
                if S_list[i-1] == c:
                    new_dp[i] = max(new_dp[i], dp[i-1] + 1)
                new_dp[i] = max(new_dp[i], new_dp[i-1])
            idx_to = state_to_idx[tuple(new_dp)]
            trans[idx_from][idx_to] += 1
    
    # DP over M steps
    cur = [0] * num_states
    cur[state_to_idx[initial]] = 1
    for _ in range(M):
        nxt = [0] * num_states
        for i in range(num_states):
            if cur[i] == 0:
                continue
            ci = cur[i]
            row = trans[i]
            for j in range(num_states):
                cnt = row[j]
                if cnt:
                    nxt[j] = (nxt[j] + ci * cnt) % MOD
        cur = nxt
    
    # aggregate answers by last element of state
    ans = [0] * (N + 1)
    for idx, state in enumerate(state_list):
        k = state[N]
        ans[k] = (ans[k] + cur[idx]) % MOD
    
    print(' '.join(str(x) for x in ans))

if __name__ == "__main__":
    solve()