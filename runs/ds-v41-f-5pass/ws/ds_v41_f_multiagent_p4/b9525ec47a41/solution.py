import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    s = data[1] if len(data) > 1 else ''

    # Precompute composition table for relations (4-bit masks)
    # relation mask: bit p*2+q set if (p,q) in R
    def compose(R, T):
        res = 0
        for p in (0, 1):
            for q in (0, 1):
                if R & (1 << (p * 2 + q)):
                    for q2 in (0, 1):
                        if T & (1 << (q * 2 + q2)):
                            res |= 1 << (p * 2 + q2)
        return res

    comp = [[0] * 16 for _ in range(16)]
    for R in range(16):
        for T in range(16):
            comp[R][T] = compose(R, T)

    # Transition relations T_s[d] as 4-bit masks on (q, q')
    T0 = {0: 2, 1: 9, 2: 4}
    T1 = {0: 2, 1: 11, 2: 13, 3: 4}

    start = 9  # identity relation {(0,0),(1,1)}
    reachable = set()
    stack = [start]
    while stack:
        R = stack.pop()
        if R in reachable:
            continue
        reachable.add(R)
        for T in T0.values():
            nxt = comp[R][T]
            if nxt != 0:
                stack.append(nxt)
        for T in T1.values():
            nxt = comp[R][T]
            if nxt != 0:
                stack.append(nxt)

    state_list = sorted(reachable)
    idx = {R: i for i, R in enumerate(state_list)}
    K = len(state_list)

    trans_flat0 = []
    trans_flat1 = []
    for R in state_list:
        i = idx[R]
        cnt = {}
        for d, T in T0.items():
            nxt = comp[R][T]
            if nxt != 0:
                cnt[nxt] = cnt.get(nxt, 0) + 1
        for nxt, c in cnt.items():
            trans_flat0.append((i, idx[nxt], c))
        cnt = {}
        for d, T in T1.items():
            nxt = comp[R][T]
            if nxt != 0:
                cnt[nxt] = cnt.get(nxt, 0) + 1
        for nxt, c in cnt.items():
            trans_flat1.append((i, idx[nxt], c))

    dp = [0] * K
    dp[idx[start]] = 1

    for ch in s:
        ndp = [0] * K
        if ch == '0':
            for i, nxt, c in trans_flat0:
                ndp[nxt] += dp[i] * c
        else:
            for i, nxt, c in trans_flat1:
                ndp[nxt] += dp[i] * c
        dp = [x % MOD for x in ndp]

    ans = 0
    for i, R in enumerate(state_list):
        if R & 9:  # contains (0,0) or (1,1)
            ans = (ans + dp[i]) % MOD
    print(ans)

if __name__ == "__main__":
    solve()