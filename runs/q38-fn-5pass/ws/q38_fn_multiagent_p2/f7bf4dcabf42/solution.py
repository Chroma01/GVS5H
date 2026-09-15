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
    letters = [chr(ord('a') + i) for i in range(26)]

    # trans[mask][c] = next mask after appending letter c to a prefix
    # whose LCS DP row against S is represented by mask.
    trans = []
    for mask in range(size):
        # Reconstruct the LCS DP row from the bitmask.
        # old[j] = LCS(processed prefix, S[:j])
        old = [0] * (N + 1)
        for j in range(1, N + 1):
            old[j] = old[j - 1] + ((mask >> (j - 1)) & 1)

        nxt = [0] * 26
        for ci, c in enumerate(letters):
            new = [0] * (N + 1)
            for j in range(1, N + 1):
                if S[j - 1] == c:
                    new[j] = max(old[j], new[j - 1], old[j - 1] + 1)
                else:
                    new[j] = max(old[j], new[j - 1])

            # Convert the new DP row back to a bitmask.
            nm = 0
            for j in range(1, N + 1):
                if new[j] != new[j - 1]:
                    nm |= 1 << (j - 1)
            nxt[ci] = nm

        trans.append(nxt)

    # popcount for each state mask
    pop = [0] * size
    for mask in range(1, size):
        pop[mask] = pop[mask >> 1] + (mask & 1)

    # DP over the length of the unknown string.
    dp = [0] * size
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * size
        for mask, val in enumerate(dp):
            if val == 0:
                continue
            for nm in trans[mask]:
                x = ndp[nm] + val
                if x >= MOD:
                    x -= MOD
                ndp[nm] = x
        dp = ndp

    # Group final states by LCS length, which is the popcount of the mask.
    ans = [0] * (N + 1)
    for mask, val in enumerate(dp):
        k = pop[mask]
        ans[k] += val
        if ans[k] >= MOD:
            ans[k] -= MOD

    print(' '.join(map(str, ans)))


if __name__ == "__main__":
    main()