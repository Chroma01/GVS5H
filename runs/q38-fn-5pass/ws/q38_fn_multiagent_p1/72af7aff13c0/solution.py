import sys


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    nxt = it.__next__
    to_int = int

    H0 = to_int(nxt())
    W0 = to_int(nxt())

    # Transpose so that W <= H.  This makes the padded stride small and keeps
    # diagonal indices cache-friendly.
    trans = H0 < W0
    if trans:
        H, W = W0, H0
    else:
        H, W = H0, W0

    st = W + 2
    size = (H + 2) * st
    A = [0] * size

    if trans:
        for h in range(1, H0 + 1):
            for w in range(1, W0 + 1):
                A[w * st + h] = to_int(nxt())
    else:
        for h in range(1, H + 1):
            base = h * st
            for w in range(1, W + 1):
                A[base + w] = to_int(nxt())

    Q = to_int(nxt())
    sh = to_int(nxt())
    sw = to_int(nxt())
    if trans:
        sh, sw = sw, sh

    MOD = 998244353
    m = MOD
    step = st - 1

    # Diagonal indices are arithmetic progressions.
    diags = [None] * (H + W + 1)
    for s in range(2, H + W + 1):
        h_min = s - W
        if h_min < 1:
            h_min = 1
        h_max = s - 1
        if h_max > H:
            h_max = H
        start = h_min * st + (s - h_min)
        cnt = h_max - h_min + 1
        diags[s] = list(range(start, start + cnt * step, step))

    a = A

    # Prefix DP.  Border (1,0) = 1 gives pref_excl(start) = 1.
    p = [0] * size
    p[st] = 1
    for h in range(1, H + 1):
        base = h * st
        up = base - st
        left = p[base]
        for w in range(1, W + 1):
            idx = base + w
            x = p[up + w] + left
            if x >= m:
                x -= m
            val = (a[idx] * x) % m
            p[idx] = val
            left = val

    # Suffix DP.  Border (H+1,W) = 1 gives suff_excl(end) = 1.
    sf = [0] * size
    sf[(H + 1) * st + W] = 1
    for h in range(H, 0, -1):
        base = h * st
        down = base + st
        right = 0
        for w in range(W, 0, -1):
            idx = base + w
            x = sf[down + w] + right
            if x >= m:
                x -= m
            val = (a[idx] * x) % m
            sf[idx] = val
            right = val

    ans = p[H * st + W]

    # Direction deltas in the (possibly transposed) grid.
    d_idx = [0] * 256
    if trans:
        d_idx[ord('L')] = -st
        d_idx[ord('R')] = st
        d_idx[ord('U')] = -1
        d_idx[ord('D')] = 1
    else:
        d_idx[ord('L')] = -1
        d_idx[ord('R')] = 1
        d_idx[ord('U')] = -st
        d_idx[ord('D')] = st

    cur = sh * st + sw
    diag = sh + sw

    # For an immediate back-and-forth move, we can update only the affected
    # neighboring cells instead of recomputing the whole diagonal.
    prev_di = 0
    prev_idx = 0
    prev_pd = 0
    prev_sd = 0

    out = []
    append = out.append
    to_str = str
    dg = diags

    for _ in range(Q):
        d = nxt()[0]
        di = d_idx[d]
        cur += di
        new = to_int(nxt())
        old = a[cur]
        changed = old != new

        use_opt = (prev_di != 0 and di == -prev_di)

        if use_opt:
            if di > 0:
                delta = prev_pd
                if delta:
                    v = prev_idx
                    h = v // st
                    w = v - h * st
                    if h < H:
                        y = v + st
                        add = (a[y] * delta) % m
                        p[y] += add
                        if p[y] >= m:
                            p[y] -= m
                    if w < W:
                        y = v + 1
                        add = (a[y] * delta) % m
                        p[y] += add
                        if p[y] >= m:
                            p[y] -= m
            else:
                delta = prev_sd
                if delta:
                    v = prev_idx
                    h = v // st
                    w = v - h * st
                    if h > 1:
                        y = v - st
                        add = (a[y] * delta) % m
                        sf[y] += add
                        if sf[y] >= m:
                            sf[y] -= m
                    if w > 1:
                        y = v - 1
                        add = (a[y] * delta) % m
                        sf[y] += add
                        if sf[y] >= m:
                            sf[y] -= m

        if changed:
            pe = p[cur - st] + p[cur - 1]
            if pe >= m:
                pe -= m
            se = sf[cur + st] + sf[cur + 1]
            if se >= m:
                se -= m

            diff = new - old
            if diff < 0:
                diff += m

            delta_ans = (diff * pe % m) * se % m
            ans += delta_ans
            if ans >= m:
                ans -= m

            a[cur] = new
            delta_p = (diff * pe) % m
            delta_s = (diff * se) % m
        else:
            delta_p = 0
            delta_s = 0

        if di > 0:
            diag += 1
            if use_opt:
                if changed:
                    p[cur] = (new * pe) % m
            else:
                for ci in dg[diag]:
                    x = p[ci - st] + p[ci - 1]
                    if x >= m:
                        x -= m
                    p[ci] = (a[ci] * x) % m
            if changed:
                sf[cur] = (new * se) % m
        else:
            diag -= 1
            if use_opt:
                if changed:
                    sf[cur] = (new * se) % m
            else:
                for ci in dg[diag]:
                    x = sf[ci + st] + sf[ci + 1]
                    if x >= m:
                        x -= m
                    sf[ci] = (a[ci] * x) % m
            if changed:
                p[cur] = (new * pe) % m

        prev_di = di
        prev_idx = cur
        prev_pd = delta_p
        prev_sd = delta_s

        append(to_str(ans))

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    solve()