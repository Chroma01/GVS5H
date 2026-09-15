import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    HW = H * W

    orig = list(map(int, data[2:2 + HW]))
    idx = 2 + HW

    Q = int(data[idx])
    sh = int(data[idx + 1])
    sw = int(data[idx + 2])
    idx += 3

    codes = [0] * Q
    vals = [0] * Q
    cntLR = 0
    cntUD = 0

    for i in range(Q):
        d = data[idx]
        a = int(data[idx + 1])
        idx += 2
        b = d[0]
        if b == 76:          # 'L'
            codes[i] = 0
            cntLR += 1
        elif b == 82:        # 'R'
            codes[i] = 1
            cntLR += 1
        elif b == 85:        # 'U'
            codes[i] = 2
            cntUD += 1
        else:                # 'D'
            codes[i] = 3
            cntUD += 1
        vals[i] = a

    del data

    mod = 998244353

    # Choose orientation.  Horizontal moves cost O(rows); vertical moves are amortized O(1).
    cost_no = H * cntLR
    cost_tr = W * cntUD
    if cost_tr < cost_no or (cost_tr == cost_no and W < H):
        trans = True
        K = W
        N = H
        A = orig
    else:
        trans = False
        K = H
        N = W
        A = [0] * HW
        for c in range(W):
            base = c * H
            pos = c
            for r in range(H):
                A[base + r] = orig[pos]
                pos += W
        orig = None

    size = (N + 1) * K
    L = [0] * size
    R = [0] * size

    # L[c] = forward DP entering column c, i.e. F[:, c-1].  L[0] = e_0.
    L[0] = 1

    # R[c] = backward DP inclusive in column c.  R[N] = e_{K-1}.
    R[N * K + K - 1] = 1

    # Precompute full forward DP.
    for c in range(N):
        inb = c * K
        outb = inb + K
        ab = inb
        above = 0
        for r in range(K):
            s = above + L[inb + r]
            if s >= mod:
                s -= mod
            v = (A[ab + r] * s) % mod
            L[outb + r] = v
            above = v

    # Precompute full backward DP.
    for c in range(N - 1, -1, -1):
        inb = (c + 1) * K
        outb = c * K
        ab = outb
        below = 0
        for r in range(K - 1, -1, -1):
            s = below + R[inb + r]
            if s >= mod:
                s -= mod
            v = (A[ab + r] * s) % mod
            R[outb + r] = v
            below = v

    ans = L[N * K + K - 1]

    if trans:
        r = sw - 1
        c = sh - 1
        # original L,R are vertical; original U,D are horizontal
        kind = (0, 0, 1, 1)
    else:
        r = sh - 1
        c = sw - 1
        # original L,R are horizontal; original U,D are vertical
        kind = (1, 1, 0, 0)

    delta = (-1, 1, -1, 1)

    # Current column c:
    # L[c+1] is correct on prefix [0, f_valid).
    # R[c] is correct on suffix [rv_valid, K).
    f_valid = K
    rv_valid = 0

    out = []
    append = out.append

    for qi in range(Q):
        code = codes[qi]
        a = vals[qi]

        if kind[code]:
            if delta[code] == 1:
                # Move right: finalize L[c+1] and compute L[c+2] in one top-down pass.
                baseC = c * K
                cur = baseC + K
                nxt = baseC + 2 * K
                a_cur = baseC
                a_next = baseC + K
                inb = baseC

                fv = f_valid
                prev = 0

                for i in range(fv):
                    fcur = L[cur + i]
                    s = prev + fcur
                    if s >= mod:
                        s -= mod
                    fn = (A[a_next + i] * s) % mod
                    L[nxt + i] = fn
                    prev = fn

                if fv < K:
                    above = L[cur + fv - 1] if fv else 0
                    for i in range(fv, K):
                        s = above + L[inb + i]
                        if s >= mod:
                            s -= mod
                        fcur = (A[a_cur + i] * s) % mod
                        L[cur + i] = fcur
                        above = fcur

                        s2 = prev + fcur
                        if s2 >= mod:
                            s2 -= mod
                        fn = (A[a_next + i] * s2) % mod
                        L[nxt + i] = fn
                        prev = fn

                c += 1
                f_valid = K
                rv_valid = 0

            else:
                # Move left: finalize R[c] and compute R[c-1] in one bottom-up pass.
                baseC = c * K
                cur = baseC
                prv = baseC - K
                a_cur = baseC
                a_prev = baseC - K
                inb = baseC + K

                rv = rv_valid
                nextval = 0

                for i in range(K - 1, rv - 1, -1):
                    rcur = R[cur + i]
                    s = nextval + rcur
                    if s >= mod:
                        s -= mod
                    rprv = (A[a_prev + i] * s) % mod
                    R[prv + i] = rprv
                    nextval = rprv

                if rv > 0:
                    below = R[cur + rv] if rv < K else 0
                    for i in range(rv - 1, -1, -1):
                        s = below + R[inb + i]
                        if s >= mod:
                            s -= mod
                        rcur = (A[a_cur + i] * s) % mod
                        R[cur + i] = rcur
                        below = rcur

                        s2 = nextval + rcur
                        if s2 >= mod:
                            s2 -= mod
                        rprv = (A[a_prev + i] * s2) % mod
                        R[prv + i] = rprv
                        nextval = rprv

                c -= 1
                f_valid = K
                rv_valid = 0

        else:
            r += delta[code]

        baseC = c * K
        baseC1 = baseC + K
        old = A[baseC + r]

        if old != a:
            # Prefix excluding (r,c): F[r-1,c] + F[r,c-1].
            if r:
                up_to = r - 1
                if up_to >= f_valid:
                    above = L[baseC1 + f_valid - 1] if f_valid else 0
                    for i in range(f_valid, up_to + 1):
                        s = above + L[baseC + i]
                        if s >= mod:
                            s -= mod
                        fcur = (A[baseC + i] * s) % mod
                        L[baseC1 + i] = fcur
                        above = fcur
                    f_valid = up_to + 1
                prefix = L[baseC1 + r - 1]
            else:
                prefix = 0

            prefix += L[baseC + r]
            if prefix >= mod:
                prefix -= mod

            # Suffix excluding (r,c): G[r+1,c] + G[r,c+1].
            if r + 1 < K:
                from_idx = r + 1
                if from_idx < rv_valid:
                    below = R[baseC + rv_valid] if rv_valid < K else 0
                    for i in range(rv_valid - 1, from_idx - 1, -1):
                        s = below + R[baseC1 + i]
                        if s >= mod:
                            s -= mod
                        rcur = (A[baseC + i] * s) % mod
                        R[baseC + i] = rcur
                        below = rcur
                    rv_valid = from_idx
                suffix = R[baseC + r + 1]
            else:
                suffix = 0

            suffix += R[baseC1 + r]
            if suffix >= mod:
                suffix -= mod

            diff = a - old
            if diff < 0:
                diff += mod

            term = (diff * prefix) % mod
            term = (term * suffix) % mod
            ans += term
            if ans >= mod:
                ans -= mod

            A[baseC + r] = a

            if r < f_valid:
                f_valid = r
            rp = r + 1
            if rp > rv_valid:
                rv_valid = rp

        append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()