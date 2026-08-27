import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos+1]); pos += 2
    n = H * W
    A = [0] * n
    for i in range(n):
        A[i] = int(data[pos]); pos += 1
    Q = int(data[pos]); sh = int(data[pos+1]); sw = int(data[pos+2]); pos += 3
    x = sh - 1
    y = sw - 1

    # forward dp: dp[i][j] = A[i][j] * (dp[i-1][j] + dp[i][j-1])
    dp = [0] * n
    for i in range(H):
        base = i * W
        up = base - W
        left = 0
        for j in range(W):
            s = left
            if i > 0:
                s += dp[up + j]
            v = A[base + j] * s % MOD
            dp[base + j] = v
            left = v

    # reverse rdp: rdp[i][j] = A[i+1][j]*rdp[i+1][j] + A[i][j+1]*rdp[i][j+1]
    # rdp[H-1][W-1] = 1 ; sum over paths from (i,j) to (H-1,W-1) of products of cells after (i,j)
    rdp = [0] * n
    rdp[n - 1] = 1
    for i in range(H - 1, -1, -1):
        base = i * W
        down = base + W
        for j in range(W - 1, -1, -1):
            if i == H - 1 and j == W - 1:
                continue
            s = 0
            if i + 1 < H:
                s += A[down + j] * rdp[down + j]
            if j + 1 < W:
                s += A[base + j + 1] * rdp[base + j + 1]
            rdp[base + j] = s % MOD

    ans = dp[n - 1]
    out = []
    for _ in range(Q):
        d = data[pos]; a = int(data[pos+1]); pos += 2
        c = d[0]
        if c == 76:    # L
            y -= 1
        elif c == 82:  # R
            y += 1
        elif c == 85:  # U
            x -= 1
        else:          # D
            x += 1

        idx = x * W + y
        old = A[idx]
        if a != old:
            # L = dp[x-1][y] + dp[x][y-1]  (excludes cell itself)
            L = 0
            if x > 0:
                L = dp[idx - W]
            if y > 0:
                L += dp[idx - 1]
            L %= MOD
            R = rdp[idx]
            ans = (ans + (a - old) * (L * R % MOD)) % MOD
            A[idx] = a

            # repair dp over rows x..H-1, cols y..W-1
            # row x: left neighbor dp[x][y-1] is unchanged
            left = dp[idx - 1] if y > 0 else 0
            basex = x * W
            upx = basex - W
            for j in range(y, W):
                s = left
                if x > 0:
                    s += dp[upx + j]
                v = A[basex + j] * s % MOD
                dp[basex + j] = v
                left = v
            for i in range(x + 1, H):
                base = i * W
                up = base - W
                left = dp[base + y - 1] if y > 0 else 0
                for j in range(y, W):
                    v = A[base + j] * (left + dp[up + j]) % MOD
                    dp[base + j] = v
                    left = v

            # repair rdp over rows 0..x, cols 0..y
            # rdp[x][y] itself depends only on downstream cells -> unchanged,
            # but recomputing it yields the same value; start from row x going up.
            for i in range(x, -1, -1):
                base = i * W
                down = base + W
                for j in range(y, -1, -1):
                    s = 0
                    if i + 1 < H:
                        s += A[down + j] * rdp[down + j]
                    if j + 1 < W:
                        s += A[base + j + 1] * rdp[base + j + 1]
                    rdp[base + j] = s % MOD

        out.append(str(ans))

    sys.stdout.write("\n".join(out) + "\n")

main()