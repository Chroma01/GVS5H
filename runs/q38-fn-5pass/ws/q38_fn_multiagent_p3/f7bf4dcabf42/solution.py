import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2]

    MOD = 998244353
    size = 1 << N

    s_codes = [ord(ch) - 97 for ch in S]

    # rows[mask] is the LCS DP row dp[0..N] represented by mask.
    # bit i is 1 iff dp[i+1] - dp[i] == 1.
    rows = []
    for mask in range(size):
        row = [0] * (N + 1)
        for i in range(N):
            row[i + 1] = row[i] + ((mask >> i) & 1)
        rows.append(row)

    # Precompute transitions.  For each state, aggregate characters that
    # lead to the same next state.
    trans_counts = []
    for mask in range(size):
        row = rows[mask]
        counts = {}

        for c in range(26):
            next_mask = 0
            prev_new = 0

            for j in range(1, N + 1):
                # Standard LCS row update when appending character c:
                # new[j] = max(new[j-1], old[j], old[j-1]+1 if S[j-1]==c)
                v = prev_new if prev_new >= row[j] else row[j]

                if s_codes[j - 1] == c:
                    cand = row[j - 1] + 1
                    if cand > v:
                        v = cand

                if v != prev_new:
                    next_mask |= 1 << (j - 1)

                prev_new = v

            counts[next_mask] = counts.get(next_mask, 0) + 1

        trans_counts.append(tuple(counts.items()))

    # popcount for each mask, equal to the current LCS length.
    pop = [0] * size
    for mask in range(1, size):
        pop[mask] = pop[mask >> 1] + (mask & 1)

    # DP over the length of the generated string T.
    dp = [0] * size
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * size
        for mask, val in enumerate(dp):
            if val == 0:
                continue
            for nxt, cnt in trans_counts[mask]:
                ndp[nxt] = (ndp[nxt] + val * cnt) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for mask, val in enumerate(dp):
        k = pop[mask]
        ans[k] = (ans[k] + val) % MOD

    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()