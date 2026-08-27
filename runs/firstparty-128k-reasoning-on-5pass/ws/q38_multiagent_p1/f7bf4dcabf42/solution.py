import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2]

    size = 1 << N

    pop = [0] * size
    for m in range(1, size):
        pop[m] = pop[m >> 1] + (m & 1)

    pref = [(1 << j) - 1 for j in range(N + 1)]
    s_idx = [ord(ch) - 97 for ch in S]

    trans = [[0] * 26 for _ in range(size)]

    for mask in range(size):
        old = [0] * (N + 1)
        for j in range(1, N + 1):
            old[j] = pop[mask & pref[j]]

        for c in range(26):
            next_mask = 0
            prev = 0  # new[j-1]

            for j in range(1, N + 1):
                if s_idx[j - 1] == c:
                    v = old[j]
                    if prev > v:
                        v = prev
                    cand = old[j - 1] + 1
                    if cand > v:
                        v = cand
                else:
                    v = old[j]
                    if prev > v:
                        v = prev

                if v > prev:
                    next_mask |= 1 << (j - 1)
                prev = v

            trans[mask][c] = next_mask

    cnt = [0] * size
    cnt[0] = 1

    for _ in range(M):
        nxt = [0] * size
        for mask, val in enumerate(cnt):
            if val:
                for nm in trans[mask]:
                    nxt[nm] += val
        for i in range(size):
            nxt[i] %= MOD
        cnt = nxt

    ans = [0] * (N + 1)
    for mask, val in enumerate(cnt):
        if val:
            ans[pop[mask]] = (ans[pop[mask]] + val) % MOD

    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()