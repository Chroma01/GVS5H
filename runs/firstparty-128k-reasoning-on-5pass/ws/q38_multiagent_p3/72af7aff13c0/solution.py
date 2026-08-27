import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    H0 = int(next(it))
    W0 = int(next(it))
    A0 = [[int(next(it)) for _ in range(W0)] for __ in range(H0)]
    Q = int(next(it))
    sh = int(next(it)) - 1
    sw = int(next(it)) - 1
    orig_dirs = [0] * Q
    vals = [0] * Q
    cntL = cntR = cntU = cntD = 0
    for i in range(Q):
        d = next(it)[0]
        a = int(next(it))
        vals[i] = a
        if d == 76:      # L
            orig_dirs[i] = 0
            cntL += 1
        elif d == 82:    # R
            orig_dirs[i] = 1
            cntR += 1
        elif d == 85:    # U
            orig_dirs[i] = 2
            cntU += 1
        else:            # D
            orig_dirs[i] = 3
            cntD += 1
    del data, it

    V0 = cntU + cntD
    Hcnt0 = cntL + cntR
    cost0 = V0 * (W0 - 1) + Hcnt0
    cost1 = Hcnt0 * (H0 - 1) + V0
    if cost1 < cost0 or (cost1 == cost0 and H0 < W0):
        transposed = True
    else:
        transposed = False

    if transposed:
        H = W0
        W = H0
        A = [[A0[i][j] for i in range(H0)] for j in range(W0)]
        cur_r = sw
        cur_c = sh
        dirs = orig_dirs
    else:
        H = H0
        W = W0
        A = A0
        cur_r = sh
        cur_c = sw
        mp = (2, 3, 0, 1)
        dirs = [mp[od] for od in orig_dirs]
    # A0 no longer needed
    A0 = None
    orig_dirs = None

    Hm1 = H - 1
    Wm1 = W - 1
    mod = MOD

    F = [[0] * W for _ in range(H)]
    for i in range(H):
        Ai = A[i]
        Fi = F[i]
        if i == 0:
            left = Ai[0]
            Fi[0] = left
            for j in range(1, W):
                left = Ai[j] * left % mod
                Fi[j] = left
        else:
            Fprev = F[i - 1]
            left = Ai[0] * Fprev[0] % mod
            Fi[0] = left
            for j in range(1, W):
                s = Fprev[j] + left
                if s >= mod:
                    s -= mod
                left = Ai[j] * s % mod
                Fi[j] = left

    G = [[0] * W for _ in range(H)]
    for i in range(H - 1, -1, -1):
        Ai = A[i]
        Gi = G[i]
        if i == Hm1:
            right = Ai[Wm1]
            Gi[Wm1] = right
            for j in range(Wm1 - 1, -1, -1):
                right = Ai[j] * right % mod
                Gi[j] = right
        else:
            Gnext = G[i + 1]
            right = Ai[Wm1] * Gnext[Wm1] % mod
            Gi[Wm1] = right
            for j in range(Wm1 - 1, -1, -1):
                s = Gnext[j] + right
                if s >= mod:
                    s -= mod
                right = Ai[j] * s % mod
                Gi[j] = right

    ans = F[Hm1][Wm1]
    r = cur_r
    c = cur_c
    out = []
    append = out.append

    for idx in range(Q):
        d = dirs[idx]
        if d == 0:  # U
            Gr = G[r]
            Ar = A[r]
            if c:
                if r + 1 < H:
                    Gnext = G[r + 1]
                    right = Gr[c]
                    for j in range(c - 1, -1, -1):
                        s = Gnext[j] + right
                        if s >= mod:
                            s -= mod
                        right = Ar[j] * s % mod
                        Gr[j] = right
                else:
                    right = Gr[c]
                    for j in range(c - 1, -1, -1):
                        right = Ar[j] * right % mod
                        Gr[j] = right
            nr = r - 1
            Gn = G[nr]
            An = A[nr]
            if c < Wm1:
                Gbelow = G[r]
                right = An[Wm1] * Gbelow[Wm1] % mod
                Gn[Wm1] = right
                for j in range(Wm1 - 1, c, -1):
                    s = Gbelow[j] + right
                    if s >= mod:
                        s -= mod
                    right = An[j] * s % mod
                    Gn[j] = right
            r = nr
        elif d == 1:  # D
            Fr = F[r]
            Ar = A[r]
            if c < Wm1:
                if r:
                    Fprev = F[r - 1]
                    left = Fr[c]
                    for j in range(c + 1, W):
                        s = Fprev[j] + left
                        if s >= mod:
                            s -= mod
                        left = Ar[j] * s % mod
                        Fr[j] = left
                else:
                    left = Fr[c]
                    for j in range(c + 1, W):
                        left = Ar[j] * left % mod
                        Fr[j] = left
            nr = r + 1
            Fn = F[nr]
            An = A[nr]
            if c:
                Fabove = F[r]
                left = An[0] * Fabove[0] % mod
                Fn[0] = left
                for j in range(1, c):
                    s = Fabove[j] + left
                    if s >= mod:
                        s -= mod
                    left = An[j] * s % mod
                    Fn[j] = left
            r = nr
        elif d == 2:  # L
            j = c - 1
            Gr = G[r]
            Ar = A[r]
            s = Gr[j + 1]
            if r + 1 < H:
                s += G[r + 1][j]
                if s >= mod:
                    s -= mod
            Gr[j] = Ar[j] * s % mod
            c = j
        else:  # R
            j = c + 1
            Fr = F[r]
            Ar = A[r]
            s = Fr[j - 1]
            if r:
                s += F[r - 1][j]
                if s >= mod:
                    s -= mod
            Fr[j] = Ar[j] * s % mod
            c = j

        a = vals[idx]
        if r == 0 and c == 0:
            f_sum = 1
        else:
            f_sum = 0
            if r:
                f_sum = F[r - 1][c]
            if c:
                f_sum += F[r][c - 1]
                if f_sum >= mod:
                    f_sum -= mod
        if r == Hm1 and c == Wm1:
            g_sum = 1
        else:
            g_sum = 0
            if r + 1 < H:
                g_sum = G[r + 1][c]
            if c + 1 < W:
                g_sum += G[r][c + 1]
                if g_sum >= mod:
                    g_sum -= mod

        old = A[r][c]
        if old != a:
            if f_sum and g_sum:
                diff = a - old
                if diff < 0:
                    diff += mod
                ans = (ans + diff * f_sum % mod * g_sum) % mod
            A[r][c] = a
        F[r][c] = a * f_sum % mod
        G[r][c] = a * g_sum % mod
        append(str(ans))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()