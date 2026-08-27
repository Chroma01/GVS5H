import sys
from collections import deque

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1])
    S = data[2].strip()

    # State: bitmask of length N. Bit i set iff d[i+1] - d[i] == 1,
    # where d[i] = LCS(S[:i], processed prefix of T).
    # d[0] = 0, d nondecreasing, increments in {0,1}; LCS value = popcount(mask).

    # Decode mask -> row values d[0..N]
    def decode(mask):
        d = [0] * (N + 1)
        v = 0
        for i in range(N):
            if (mask >> i) & 1:
                v += 1
            d[i + 1] = v
        return d

    # Encode row values d[0..N] -> mask
    def encode(d):
        mask = 0
        for i in range(N):
            if d[i + 1] > d[i]:
                mask |= (1 << i)
        return mask

    # Transition: given current row d (against processed prefix), append char c.
    # Standard LCS DP row update:
    #   nd[0] = 0
    #   nd[i] = max(d[i], nd[i-1])
    #   if S[i-1] == c: nd[i] = max(nd[i], d[i-1] + 1)
    def trans(mask, c):
        d = decode(mask)
        nd = [0] * (N + 1)
        for i in range(1, N + 1):
            v = d[i] if d[i] >= nd[i - 1] else nd[i - 1]
            if S[i - 1] == c:
                alt = d[i - 1] + 1
                if alt > v:
                    v = alt
            nd[i] = v
        return encode(nd)

    # BFS over reachable states from mask 0
    start = 0
    state_id = {start: 0}
    states = [start]
    q = deque([start])
    # trans_table[state_index][letter 0..25] = next state mask
    trans_table = []
    while q:
        m = q.popleft()
        row = [0] * 26
        for c in range(26):
            nm = trans(m, chr(ord('a') + c))
            row[c] = nm
            if nm not in state_id:
                state_id[nm] = len(states)
                states.append(nm)
                q.append(nm)
        trans_table.append(row)

    Z = len(states)
    # For each state, aggregate: list of (next_state_index, multiplicity of letters)
    agg = []
    for si in range(Z):
        cnt = {}
        for c in range(26):
            nm = trans_table[si][c]
            ni = state_id[nm]
            cnt[ni] = cnt.get(ni, 0) + 1
        agg.append(list(cnt.items()))

    # DP over M steps
    dp = [0] * Z
    dp[state_id[start]] = 1
    for _ in range(M):
        ndp = [0] * Z
        for si in range(Z):
            v = dp[si]
            if v:
                for ni, mult in agg[si]:
                    ndp[ni] = (ndp[ni] + v * mult) % MOD
        dp = ndp

    # Aggregate by popcount (LCS value)
    ans = [0] * (N + 1)
    for si in range(Z):
        if dp[si]:
            k = bin(states[si]).count('1')
            ans[k] = (ans[k] + dp[si]) % MOD

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

main()