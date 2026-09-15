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
    s_codes = [ord(ch) for ch in S]

    # rows[mask][j] = LCS value at prefix length j for the DP row encoded by mask.
    rows = []
    for mask in range(states):
        row = [0] * (N + 1)
        v = 0
        for j in range(1, N + 1):
            if (mask >> (j - 1)) & 1:
                v += 1
            row[j] = v
        rows.append(row)

    # next_state[mask][c] = mask after appending character c.
    next_state = [[0] * 26 for _ in range(states)]

    for mask in range(states):
        old = rows[mask]
        for ci in range(26):
            code = 97 + ci
            new_prev = 0
            new_mask = 0

            for j in range(1, N + 1):
                best = old[j]
                if new_prev > best:
                    best = new_prev

                if code == s_codes[j - 1]:
                    cand = old[j - 1] + 1
                    if cand > best:
                        best = cand

                if best > new_prev:
                    new_mask |= 1 << (j - 1)

                new_prev = best

            next_state[mask][ci] = new_mask

    # DP over automaton states.
    cur = [0] * states
    cur[0] = 1

    for _ in range(M):
        nxt = [0] * states
        for mask, val in enumerate(cur):
            if val == 0:
                continue
            for ns in next_state[mask]:
                x = nxt[ns] + val
                if x >= MOD:
                    x -= MOD
                nxt[ns] = x
        cur = nxt

    # Aggregate by final LCS length = popcount(mask).
    ans = [0] * (N + 1)
    for mask, val in enumerate(cur):
        if val == 0:
            continue
        k = mask.bit_count()
        x = ans[k] + val
        if x >= MOD:
            x -= MOD
        ans[k] = x

    print(*ans)

if __name__ == "__main__":
    solve()