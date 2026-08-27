import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    cells = H * W

    qpos = 2 + cells
    Q = int(data[qpos])
    sh = int(data[qpos + 1])
    sw = int(data[qpos + 2])
    qdir = qpos + 3

    # Count moves that would be horizontal in each of the two orientations.
    lr = 0
    for i in range(Q):
        ch = data[qdir + 2 * i][0]
        if ch == 76 or ch == 82:  # L or R
            lr += 1
    ud = Q - lr

    # Transposing swaps which original moves become horizontal.
    # A horizontal move costs O(number_of_rows), while a vertical move is O(1).
    transposed = W * ud < H * lr

    rows = []
    p = 2
    for _ in range(H):
        rows.append(list(map(int, data[p:p + W])))
        p += W

    # Direction codes in the computational grid:
    # 0=left, 1=right, 2=up, 3=down.
    dcode = [0] * 256
    if transposed:
        m, n = W, H
        cols = rows  # Original row h becomes transposed column h.
        r, c = sw - 1, sh - 1
        dcode[76] = 2  # original L -> transposed U
        dcode[82] = 3  # original R -> transposed D
        dcode[85] = 0  # original U -> transposed L
        dcode[68] = 1  # original D -> transposed R
    else:
        m, n = H, W
        cols = [list(col) for col in zip(*rows)]
        del rows
        r, c = sh - 1, sw - 1
        dcode[76] = 0
        dcode[82] = 1
        dcode[85] = 2
        dcode[68] = 3

    mod = MOD
    m1 = m - 1

    def forward_new(col, vec):
        """Apply one column to a left DP frontier."""
        out = [0] * m
        acc = 0
        for i in range(m):
            x = vec[i] + acc
            if x >= mod:
                x -= mod
            acc = col[i] * x % mod
            out[i] = acc
        return out

    def backward_new(col, vec):
        """Apply one column to a right suffix frontier."""
        out = [0] * m
        acc = 0
        for i in range(m1, -1, -1):
            x = vec[i] + acc
            if x >= mod:
                x -= mod
            acc = col[i] * x % mod
            out[i] = acc
        return out

    # pref is the DP frontier before the current column.
    # The virtual source is represented by e_1.
    v = [0] * m
    v[0] = 1
    left_stack = [v]
    for j in range(n):
        v = forward_new(cols[j], v)
        if j < c:
            left_stack.append(v)
    ans = v[-1]
    pref = left_stack[-1]

    # suff is the suffix frontier after the current column.
    # The virtual sink is represented by e_m.
    v = [0] * m
    v[-1] = 1
    right_stack = [v]
    for j in range(n - 1, c, -1):
        v = backward_new(cols[j], v)
        right_stack.append(v)
    suff = right_stack[-1]

    # For the current column:
    # L[i] = weighted paths reaching a predecessor of cell i,
    # R[i] = weighted paths leaving a successor of cell i.
    # Both exclude A[current column][i].
    L = [0] * m
    R = [0] * m
    col = cols[c]

    acc = 0
    for i in range(m):
        x = pref[i] + acc
        if x >= mod:
            x -= mod
        L[i] = x
        acc = col[i] * x % mod

    acc = 0
    for i in range(m1, -1, -1):
        x = suff[i] + acc
        if x >= mod:
            x -= mod
        R[i] = x
        acc = col[i] * x % mod

    out_lines = []
    pos = qdir

    for _ in range(Q):
        code = dcode[data[pos][0]]
        a = int(data[pos + 1])
        pos += 2

        if code == 0:  # Move left.
            oldcol = col

            # Reuse the obsolete left-frontier vector as the new suffix vector.
            buf = left_stack.pop()
            new_pref = left_stack[-1]

            c -= 1
            col = cols[c]

            # Cross the old column from right to left, and simultaneously
            # build all R values for the new current column.
            acc_boundary = 0
            acc_new = 0
            for i in range(m1, -1, -1):
                x = suff[i] + acc_boundary
                if x >= mod:
                    x -= mod
                acc_boundary = oldcol[i] * x % mod
                buf[i] = acc_boundary

                y = acc_boundary + acc_new
                if y >= mod:
                    y -= mod
                R[i] = y
                acc_new = col[i] * y % mod

            right_stack.append(buf)
            suff = buf
            pref = new_pref

            # Build all L values for the new current column.
            acc = 0
            for i in range(m):
                y = pref[i] + acc
                if y >= mod:
                    y -= mod
                L[i] = y
                acc = col[i] * y % mod

        elif code == 1:  # Move right.
            oldcol = col

            # Reuse the obsolete suffix vector as the new left-frontier vector.
            buf = right_stack.pop()
            new_suff = right_stack[-1]

            c += 1
            col = cols[c]

            # Cross the old column from left to right, and simultaneously
            # build all L values for the new current column.
            acc_boundary = 0
            acc_new = 0
            for i in range(m):
                x = pref[i] + acc_boundary
                if x >= mod:
                    x -= mod
                acc_boundary = oldcol[i] * x % mod
                buf[i] = acc_boundary

                y = acc_boundary + acc_new
                if y >= mod:
                    y -= mod
                L[i] = y
                acc_new = col[i] * y % mod

            left_stack.append(buf)
            pref = buf
            suff = new_suff

            # Build all R values for the new current column.
            acc = 0
            for i in range(m1, -1, -1):
                y = suff[i] + acc
                if y >= mod:
                    y -= mod
                R[i] = y
                acc = col[i] * y % mod

        elif code == 2:  # Move up.
            nr = r - 1
            # R[nr] depends on the cell we are leaving.
            x = suff[nr] + col[r] * R[r] % mod
            if x >= mod:
                x -= mod
            R[nr] = x
            r = nr

        else:  # Move down.
            nr = r + 1
            # L[nr] depends on the cell we are leaving.
            x = pref[nr] + col[r] * L[r] % mod
            if x >= mod:
                x -= mod
            L[nr] = x
            r = nr

        # F is affine in A[r][c]:
        # F = paths_avoiding_cell + A[r][c] * L[r] * R[r].
        left_value = L[r]
        right_value = R[r]
        old = col[r]
        delta = a - old
        if delta:
            if delta < 0:
                delta += mod
            ans = (ans + delta * left_value % mod * right_value) % mod
        col[r] = a

        out_lines.append(str(ans))

    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()