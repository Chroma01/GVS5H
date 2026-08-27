import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    to_int = int
    p = 0

    H = to_int(data[p])
    W = to_int(data[p + 1])
    p += 2

    # Use the smaller dimension as the vector width.
    trans = H > W
    R = W if trans else H
    C = H if trans else W
    S = R + C - 2

    # Anti-diagonal s = r + c (0-indexed).
    L = [0] * (S + 1)
    length = [0] * (S + 1)
    for k in range(S + 1):
        l = k - (C - 1)
        if l < 0:
            l = 0
        u = k
        if u > R - 1:
            u = R - 1
        L[k] = l
        length[k] = u - l + 1

    # A[s][i] is the value on anti-diagonal s, index i = r - L[s].
    A = [[0] * length[k] for k in range(S + 1)]
    for h in range(H):
        for w in range(W):
            val = to_int(data[p])
            p += 1
            s = h + w
            r = w if trans else h
            A[s][r - L[s]] = val

    Q = to_int(data[p])
    sh = to_int(data[p + 1])
    sw = to_int(data[p + 2])
    p += 3

    r = (sw - 1) if trans else (sh - 1)
    s = sh + sw - 2

    # G[s]: prefix sums to diagonal s, excluding the cell itself.
    # B[s]: suffix sums from diagonal s, excluding the cell itself.
    G = [[0] * length[k] for k in range(S + 1)]
    B = [[0] * length[k] for k in range(S + 1)]
    G[0][0] = 1
    B[S][0] = 1

    mod = MOD

    # Case codes for full recomputation.
    g_case = [0] * S
    for t in range(S):
        diff = length[t + 1] - length[t]
        if diff == 1:
            g_case[t] = 1
        elif diff == 0:
            g_case[t] = 0
        else:
            g_case[t] = -1

    b_case = [0] * (S + 1)
    for t in range(1, S + 1):
        diff = length[t - 1] - length[t]
        if diff == 1:
            b_case[t] = 1
        elif diff == 0:
            b_case[t] = 0
        else:
            b_case[t] = -1

    def compute_G(k, G=G, A=A, length=length, g_case=g_case, mod=mod):
        t = k - 1
        old = G[t]
        a = A[t]
        new = G[k]
        n = length[t]
        case = g_case[t]

        if case == 1:  # target length n + 1
            pp = (a[0] * old[0]) % mod
            new[0] = pp
            for j in range(1, n):
                p = (a[j] * old[j]) % mod
                x = pp + p
                if x >= mod:
                    x -= mod
                new[j] = x
                pp = p
            new[n] = pp
        elif case == 0:  # target length n
            pp = (a[0] * old[0]) % mod
            new[0] = pp
            for j in range(1, n):
                p = (a[j] * old[j]) % mod
                x = pp + p
                if x >= mod:
                    x -= mod
                new[j] = x
                pp = p
        else:  # target length n - 1
            pp = (a[0] * old[0]) % mod
            for j in range(1, n):
                p = (a[j] * old[j]) % mod
                x = pp + p
                if x >= mod:
                    x -= mod
                new[j - 1] = x
                pp = p

    def compute_B(k, B=B, A=A, length=length, b_case=b_case, mod=mod):
        t = k + 1
        old = B[t]
        a = A[t]
        new = B[k]
        n = length[t]
        case = b_case[t]

        if case == 1:  # target length n + 1
            pp = (a[0] * old[0]) % mod
            new[0] = pp
            for j in range(1, n):
                p = (a[j] * old[j]) % mod
                x = pp + p
                if x >= mod:
                    x -= mod
                new[j] = x
                pp = p
            new[n] = pp
        elif case == 0:  # target length n
            # Required plateau form:
            # new[j] = p[j] + p[j+1] for j = 0..n-2, new[n-1] = p[n-1].
            pp = (a[0] * old[0]) % mod
            for j in range(1, n):
                p = (a[j] * old[j]) % mod
                x = pp + p
                if x >= mod:
                    x -= mod
                new[j - 1] = x
                pp = p
            new[n - 1] = pp
        else:  # target length n - 1
            pp = (a[0] * old[0]) % mod
            for j in range(1, n):
                p = (a[j] * old[j]) % mod
                x = pp + p
                if x >= mod:
                    x -= mod
                new[j - 1] = x
                pp = p

    # Initial full precomputation.
    for k in range(1, S + 1):
        compute_G(k)
    for k in range(S - 1, -1, -1):
        compute_B(k)

    # Initial answer at the starting diagonal.
    a = A[s]
    g = G[s]
    b = B[s]
    ans = 0
    for i in range(length[s]):
        ans += a[i] * g[i] * b[i]
    ans %= mod

    # Direction maps in transposed coordinates.
    # ASCII: U=85, D=68, L=76, R=82.
    ds = [0] * 128
    dr = [0] * 128
    if not trans:
        ds[85] = -1
        dr[85] = -1  # U
        ds[68] = 1
        dr[68] = 1   # D
        ds[76] = -1
        dr[76] = 0   # L
        ds[82] = 1
        dr[82] = 0   # R
    else:
        ds[85] = -1
        dr[85] = 0   # U
        ds[68] = 1
        dr[68] = 0   # D
        ds[76] = -1
        dr[76] = -1  # L
        ds[82] = 1
        dr[82] = 1   # R

    def add_G_target(src, j, v, G=G, length=length, g_case=g_case, mod=mod):
        arr = G[src + 1]
        case = g_case[src]
        n = length[src]

        if case == 1:  # target length n + 1
            x = arr[j] + v
            if x >= mod:
                x -= mod
            arr[j] = x
            x = arr[j + 1] + v
            if x >= mod:
                x -= mod
            arr[j + 1] = x
        elif case == 0:  # target length n
            x = arr[j] + v
            if x >= mod:
                x -= mod
            arr[j] = x
            if j + 1 < n:
                x = arr[j + 1] + v
                if x >= mod:
                    x -= mod
                arr[j + 1] = x
        else:  # target length n - 1
            if j > 0:
                x = arr[j - 1] + v
                if x >= mod:
                    x -= mod
                arr[j - 1] = x
            if j < n - 1:
                x = arr[j] + v
                if x >= mod:
                    x -= mod
                arr[j] = x

    def add_B_target(src, j, v, B=B, length=length, b_case=b_case, mod=mod):
        arr = B[src - 1]
        case = b_case[src]
        n = length[src]

        if case == 1:  # target length n + 1
            x = arr[j] + v
            if x >= mod:
                x -= mod
            arr[j] = x
            x = arr[j + 1] + v
            if x >= mod:
                x -= mod
            arr[j + 1] = x
        elif case == 0:  # target length n
            if j > 0:
                x = arr[j - 1] + v
                if x >= mod:
                    x -= mod
                arr[j - 1] = x
            x = arr[j] + v
            if x >= mod:
                x -= mod
            arr[j] = x
        else:  # target length n - 1
            if j > 0:
                x = arr[j - 1] + v
                if x >= mod:
                    x -= mod
                arr[j - 1] = x
            if j < n - 1:
                x = arr[j] + v
                if x >= mod:
                    x -= mod
                arr[j] = x

    def apply_G1(t, i, delta, g_val, G=G, length=length, g_case=g_case, mod=mod):
        if g_val:
            add = (delta * g_val) % mod
            if add:
                arr = G[t + 1]
                case = g_case[t]
                n = length[t]

                if case == 1:
                    x = arr[i] + add
                    if x >= mod:
                        x -= mod
                    arr[i] = x
                    x = arr[i + 1] + add
                    if x >= mod:
                        x -= mod
                    arr[i + 1] = x
                elif case == 0:
                    x = arr[i] + add
                    if x >= mod:
                        x -= mod
                    arr[i] = x
                    if i + 1 < n:
                        x = arr[i + 1] + add
                        if x >= mod:
                            x -= mod
                        arr[i + 1] = x
                else:
                    if i > 0:
                        x = arr[i - 1] + add
                        if x >= mod:
                            x -= mod
                        arr[i - 1] = x
                    if i < n - 1:
                        x = arr[i] + add
                        if x >= mod:
                            x -= mod
                        arr[i] = x

    def apply_B1(t, i, delta, b_val, B=B, length=length, b_case=b_case, mod=mod):
        if b_val:
            add = (delta * b_val) % mod
            if add:
                arr = B[t - 1]
                case = b_case[t]
                n = length[t]

                if case == 1:
                    x = arr[i] + add
                    if x >= mod:
                        x -= mod
                    arr[i] = x
                    x = arr[i + 1] + add
                    if x >= mod:
                        x -= mod
                    arr[i + 1] = x
                elif case == 0:
                    if i > 0:
                        x = arr[i - 1] + add
                        if x >= mod:
                            x -= mod
                        arr[i - 1] = x
                    x = arr[i] + add
                    if x >= mod:
                        x -= mod
                    arr[i] = x
                else:
                    if i > 0:
                        x = arr[i - 1] + add
                        if x >= mod:
                            x -= mod
                        arr[i - 1] = x
                    if i < n - 1:
                        x = arr[i] + add
                        if x >= mod:
                            x -= mod
                        arr[i] = x

    def apply_G2(t, i, delta, g_val, G=G, A=A, length=length, g_case=g_case,
                 mod=mod, add_G_target=add_G_target):
        if g_val:
            base = (delta * g_val) % mod
            if base:
                a_next = A[t + 1]
                case = g_case[t]
                n = length[t]

                if case == 1:
                    j = i
                    v = (base * a_next[j]) % mod
                    if v:
                        add_G_target(t + 1, j, v)
                    j = i + 1
                    v = (base * a_next[j]) % mod
                    if v:
                        add_G_target(t + 1, j, v)
                elif case == 0:
                    j = i
                    v = (base * a_next[j]) % mod
                    if v:
                        add_G_target(t + 1, j, v)
                    if i + 1 < n:
                        j = i + 1
                        v = (base * a_next[j]) % mod
                        if v:
                            add_G_target(t + 1, j, v)
                else:
                    if i > 0:
                        j = i - 1
                        v = (base * a_next[j]) % mod
                        if v:
                            add_G_target(t + 1, j, v)
                    if i < n - 1:
                        j = i
                        v = (base * a_next[j]) % mod
                        if v:
                            add_G_target(t + 1, j, v)

    def apply_B2(t, i, delta, b_val, B=B, A=A, length=length, b_case=b_case,
                 mod=mod, add_B_target=add_B_target):
        if b_val:
            base = (delta * b_val) % mod
            if base:
                a_prev = A[t - 1]
                case = b_case[t]
                n = length[t]

                if case == 1:
                    j = i
                    v = (base * a_prev[j]) % mod
                    if v:
                        add_B_target(t - 1, j, v)
                    j = i + 1
                    v = (base * a_prev[j]) % mod
                    if v:
                        add_B_target(t - 1, j, v)
                elif case == 0:
                    if i > 0:
                        j = i - 1
                        v = (base * a_prev[j]) % mod
                        if v:
                            add_B_target(t - 1, j, v)
                    j = i
                    v = (base * a_prev[j]) % mod
                    if v:
                        add_B_target(t - 1, j, v)
                else:
                    if i > 0:
                        j = i - 1
                        v = (base * a_prev[j]) % mod
                        if v:
                            add_B_target(t - 1, j, v)
                    if i < n - 1:
                        j = i
                        v = (base * a_prev[j]) % mod
                        if v:
                            add_B_target(t - 1, j, v)

    # Maintain a small window of extra valid vectors:
    # G[s+1], G[s+2], B[s-1], B[s-2].
    g1_ok = s + 1 <= S
    g2_ok = s + 2 <= S
    b1_ok = s - 1 >= 0
    b2_ok = s - 2 >= 0

    out = []
    append = out.append

    cG = compute_G
    cB = compute_B
    aG1 = apply_G1
    aB1 = apply_B1
    aG2 = apply_G2
    aB2 = apply_B2
    Ls = L
    As = A
    Gs = G
    Bs = B
    ds_l = ds
    dr_l = dr
    mod_l = mod

    for _ in range(Q):
        d = data[p][0]
        val = to_int(data[p + 1])
        p += 2

        r += dr_l[d]
        new_s = s + ds_l[d]

        old_g1, old_g2, old_b1, old_b2 = g1_ok, g2_ok, b1_ok, b2_ok

        if new_s == s + 1:
            # Move to the next anti-diagonal.
            if not g1_ok:
                cG(new_s)
                g1_ok = True

            i = r - Ls[new_s]
            a_new = As[new_s]
            old_val = a_new[i]
            changed = old_val != val

            if changed:
                delta = val - old_val
                if delta < 0:
                    delta += mod_l

                g_val = Gs[new_s][i]
                b_val = Bs[new_s][i]
                ans = (ans + (delta * g_val % mod_l) * b_val) % mod_l

                # B[new_s - 1] becomes the new b1.
                aB1(new_s, i, delta, b_val)

                # G[new_s + 1] becomes the new g1, if it was valid.
                if old_g2:
                    aG1(new_s, i, delta, g_val)
                    new_g1 = True
                else:
                    new_g1 = False

                # B[new_s - 2] becomes the new b2, if it was valid.
                if old_b1:
                    aB2(new_s, i, delta, b_val)
                    new_b2 = True
                else:
                    new_b2 = False

                a_new[i] = val

                g1_ok = new_g1
                g2_ok = False
                b1_ok = True
                b2_ok = new_b2
            else:
                g1_ok = old_g2
                g2_ok = False
                b1_ok = True
                b2_ok = old_b1

            s = new_s

        else:
            # Move to the previous anti-diagonal.
            if not b1_ok:
                cB(new_s)
                b1_ok = True

            i = r - Ls[new_s]
            a_new = As[new_s]
            old_val = a_new[i]
            changed = old_val != val

            if changed:
                delta = val - old_val
                if delta < 0:
                    delta += mod_l

                g_val = Gs[new_s][i]
                b_val = Bs[new_s][i]
                ans = (ans + (delta * g_val % mod_l) * b_val) % mod_l

                # G[new_s + 1] becomes the new g1.
                aG1(new_s, i, delta, g_val)

                # B[new_s - 1] becomes the new b1, if it was valid.
                if old_b2:
                    aB1(new_s, i, delta, b_val)
                    new_b1 = True
                else:
                    new_b1 = False

                # G[new_s + 2] becomes the new g2, if it was valid.
                if old_g1:
                    aG2(new_s, i, delta, g_val)
                    new_g2 = True
                else:
                    new_g2 = False

                a_new[i] = val

                g1_ok = True
                g2_ok = new_g2
                b1_ok = new_b1
                b2_ok = False
            else:
                g1_ok = True
                g2_ok = old_g1
                b1_ok = old_b2
                b2_ok = False

            s = new_s

        append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()