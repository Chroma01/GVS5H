import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1])
    S = data[2]

    # Decode mask -> dp row: dp[0]=0, dp[j] = dp[j-1] + bit(j-1)
    # Transition: given mask and char c, compute new mask.
    # ndp[j] = max(dp[j], ndp[j-1], dp[j-1] + (S[j-1]==c))
    # Encode new mask similarly.

    # Precompute transitions lazily via memoization
    trans = {}  # (mask, ci) -> new mask

    def get_trans(mask, ci):
        key = (mask, ci)
        res = trans.get(key)
        if res is not None:
            return res
        # decode dp row
        dp = [0] * (N + 1)
        for j in range(1, N + 1):
            dp[j] = dp[j - 1] + ((mask >> (j - 1)) & 1)
        ndp = [0] * (N + 1)
        c = chr(ord('a') + ci)
        newmask = 0
        for j in range(1, N + 1):
            v = dp[j]
            if ndp[j - 1] > v:
                v = ndp[j - 1]
            match = dp[j - 1] + (1 if S[j - 1] == c else 0)
            if match > v:
                v = match
            ndp[j] = v
            if v > ndp[j - 1]:
                newmask |= (1 << (j - 1))
        trans[key] = newmask
        return newmask

    # DP over positions
    f = {0: 1}
    for _ in range(M):
        g = {}
        for mask, cnt in f.items():
            for ci in range(26):
                nm = get_trans(mask, ci)
                g[nm] = (g.get(nm, 0) + cnt) % MOD
        f = g

    ans = [0] * (N + 1)
    for mask, cnt in f.items():
        k = bin(mask).count('1')
        ans[k] = (ans[k] + cnt) % MOD

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

main()