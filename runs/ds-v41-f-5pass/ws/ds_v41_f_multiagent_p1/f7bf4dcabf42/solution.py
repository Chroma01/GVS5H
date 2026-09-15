import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2].decode()

    # Distinct letters occurring in S; all other letters share the same transition.
    distinct = []
    seen = set()
    for ch in S:
        if ch not in seen:
            seen.add(ch)
            distinct.append(ch)
    D = len(distinct)
    non = 26 - D

    states = 1 << N

    # popcount of each mask = current LCS length
    pop = [0] * states
    for st in range(1, states):
        pop[st] = pop[st >> 1] + (st & 1)

    # Recover the LCS DP row from a frontier mask.
    rows = [[0] * (N + 1) for _ in range(states)]
    for mask in range(states):
        row = rows[mask]
        for i in range(1, N + 1):
            row[i] = row[i - 1] + ((mask >> (i - 1)) & 1)

    # Precompute transitions: for each state and each letter of S.
    trans = [[0] * D for _ in range(states)]
    for mask in range(states):
        old = rows[mask]
        for ci, ch in enumerate(distinct):
            new = [0] * (N + 1)
            for i in range(1, N + 1):
                v = new[i - 1]
                if old[i] > v:
                    v = old[i]
                if S[i - 1] == ch:
                    cand = old[i - 1] + 1
                    if cand > v:
                        v = cand
                new[i] = v
            nm = 0
            for i in range(1, N + 1):
                if new[i] > new[i - 1]:
                    nm |= 1 << (i - 1)
            trans[mask][ci] = nm

    counts = [0] * states
    counts[0] = 1

    for _ in range(M):
        nc = [0] * states
        for st in range(states):
            cnt = counts[st]
            if cnt == 0:
                continue
            if non:  # letters not in S keep the frontier unchanged
                nc[st] = (nc[st] + cnt * non) % MOD
            for ci in range(D):
                ns = trans[st][ci]
                nc[ns] = (nc[ns] + cnt) % MOD
        counts = nc

    ans = [0] * (N + 1)
    for st in range(states):
        cnt = counts[st]
        if cnt:
            ans[pop[st]] = (ans[pop[st]] + cnt) % MOD

    sys.stdout.write(" ".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    main()