import sys

MOD = 998244353


def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2]

    size = 1 << N

    # Decode every bitmask into the corresponding LCS DP row.
    # If bit i is 1, then dp[i+1] - dp[i] == 1.
    rows = []
    for mask in range(size):
        row = [0] * (N + 1)
        v = 0
        for j in range(1, N + 1):
            if (mask >> (j - 1)) & 1:
                v += 1
            row[j] = v
        rows.append(row)

    # Precompute transitions.
    # transitions[mask] = list of (next_mask, number_of_letters)
    transitions = []
    for mask in range(size):
        row = rows[mask]
        cnt = {}

        for ci in range(26):
            c = chr(ord('a') + ci)

            # Standard LCS recurrence after appending character c:
            # new[j] = max(row[j], new[j-1], row[j-1] + (S[j-1] == c))
            new = [0] * (N + 1)
            for j in range(1, N + 1):
                best = row[j]
                if new[j - 1] > best:
                    best = new[j - 1]
                match = row[j - 1] + (1 if S[j - 1] == c else 0)
                if match > best:
                    best = match
                new[j] = best

            # Encode the new DP row back into a bitmask.
            nxt = 0
            for j in range(1, N + 1):
                if new[j] != new[j - 1]:
                    nxt |= 1 << (j - 1)

            cnt[nxt] = cnt.get(nxt, 0) + 1

        transitions.append(list(cnt.items()))

    # DP over the length of the generated string.
    dp = [0] * size
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * size
        for state, val in enumerate(dp):
            if val:
                for nxt, mult in transitions[state]:
                    ndp[nxt] += val * mult
        dp = [x % MOD for x in ndp]

    # Popcount of a mask equals the final LCS length.
    pop = [0] * size
    for mask in range(1, size):
        pop[mask] = pop[mask >> 1] + (mask & 1)

    ans = [0] * (N + 1)
    for mask, val in enumerate(dp):
        ans[pop[mask]] = (ans[pop[mask]] + val) % MOD

    print(' '.join(map(str, ans)))


if __name__ == "__main__":
    solve()