import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    M = int(data[1])
    S = data[2].decode()

    full = (1 << N) - 1

    # match_mask[c] has bit i set iff S[i] == chr(ord('a') + c).
    match_mask = [0] * 26
    for i, ch in enumerate(S):
        match_mask[ord(ch) - ord('a')] |= 1 << i

    # LCS row differences are represented by an N-bit mask.
    # If D is the old difference mask and A is the match mask, then:
    #   X = D | A
    #   Y = ((D << 1) | 1) mod 2^N
    #   D' = X & ~(X - Y)
    transitions = [[0] * 26 for _ in range(1 << N)]
    for d in range(1 << N):
        for c in range(26):
            x = d | match_mask[c]
            y = ((d << 1) | 1) & full
            subtraction = (x - y) & full
            transitions[d][c] = x & (full ^ subtraction)

    dp = [0] * (1 << N)
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * (1 << N)
        for state, count in enumerate(dp):
            if count == 0:
                continue
            for c in range(26):
                nxt = transitions[state][c]
                ndp[nxt] = (ndp[nxt] + count) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for state, count in enumerate(dp):
        ans[state.bit_count()] = (ans[state.bit_count()] + count) % MOD

    print(*ans)

if __name__ == "__main__":
    solve()