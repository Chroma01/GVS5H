import sys
import numpy as np

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    p = 0
    H = int(data[p]); W = int(data[p+1]); p += 2
    A = [[int(data[p + i*W + j]) % MOD for j in range(W)] for i in range(H)]
    p += H * W
    Q = int(data[p]); sh = int(data[p+1]); sw = int(data[p+2]); p += 3

    # Transpose so W <= H (width is the smaller dimension, W <= 447)
    transposed = False
    if W > H:
        transposed = True
        A = [list(row) for row in zip(*A)]
        H, W = W, H
        sh, sw = sw, sh

    if transposed:
        dirmap = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
    else:
        dirmap = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}

    # Queries decoded up front
    queries = []
    for _ in range(Q):
        d = data[p].decode(); a = int(data[p+1]) % MOD; p += 2
        queries.append((dirmap[d], a))

    # ---------------- Small-W path: pure Python tight loops ----------------
    if W <= 24:
        # din[i] = dp tuple (length W) entering row i (0-indexed rows 0..H-1)
        din = [None] * (H + 1)
        dp0 = [0] * W
        din[0] = tuple(dp0)
        for i in range(H):
            row = A[i]
            ndp = [0] * W
            s = 0
            for j in range(W):
                s += dp0[j]
                ndp[j] = row[j] * s % MOD
            dp0 = ndp
            din[i + 1] = tuple(dp0)

        B = 450
        out = []
        cur_h, cur_w = sh, sw
        top_dirty = H + 1
        since = 0
        M = MOD
        for (dh, dw), a in queries:
            cur_h += dh; cur_w += dw
            A[cur_h - 1][cur_w - 1] = a
            if cur_h < top_dirty:
                top_dirty = cur_h
            since += 1

            dp = list(din[top_dirty - 1])
            for i in range(top_dirty - 1, H):
                row = A[i]
                ndp = [0] * W
                s = 0
                for j in range(W):
                    s += dp[j]
                    ndp[j] = row[j] * s % M
                dp = ndp
            out.append(str(dp[W - 1] % M))

            if since >= B:
                # full rebuild of checkpoints
                dp = [0] * W
                din[0] = tuple(dp)
                for i in range(H):
                    row = A[i]
                    ndp = [0] * W
                    s = 0
                    for j in range(W):
                        s += dp[j]
                        ndp[j] = row[j] * s % M
                    dp = ndp
                    din[i + 1] = tuple(dp)
                top_dirty = H + 1
                since = 0

        sys.stdout.write("\n".join(out) + "\n")
        return

    # ---------------- Large-W path: numpy with adaptive checkpointing ----------------
    Am = [np.array(row, dtype=np.int64) for row in A]
    din = [None] * (H + 1)  # din[i] = dp vector entering row i (length W+1, slot 0 = 0)

    def full_rebuild():
        dp = np.zeros(W + 1, dtype=np.int64)
        din[0] = dp.copy()
        for i in range(H):
            dp[1:] = (Am[i] * (np.cumsum(dp[:W]) % MOD)) % MOD
            din[i + 1] = dp.copy()

    full_rebuild()

    B = 450
    # If the recompute suffix exceeds LONG, refresh checkpoints immediately.
    # Cost of refresh ~ H row-ops; amortized against the LONG row-ops we would
    # otherwise pay per subsequent query in this dirty stretch.
    LONG = max(4 * B, H // 4)

    out = []
    cur_h, cur_w = sh, sw
    top_dirty = H + 1
    since = 0

    for (dh, dw), a in queries:
        cur_h += dh; cur_w += dw
        Am[cur_h - 1][cur_w - 1] = a
        if cur_h < top_dirty:
            top_dirty = cur_h
        since += 1

        dp = din[top_dirty - 1].copy()
        for i in range(top_dirty - 1, H):
            dp[1:] = (Am[i] * (np.cumsum(dp[:W]) % MOD)) % MOD
        out.append(str(int(dp[W] % MOD)))

        if since >= B or (H - top_dirty + 1) > LONG:
            full_rebuild()
            top_dirty = H + 1
            since = 0

    sys.stdout.write("\n".join(out) + "\n")

main()