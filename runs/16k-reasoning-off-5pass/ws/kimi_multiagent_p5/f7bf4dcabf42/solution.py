import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1])
    S = data[2].strip()

    # State: bitmask of N bits, bit i = d[i+1] - d[i] where d is the LCS DP row.
    # d[i] = popcount of the lowest i bits.
    index = {0: 0}
    states = [0]          # list of masks
    trans = []            # trans[state_idx][26] -> state_idx

    def popcount(x):
        return bin(x).count("1")

    def step(mask, c):
        # d[i] = LCS of processed prefix of T with S[:i]
        # new[i] = d[i-1] + 1 if S[i-1] == c else max(d[i], new[i-1])
        d = [0] * (N + 1)
        for i in range(1, N + 1):
            d[i] = d[i - 1] + ((mask >> (i - 1)) & 1)
        new = [0] * (N + 1)
        nmask = 0
        for i in range(1, N + 1):
            if S[i - 1] == c:
                new[i] = d[i - 1] + 1
            else:
                a = d[i]
                b = new[i - 1]
                new[i] = a if a >= b else b
            if new[i] > new[i - 1]:
                nmask |= (1 << (i - 1))
        return nmask

    # BFS over reachable states, computing transitions lazily
    head = 0
    while head < len(states):
        mask = states[head]
        row = [0] * 26
        for ci in range(26):
            c = chr(ord('a') + ci)
            nm = step(mask, c)
            if nm not in index:
                index[nm] = len(states)
                states.append(nm)
            row[ci] = index[nm]
        trans.append(row)
        head += 1

    nstates = len(states)
    dp = [0] * nstates
    dp[0] = 1
    for _ in range(M):
        ndp = [0] * nstates
        for s in range(nstates):
            v = dp[s]
            if v:
                tr = trans[s]
                for ci in range(26):
                    ndp[tr[ci]] = (ndp[tr[ci]] + v) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for s in range(nstates):
        k = popcount(states[s])
        ans[k] = (ans[k] + dp[s]) % MOD

    sys.stdout.write(" ".join(map(str, ans)) + "\n")

main()