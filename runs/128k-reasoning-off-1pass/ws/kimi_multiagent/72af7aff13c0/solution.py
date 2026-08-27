import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos+1]); pos += 2

    # Transpose so that W = min(H, W) (the thin dimension)
    transpose = False
    if H < W:
        transpose = True
        H, W = W, H

    A = [[0]*(W+1) for _ in range(H+1)]
    if not transpose:
        for i in range(1, H+1):
            Ai = A[i]
            for j in range(1, W+1):
                Ai[j] = int(data[pos]); pos += 1
    else:
        col = [list(map(int, data[pos + r*W : pos + (r+1)*W])) for r in range(W)]
        pos += H * W
        for i in range(1, H+1):
            Ai = A[i]
            ci = col[i-1]
            for j in range(1, W+1):
                Ai[j] = ci[j-1]

    Q = int(data[pos]); sh = int(data[pos+1]); sw = int(data[pos+2]); pos += 3
    if transpose:
        sh, sw = sw, sh

    # Simulate the walk to know all updated cells
    h, w = sh, sw
    cells = []
    for _ in range(Q):
        d = data[pos]; a = int(data[pos+1]); pos += 2
        if d == b'L': w -= 1
        elif d == b'R': w += 1
        elif d == b'U': h -= 1
        else: h += 1
        cells.append((h, w, a))

    F = [[0]*(W+1) for _ in range(H+1)]

    def full_rebuild():
        F[0][1] = 1
        for i in range(1, H+1):
            Fi = F[i]; Fim1 = F[i-1]; Ai = A[i]
            s = 0
            for j in range(1, W+1):
                s = Ai[j] * (Fim1[j] + s) % MOD
                Fi[j] = s
        F[0][1] = 0

    out = []
    B = 450
    n = len(cells)
    for blk_start in range(0, n, B):
        blk = cells[blk_start:blk_start+B]
        m = len(blk)
        rmin = min(c[0] for c in blk)
        cmin = min(c[1] for c in blk)
        full_rebuild()
        for t in range(m):
            ch, cw, a = blk[t]
            A[ch][cw] = a
            # Repair union of cones of this block's updates: rows >= rmin, cols >= cmin
            for i in range(rmin, H+1):
                Fi = F[i]; Fim1 = F[i-1]; Ai = A[i]
                prev = Fi[cmin-1]
                for j in range(cmin, W+1):
                    v = Ai[j] * (Fim1[j] + prev) % MOD
                    Fi[j] = v
                    prev = v
            out.append(str(F[H][W]))

    sys.stdout.write("\n".join(out) + "\n")

main()