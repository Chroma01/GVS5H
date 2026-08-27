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

    # Precompute transitions.
    # State mask: bit i is 1 iff LCS DP row increases from position i to i+1.
    trans = []
    for mask in range(size):
        # Reconstruct the LCS DP row from the mask.
        row = [0] * (N + 1)
        cur = 0
        for i in range(N):
            if (mask >> i) & 1:
                cur += 1
            row[i + 1] = cur

        nxt_count = {}
        for c in range(26):
            new = [0] * (N + 1)

            # Correct recurrence for appending one character to the candidate string:
            # new[i] = max(old[i], new[i-1], old[i-1] + (S[i-1] == c))
            for i in range(1, N + 1):
                v = row[i]
                if new[i - 1] > v:
                    v = new[i - 1]
                if s[i - 1] == c:
                    t = row[i - 1] + 1
                    if t > v:
                        v = t
                new[i] = v

            # Convert the new row back to a mask.
            nm = 0
            prev = 0
            for i in range(1, N + 1):
                if new[i] > prev:
                    nm |= 1 << (i - 1)
                prev = new[i]

            nxt_count[nm] = nxt_count.get(nm, 0) + 1

        trans.append(list(nxt_count.items()))

    # DP over string length.
    dp = [0] * size
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * size
        for mask, val in enumerate(dp):
            if val:
                for nxt, mult in trans[mask]:
                    ndp[nxt] = (ndp[nxt] + val * mult) % MOD
        dp = ndp

    # Popcounts of all masks.
    pop = [0] * size
    for i in range(1, size):
        pop[i] = pop[i >> 1] + (i & 1)

    # Aggregate by LCS length.
    ans = [0] * (N + 1)
    for mask, val in enumerate(dp):
        if val:
            ans[pop[mask]] = (ans[pop[mask]] + val) % MOD

    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()