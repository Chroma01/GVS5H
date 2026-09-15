import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    M = int(data[1])
    S = data[2].decode()
    MOD = 998244353

    size = 1 << N
    # mask bit (i-1) = d[i] - d[i-1], where d[i] = LCS(S[0:i], T) for the
    # already-scanned prefix T. d[0]=0, final LCS = popcount(mask).
    # Appending char c: e[i] = d'[i]-d[i] in {0,1}.
    #   if bit_i==1: e[i]=0
    #   else:        e[i]=max(e[i-1], [S[i-1]==c])
    # new bit_i = bit_i + e[i] - e[i-1]
    trans = [[0] * 26 for _ in range(size)]
    for mask in range(size):
        tr = trans[mask]
        for c in range(26):
            ch = chr(97 + c)
            e_prev = 0
            nm = 0
            for i in range(1, N + 1):
                bit = (mask >> (i - 1)) & 1
                if bit == 1:
                    e_i = 0
                else:
                    eq = 1 if S[i - 1] == ch else 0
                    e_i = e_prev if e_prev > eq else eq
                nm |= (bit + e_i - e_prev) << (i - 1)
                e_prev = e_i
            tr[c] = nm

    # Aggregate letters that share the same destination mask for speed.
    agg = []
    for mask in range(size):
        cnt = {}
        for c in range(26):
            t = trans[mask][c]
            cnt[t] = cnt.get(t, 0) + 1
        agg.append(list(cnt.items()))

    dp = [0] * size
    dp[0] = 1
    for _ in range(M):
        ndp = [0] * size
        for mask in range(size):
            v = dp[mask]
            if v:
                for t, cn in agg[mask]:
                    ndp[t] = (ndp[t] + v * cn) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for mask in range(size):
        pc = bin(mask).count('1')
        ans[pc] = (ans[pc] + dp[mask]) % MOD

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

main()