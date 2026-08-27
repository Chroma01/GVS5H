import sys
import math


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]
    p += 1
    A = data[p:p + N]
    p += N
    B = data[p:p + N]
    p += N
    K = data[p]
    p += 1
    X = [0] * K
    Y = [0] * K
    for i in range(K):
        X[i] = data[p]
        Y[i] = data[p + 1]
        p += 2
    del data

    # Number of index blocks.  S is the number of blocks, not the block size.
    logN = math.log2(N) if N > 1 else 0.0
    S = min(50, int(math.sqrt(K * logN / 4.0)) + 1)
    if S < 1:
        S = 1

    L = (N + S - 1) // S
    nb = (N + L - 1) // L
    full_blocks = N // L          # only complete blocks of length L

    # Global prefix sums of original values.
    prefA = [0] * (N + 1)
    s = 0
    for i, a in enumerate(A):
        s += a
        prefA[i + 1] = s

    prefB = [0] * (N + 1)
    s = 0
    for i, b in enumerate(B):
        s += b
        prefB[i + 1] = s

    def build_blocks(arr):
        starts = [i * L for i in range(nb)]
        lens = [0] * nb
        sorted_vals = []
        sorted_idxs = []
        sorted_pref = []
        sums = []
        for i in range(nb):
            st = i * L
            m = N - st
            if m > L:
                m = L
            lens[i] = m
            vals = arr[st:st + m]
            order = list(range(m))
            order.sort(key=vals.__getitem__)
            sv = [vals[idx] for idx in order]
            sp = [0]
            ss = 0
            for v in sv:
                ss += v
                sp.append(ss)
            sorted_vals.append(sv)
            sorted_idxs.append(order)
            sorted_pref.append(sp)
            sums.append(ss)
        return starts, lens, sorted_vals, sorted_idxs, sorted_pref, sums

    A_starts, A_lens, A_sorted_vals, A_sorted_idxs, A_sorted_pref, A_sums = build_blocks(A)
    B_starts, B_lens, B_sorted_vals, B_sorted_idxs, B_sorted_pref, B_sums = build_blocks(B)

    # Global order by value, used for on-the-full-block cost columns.
    A_g_idxs = list(range(N))
    A_g_idxs.sort(key=A.__getitem__)
    A_g_vals = [A[i] for i in A_g_idxs]

    B_g_idxs = list(range(N))
    B_g_idxs.sort(key=B.__getitem__)
    B_g_vals = [B[i] for i in B_g_idxs]

    # Decompose queries into full blocks and remainders.
    fa = [0] * K
    fb = [0] * K
    ra = [0] * K
    rb = [0] * K
    A_start = [0] * K
    B_start = [0] * K

    for i in range(K):
        x = X[i]
        y = Y[i]
        fa_i = x // L
        ra_i = x - fa_i * L
        fb_i = y // L
        rb_i = y - fb_i * L
        fa[i] = fa_i
        fb[i] = fb_i
        ra[i] = ra_i
        rb[i] = rb_i
        A_start[i] = fa_i * L
        B_start[i] = fb_i * L

    # Queries that need remainder-vs-full contributions.
    queries_by_fb = [[] for _ in range(full_blocks + 1)]
    queries_by_fa = [[] for _ in range(full_blocks + 1)]
    has_ra = False
    has_rb = False
    for i in range(K):
        if ra[i]:
            has_ra = True
            queries_by_fb[fb[i]].append(i)
        if rb[i]:
            has_rb = True
            queries_by_fa[fa[i]].append(i)

    ans = [0] * K

    # ---------------- Partial-partial ----------------
    DIRECT_THRESH = 2000

    def cost_direct(fa, fb, x, y, A=A, B=B, L=L):
        sa = fa * L
        sb = fb * L
        total = 0
        if x <= y:
            A_loc = A
            B_loc = B
            for i in range(sa, sa + x):
                ai = A_loc[i]
                for j in range(sb, sb + y):
                    d = ai - B_loc[j]
                    if d < 0:
                        d = -d
                    total += d
        else:
            A_loc = A
            B_loc = B
            for j in range(sb, sb + y):
                bj = B_loc[j]
                for i in range(sa, sa + x):
                    d = A_loc[i] - bj
                    if d < 0:
                        d = -d
                    total += d
        return total

    def cost_sort(fa, fb, x, y, A=A, B=B, L=L):
        sa = fa * L
        sb = fb * L
        ua = A[sa:sa + x]
        vb = B[sb:sb + y]
        ua.sort()
        vb.sort()

        if x <= y:
            outer = ua
            inner = vb
            m = y
        else:
            outer = vb
            inner = ua
            m = x

        sum_inner = sum(inner)
        j = 0
        pref = 0
        total = 0
        for o in outer:
            while j < m and inner[j] < o:
                pref += inner[j]
                j += 1
            total += o * j - pref + (sum_inner - pref) - o * (m - j)
        return total

    def cost_scan(fa, fb, x, y,
                  L=L,
                  prefA=prefA,
                  prefB=prefB,
                  A_sorted_vals=A_sorted_vals,
                  A_sorted_idxs=A_sorted_idxs,
                  B_sorted_vals=B_sorted_vals,
                  B_sorted_idxs=B_sorted_idxs,
                  A_lens=A_lens,
                  B_lens=B_lens):
        sa = fa * L
        sb = fb * L
        lenA = A_lens[fa]
        lenB = B_lens[fb]

        if lenA <= lenB:
            sum_inner = prefB[sb + y] - prefB[sb]
            av = A_sorted_vals[fa]
            ai = A_sorted_idxs[fa]
            bv = B_sorted_vals[fb]
            bi = B_sorted_idxs[fb]

            j = 0
            cnt = 0
            sum_less = 0
            total = 0
            blen = lenB
            for t in range(lenA):
                u = av[t]
                if ai[t] >= x:
                    continue
                while j < blen and bv[j] < u:
                    if bi[j] < y:
                        cnt += 1
                        sum_less += bv[j]
                    j += 1
                total += u * cnt - sum_less + (sum_inner - sum_less) - u * (y - cnt)
            return total
        else:
            sum_inner = prefA[sa + x] - prefA[sa]
            bv = B_sorted_vals[fb]
            bi = B_sorted_idxs[fb]
            av = A_sorted_vals[fa]
            ai = A_sorted_idxs[fa]

            j = 0
            cnt = 0
            sum_less = 0
            total = 0
            alen = lenA
            for t in range(lenB):
                v = bv[t]
                if bi[t] >= y:
                    continue
                while j < alen and av[j] < v:
                    if ai[j] < x:
                        cnt += 1
                        sum_less += av[j]
                    j += 1
                total += v * cnt - sum_less + (sum_inner - sum_less) - v * (x - cnt)
            return total

    groups = {}
    for i in range(K):
        x = ra[i]
        y = rb[i]
        if x and y:
            key = (fa[i], fb[i])
            if key in groups:
                groups[key].append((i, x, y))
            else:
                groups[key] = [(i, x, y)]

    for (fa_g, fb_g), qlist in groups.items():
        max_x = 0
        max_y = 0
        per_est = 0
        for _, x, y in qlist:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if x * y <= DIRECT_THRESH:
                per_est += x * y
            elif x + y <= L:
                per_est += 2 * (x + y)
            else:
                per_est += 2 * L

        row_cost = max_x * max_y

        if row_cost <= per_est:
            sa = fa_g * L
            sb = fb_g * L
            V = B[sb:sb + max_y]
            col = [0] * (max_y + 1)
            qs = sorted(qlist, key=lambda t: t[1])
            row = 0
            m = max_y
            A_loc = A
            col_loc = col
            V_loc = V
            for qi, x, y in qs:
                while row < x:
                    u = A_loc[sa + row]
                    s = 0
                    for j in range(m):
                        d = u - V_loc[j]
                        if d < 0:
                            d = -d
                        s += d
                        col_loc[j + 1] += s
                    row += 1
                ans[qi] += col[y]
        else:
            cache = {}
            for qi, x, y in qlist:
                key = (x, y)
                cost = cache.get(key)
                if cost is None:
                    if x * y <= DIRECT_THRESH:
                        cost = cost_direct(fa_g, fb_g, x, y)
                    elif x + y <= L:
                        cost = cost_sort(fa_g, fb_g, x, y)
                    else:
                        cost = cost_scan(fa_g, fb_g, x, y)
                    cache[key] = cost
                ans[qi] += cost

    # ---------------- B full blocks: A-remainder vs B-full, and C ----------------
    C = [[0] * nb for _ in range(nb)]
    cost_arr = [0] * N
    prefix = [0] * (N + 1)

    ans_l = ans
    X_l = X
    A_start_l = A_start

    for b in range(full_blocks):
        bv = B_sorted_vals[b]
        bp = B_sorted_pref[b]
        bsum = B_sums[b]
        m = B_lens[b]

        j = 0
        ca = cost_arr
        for u, idx in zip(A_g_vals, A_g_idxs):
            while j < m and bv[j] < u:
                j += 1
            sl = bp[j]
            ca[idx] = u * j - sl + (bsum - sl) - u * (m - j)

        s = 0
        prefix[0] = 0
        pref = prefix
        for a in range(nb):
            st = a * L
            en = st + A_lens[a]
            block_sum = 0
            for i in range(st, en):
                c = ca[i]
                s += c
                block_sum += c
                pref[i + 1] = s
            C[a][b] = block_sum

        for fb_val in range(b + 1, full_blocks + 1):
            for qi in queries_by_fb[fb_val]:
                ans_l[qi] += pref[X_l[qi]] - pref[A_start_l[qi]]

    # ---------------- Full-full via 2D block prefix ----------------
    P = [[0] * (full_blocks + 1) for _ in range(full_blocks + 1)]
    for i in range(1, full_blocks + 1):
        row_sum = 0
        Pi = P[i]
        Pim1 = P[i - 1]
        Ci = C[i - 1]
        for j in range(1, full_blocks + 1):
            row_sum += Ci[j - 1]
            Pi[j] = Pim1[j] + row_sum

    for i in range(K):
        ans[i] += P[fa[i]][fb[i]]

    # ---------------- A full blocks: B-remainder vs A-full ----------------
    if has_rb:
        cost_arrB = [0] * N
        prefixB = [0] * (N + 1)
        Y_l = Y
        B_start_l = B_start

        for a in range(full_blocks):
            av = A_sorted_vals[a]
            ap = A_sorted_pref[a]
            asum = A_sums[a]
            m = A_lens[a]

            j = 0
            ca = cost_arrB
            for v, idx in zip(B_g_vals, B_g_idxs):
                while j < m and av[j] < v:
                    j += 1
                sl = ap[j]
                ca[idx] = v * j - sl + (asum - sl) - v * (m - j)

            s = 0
            prefixB[0] = 0
            pref = prefixB
            for i in range(N):
                s += ca[i]
                pref[i + 1] = s

            for fa_val in range(a + 1, full_blocks + 1):
                for qi in queries_by_fa[fa_val]:
                    ans_l[qi] += pref[Y_l[qi]] - pref[B_start_l[qi]]

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    solve()