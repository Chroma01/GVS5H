import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2]

    s = [ord(ch) - 97 for ch in S]
    size = 1 << N

    pop = [0] * size
    for i in range(1, size):
        pop[i] = pop[i >> 1] + (i & 1)

    trans = []
    for mask in range(size):
        old = [0] * (N + 1)
        for i in range(N):
            old[i + 1] = old[i] + ((mask >> i) & 1)

        counts = {}
        for c in range(26):
            new = [0] * (N + 1)
            for j in range(1, N + 1):
                best = new[j - 1]
                if old[j] > best:
                    best = old[j]
                if s[j - 1] == c:
                    v = old[j - 1] + 1
                    if v > best:
                        best = v
                new[j] = best

            nm = 0
            for i in range(N):
                if new[i + 1] > new[i]:
                    nm |= 1 << i

            counts[nm] = counts.get(nm, 0) + 1

        trans.append(list(counts.items()))

    dp = [0] * size
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * size
        for mask, val in enumerate(dp):
            if val:
                for nm, cnt in trans[mask]:
                    ndp[nm] += val * cnt
        dp = [x % MOD for x in ndp]

    ans = [0] * (N + 1)
    for mask, val in enumerate(dp):
        if val:
            ans[pop[mask]] = (ans[pop[mask]] + val) % MOD

    print(' '.join(map(str, ans)))

if __name__ == "__main__":
    main()