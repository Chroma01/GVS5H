import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2]
    s_vals = list(S)

    size = 1 << N

    pop = [0] * size
    for i in range(1, size):
        pop[i] = pop[i >> 1] + (i & 1)

    rows = []
    for mask in range(size):
        row = [0] * (N + 1)
        for j in range(1, N + 1):
            row[j] = row[j - 1] + ((mask >> (j - 1)) & 1)
        rows.append(row)

    trans = []
    for mask in range(size):
        row = rows[mask]
        t = []
        for c in range(97, 123):
            new = [0] * (N + 1)
            for j in range(1, N + 1):
                best = row[j]
                if new[j - 1] > best:
                    best = new[j - 1]
                if c == s_vals[j - 1]:
                    cand = row[j - 1] + 1
                    if cand > best:
                        best = cand
                new[j] = best

            nm = 0
            for j in range(1, N + 1):
                if new[j] > new[j - 1]:
                    nm |= 1 << (j - 1)
            t.append(nm)
        trans.append(t)

    dp = [0] * size
    dp[0] = 1
    mod = MOD

    for _ in range(M):
        ndp = [0] * size
        for mask, val in enumerate(dp):
            if val:
                for nm in trans[mask]:
                    x = ndp[nm] + val
                    if x >= mod:
                        x -= mod
                    ndp[nm] = x
        dp = ndp

    ans = [0] * (N + 1)
    for mask, val in enumerate(dp):
        if val:
            k = pop[mask]
            x = ans[k] + val
            if x >= mod:
                x -= mod
            ans[k] = x

    print(' '.join(map(str, ans)))

if __name__ == "__main__":
    main()