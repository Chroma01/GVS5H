import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    to_int = int
    H0 = to_int(data[0])
    W0 = to_int(data[1])

    # Transpose if needed so that H is the smaller dimension.
    if H0 <= W0:
        H, W = H0, W0
        trans = False
    else:
        H, W = W0, H0
        trans = True

    D = H + W - 1
    S = H + 2          # stride per diagonal: sentinel at h=-1 and h=H
    S1 = S + 1
    M = D * S

    A = [0] * M
    tok = 2

    # Fill grid values into diagonal-major flat array.
    if not trans:
        for h in range(H):
            idx = h * S + h + 1
            for _ in range(W):
                A[idx] = to_int(data[tok])
                tok += 1
                idx += S
    else:
        step = S1
        # Original rows = W, original columns = H.
        for h0 in range(W):
            idx = h0 * S + 1
            for _ in range(H):
                A[idx] = to_int(data[tok])
                tok += 1
                idx += step

    Q = to_int(data[tok])
    sh = to_int(data[tok + 1])
    sw = to_int(data[tok + 2])
    tok += 3

    # Valid global indices for each diagonal.
    pos_lists = [None] * D
    for s in range(D):
        lo = s - W + 1
        if lo < 0:
            lo = 0
        hi = s if s < H else H - 1
        base = s * S
        pos_lists[s] = tuple(range(base + lo + 1, base + hi + 2))

    mod = MOD

    # Forward DP: F[cell] = sum of products from (0,0) to cell.
    F = [0] * M
    F[1] = A[1]
    for s in range(1, D):
        for idx in pos_lists[s]:
            F[idx] = A[idx] * (F[idx - S1] + F[idx - S]) % mod

    # Backward DP: G[cell] = sum of products from cell to (H-1,W-1).
    G = [0] * M
    end_idx = (D - 1) * S + H
    G[end_idx] = A[end_idx]
    for s in range(D - 2, -1, -1):
        for idx in pos_lists[s]:
            G[idx] = A[idx] * (G[idx + S] + G[idx + S + 1]) % mod

    ans = F[end_idx]

    def recompute_F(s, A=A, F=F, pos_lists=pos_lists, S=S, S1=S1, mod=mod):
        for idx in pos_lists[s]:
            F[idx] = A[idx] * (F[idx - S1] + F[idx - S]) % mod

    def recompute_G(s, A=A, G=G, pos_lists=pos_lists, S=S, mod=mod):
        for idx in pos_lists[s]:
            G[idx] = A[idx] * (G[idx + S] + G[idx + S + 1]) % mod

    # Index delta for each direction in the (possibly transposed) grid.
    didx_map = [0] * 256
    if not trans:
        didx_map[82] = S        # R
        didx_map[68] = S + 1    # D
        didx_map[76] = -S       # L
        didx_map[85] = -S - 1   # U
    else:
        didx_map[82] = S + 1    # R -> D
        didx_map[68] = S        # D -> R
        didx_map[76] = -S - 1   # L -> U
        didx_map[85] = -S       # U -> L

    s = sh + sw - 2
    idx = s * S + (sw if trans else sh)

    out = []
    append = out.append

    A_loc = A
    F_loc = F
    G_loc = G
    reF = recompute_F
    reG = recompute_G
    didx_map_loc = didx_map
    Dm1 = D - 1
    S_loc = S
    S1_loc = S1
    mod_loc = mod
    data_loc = data

    for _ in range(Q):
        c = data_loc[tok][0]
        a = to_int(data_loc[tok + 1])
        tok += 2

        didx = didx_map_loc[c]
        if didx > 0:
            s += 1
            idx += didx
            reF(s)
        else:
            s -= 1
            idx += didx
            reG(s)

        old = A_loc[idx]
        if old != a:
            if s == 0:
                pred = 1
            else:
                pred = F_loc[idx - S1_loc] + F_loc[idx - S_loc]

            if s == Dm1:
                succ = 1
            else:
                succ = G_loc[idx + S_loc] + G_loc[idx + S_loc + 1]

            coef = pred * succ % mod_loc
            ans = (ans + (a - old) * coef) % mod_loc

            A_loc[idx] = a
            F_loc[idx] = a * pred % mod_loc
            G_loc[idx] = a * succ % mod_loc

        append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()