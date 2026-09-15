import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2]

    states = 1 << N

    # fvals[mask][j] = LCS value at prefix length j of S
    # for the row encoded by mask.
    fvals = []
    for mask in range(states):
        f = [0] * (N + 1)
        for j in range(1, N + 1):
            f[j] = f[j - 1] + ((mask >> (j - 1)) & 1)
        fvals.append(f)

    letters = [chr(ord('a') + i) for i in range(26)]

    # trans[mask] = list of (next_mask, number_of_letters)
    trans = []
    for mask in range(states):
        f = fvals[mask]
        counts = {}

        for ch in letters:
            new_mask = 0
            prev_g = 0

            for j in range(1, N + 1):
                # Standard LCS row update:
                # g[j] = max(f[j], g[j-1], f[j-1] + 1 if ch == S[j-1])
                v = f[j]
                if prev_g > v:
                    v = prev_g

                if ch == S[j - 1]:
                    cand = f[j - 1] + 1
                    if cand > v:
                        v = cand

                if v != prev_g:
                    new_mask |= 1 << (j - 1)

                prev_g = v

            counts[new_mask] = counts.get(new_mask, 0) + 1

        trans.append(list(counts.items()))

    dp = [0] * states
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * states
        for mask, val in enumerate(dp):
            if val == 0:
                continue
            for nxt, cnt in trans[mask]:
                ndp[nxt] = (ndp[nxt] + val * cnt) % MOD
        dp = ndp

    pop = [0] * states
    for mask in range(1, states):
        pop[mask] = pop[mask >> 1] + (mask & 1)

    ans = [0] * (N + 1)
    for mask, val in enumerate(dp):
        k = pop[mask]
        ans[k] = (ans[k] + val) % MOD

    print(*ans)

if __name__ == "__main__":
    solve()