import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2].strip()
    MOD = 998244353
    size = 1 << N
    chars = sorted(set(S))
    idw = 26 - len(chars)

    # decode masks
    dps = []
    for mask in range(size):
        dp = [0] * (N + 1)
        for j in range(1, N + 1):
            dp[j] = dp[j - 1] + ((mask >> (j - 1)) & 1)
        dps.append(dp)

    # build transitions
    groups = []
    for mask in range(size):
        dp = dps[mask]
        d = {}
        if idw > 0:
            d[mask] = idw
        for c in chars:
            new = [0] * (N + 1)
            for j in range(1, N + 1):
                a = new[j - 1]
                b = dp[j]
                e = dp[j - 1] + (1 if S[j - 1] == c else 0)
                v = a
                if b > v: v = b
                if e > v: v = e
                new[j] = v
            nm = 0
            for j in range(1, N + 1):
                if new[j] - new[j - 1] == 1:
                    nm |= 1 << (j - 1)
            d[nm] = d.get(nm, 0) + 1
        groups.append(list(d.items()))

    cur = [0] * size
    cur[0] = 1
    for _ in range(M):
        new = [0] * size
        for mask in range(size):
            v = cur[mask]
            if v:
                for (t, w) in groups[mask]:
                    new[t] = (new[t] + v * w) % MOD
        cur = new

    ans = [0] * (N + 1)
    for mask in range(size):
        if cur[mask]:
            ans[bin(mask).count('1')] = (ans[bin(mask).count('1')] + cur[mask]) % MOD
    sys.stdout.write(' '.join(map(str, ans)) + '\n')

main()