import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2] if len(data) > 2 else ""
    s = [ord(ch) for ch in S]

    size = 1 << N

    # popcount for each mask
    pop = [0] * size
    for i in range(1, size):
        pop[i] = pop[i >> 1] + (i & 1)

    # For each mask, build the old LCS row f[0..N].
    # Bit i of the mask is f[i+1] - f[i].
    rows = []
    for mask in range(size):
        f = [0] * (N + 1)
        for i in range(N):
            f[i + 1] = f[i] + ((mask >> i) & 1)
        rows.append(f)

    # Precompute transitions.
    # Correct LCS row update when appending character c to the candidate string:
    # g[i+1] = max(f[i+1], g[i], f[i] + (S[i] == c))
    trans = []
    for mask in range(size):
        f = rows[mask]
        cnt = {}
        for code in range(97, 123):  # 'a'..'z'
            g = 0
            nm = 0
            for i in range(N):
                best = f[i + 1]
                if g > best:
                    best = g
                if s[i] == code:
                    cand = f[i] + 1
                    if cand > best:
                        best = cand

                if best > g:
                    nm |= 1 << i
                g = best

            cnt[nm] = cnt.get(nm, 0) + 1
        trans.append(list(cnt.items()))

    # DP over candidate string length.
    dp = [0] * size
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * size
        for mask, val in enumerate(dp):
            if val:
                for nm, ways in trans[mask]:
                    ndp[nm] = (ndp[nm] + val * ways) % MOD
        dp = ndp

    # Bucket final states by LCS length = popcount(mask).
    ans = [0] * (N + 1)
    for mask, val in enumerate(dp):
        if val:
            ans[pop[mask]] = (ans[pop[mask]] + val) % MOD

    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()