import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    pos = 0

    def rd():
        nonlocal pos
        v = data[pos]
        pos += 1
        return v

    H = int(rd()); W = int(rd())
    A = [[int(rd()) % MOD for _ in range(W)] for _ in range(H)]
    Q = int(rd()); sh = int(rd()); sw = int(rd())

    queries = []
    for _ in range(Q):
        d = rd().decode()
        a = int(rd()) % MOD
        queries.append((d, a))

    # Transpose if needed so that W = min(H, W) <= 447
    if W > H:
        A = [list(row) for row in zip(*A)]
        H, W = W, H
        sh, sw = sw, sh
        mp = {'U': 'L', 'L': 'U', 'D': 'R', 'R': 'D'}
        queries = [(mp[d], a) for d, a in queries]

    # P[h]: dp row h (length W), valid for h < frontier
    # S[h]: suffix functional (length W), valid for h >= frontier
    P = [None] * (H + 1)
    S = [None] * (H + 2)
    P[0] = [0] * W
    for h in range(1, H + 1):
        Ah = A[h - 1]
        Pm = P[h - 1]
        cur = [0] * W
        acc = 0
        for w in range(W):
            acc = Ah[w] * ((Pm[w] + acc) % MOD) % MOD
            cur[w] = acc
        P[h] = cur

    S[H] = [0] * (W - 1) + [1]
    for h in range(H - 1, 0, -1):
        Ah1 = A[h]  # row h+1 (0-indexed h)
        Sp = S[h + 1]
        cur = [0] * W
        acc = 0
        for k in range(W - 1, -1, -1):
            acc = Ah1[k] * ((Sp[k] + acc) % MOD) % MOD
            cur[k] = acc
        S[h] = cur

    f = sh
    r_cur, c_cur = sh, sw
    out = []
    dmap = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    for d, a in queries:
        dr, dc = dmap[d]
        r_cur += dr
        c_cur += dc
        r, c = r_cur, c_cur
        A[r - 1][c - 1] = a

        while f < r:
            Ah = A[f - 1]
            Pm = P[f - 1]
            cur = [0] * W
            acc = 0
            for w in range(W):
                acc = Ah[w] * ((Pm[w] + acc) % MOD) % MOD
                cur[w] = acc
            P[f] = cur
            f += 1
        while f > r:
            f -= 1
            Ah1 = A[f]  # row f+1 (0-indexed f)
            Sp = S[f + 1]
            cur = [0] * W
            acc = 0
            for k in range(W - 1, -1, -1):
                acc = Ah1[k] * ((Sp[k] + acc) % MOD) % MOD
                cur[k] = acc
            S[f] = cur

        Ah = A[r - 1]
        Pm = P[r - 1]
        Sr = S[r]
        acc = 0
        ans = 0
        for w in range(W):
            acc = Ah[w] * ((Pm[w] + acc) % MOD) % MOD
            ans = (ans + Sr[w] * acc) % MOD
        out.append(str(ans))

    sys.stdout.write("\n".join(out) + "\n")

main()