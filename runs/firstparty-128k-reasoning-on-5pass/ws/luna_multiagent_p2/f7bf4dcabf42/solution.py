import sys

MOD = 998244353
ALPHABET = 26


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2].decode()

    state_count = 1 << N

    # Decode every profile mask into its corresponding LCS row.
    rows = []
    for mask in range(state_count):
        row = [0] * (N + 1)
        value = 0
        for i in range(1, N + 1):
            value += (mask >> (i - 1)) & 1
            row[i] = value
        rows.append(row)

    # Aggregate transitions for each state. Different letters can lead
    # to the same next profile.
    transitions = [[] for _ in range(state_count)]
    for mask in range(state_count):
        old = rows[mask]
        counts = {}
        for c in range(ALPHABET):
            prev_new = 0
            next_mask = 0
            for i in range(1, N + 1):
                if ord(S[i - 1]) - 97 == c:
                    value = old[i - 1] + 1
                else:
                    value = max(old[i], prev_new)

                if value - prev_new:
                    next_mask |= 1 << (i - 1)
                prev_new = value

            counts[next_mask] = counts.get(next_mask, 0) + 1

        transitions[mask] = list(counts.items())

    dp = [0] * state_count
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * state_count
        for state, ways in enumerate(dp):
            if ways:
                for nxt, multiplicity in transitions[state]:
                    ndp[nxt] = (ndp[nxt] + ways * multiplicity) % MOD
        dp = ndp

    answer = [0] * (N + 1)
    for state, ways in enumerate(dp):
        answer[state.bit_count()] = (answer[state.bit_count()] + ways) % MOD

    print(*answer)


if __name__ == "__main__":
    solve()