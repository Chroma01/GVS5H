import sys


def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])

    half = N // 2
    half1 = half + 1
    maxE = N * (N - 1) // 2

    C2 = [i * (i - 1) // 2 for i in range(N + 1)]

    # Maximum possible degree of the final polynomial (valid parity only).
    add = [[0] * (N + 1) for _ in range(N + 1)]
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            add[a][b] = C2[b] + a * b

    maxdeg0 = [[[-1] * (N + 1) for _ in range(half1)] for __ in range(N + 1)]
    maxdeg1 = [[[-1] * (N + 1) for _ in range(half1)] for __ in range(N + 1)]
    maxdeg0[1][1][1] = 0

    for used in range(1, N):
        rem = N - used
        for even in range(half1):
            md0 = maxdeg0[used][even]
            md1 = maxdeg1[used][even]
            for a in range(1, used + 1):
                d = md0[a]
                if d >= 0:
                    for b in range(1, rem + 1):
                        nu = used + b
                        nd = d + add[a][b]
                        if nd > maxdeg1[nu][even][b]:
                            maxdeg1[nu][even][b] = nd
                d = md1[a]
                if d >= 0:
                    for b in range(1, rem + 1):
                        ne = even + b
                        if ne <= half:
                            nu = used + b
                            nd = d + add[a][b]
                            if nd > maxdeg0[nu][ne][b]:
                                maxdeg0[nu][ne][b] = nd

    D = 0
    for a in range(1, N + 1):
        d = maxdeg0[N][half][a]
        if d > D:
            D = d
        d = maxdeg1[N][half][a]
        if d > D:
            D = d
    if D < 0:
        D = 0
    if D > maxE:
        D = maxE

    del maxdeg0, maxdeg1, add

    # Binomial coefficients for choosing labels of the next layer.
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = 1
        C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % P

    # can_finish[used][even][parity]: can still reach used=N, even=half.
    can = [[[False, False] for _ in range(half1)] for __ in range(N + 1)]
    can[N][half][0] = True
    can[N][half][1] = True

    for used in range(N - 1, 0, -1):
        rem = N - used
        for even in range(half1):
            for p in (0, 1):
                np = 1 - p
                ok = False
                for b in range(1, rem + 1):
                    ne = even + (b if np == 0 else 0)
                    if ne <= half and can[used + b][ne][np]:
                        ok = True
                        break
                can[used][even][p] = ok

    can_mask = [[0, 0] for _ in range(N + 1)]
    for used in range(N + 1):
        for p in (0, 1):
            m = 0
            for e in range(half1):
                if can[used][e][p]:
                    m |= 1 << e
            can_mask[used][p] = m

    # Structurally reachable states, also pruned by can_finish.
    mask0 = [[0] * (N + 1) for _ in range(N + 1)]
    mask1 = [[0] * (N + 1) for _ in range(N + 1)]
    if can[1][1][0]:
        mask0[1][1] = 1 << 1

    for used in range(1, N):
        rem = N - used
        for a in range(1, used + 1):
            m0 = mask0[used][a]
            if m0:
                for b in range(1, rem + 1):
                    nu = used + b
                    m = m0 & can_mask[nu][1]
                    if m:
                        mask1[nu][b] |= m
            m1 = mask1[used][a]
            if m1:
                for b in range(1, rem + 1):
                    nu = used + b
                    m = (m1 << b) & can_mask[nu][0]
                    if m:
                        mask0[nu][b] |= m

    stride = N + 1
    size = stride * stride * half1
    base = [[0] * (N + 1) for _ in range(N + 1)]
    for used in range(N + 1):
        for a in range(N + 1):
            base[used][a] = (used * stride + a) * half1

    reach0 = [[[] for _ in range(N + 1)] for __ in range(N + 1)]
    reach1 = [[[] for _ in range(N + 1)] for __ in range(N + 1)]
    mod_info0 = [[] for _ in range(N + 1)]
    mod_info1 = [[] for _ in range(N + 1)]

    for used in range(1, N + 1):
        for a in range(1, used + 1):
            m = mask0[used][a]
            if m:
                l = tuple(e for e in range(half1) if (m >> e) & 1)
                reach0[used][a] = l
                mod_info0[used].append((base[used][a], l))
            m = mask1[used][a]
            if m:
                l = tuple(e for e in range(half1) if (m >> e) & 1)
                reach1[used][a] = l
                mod_info1[used].append((base[used][a], l))

    # Precompute transitions with only feasible even-count indices.
    trans_by_used = [[] for _ in range(N + 1)]
    for used in range(1, N):
        rem = N - used
        for a in range(1, used + 1):
            r0 = reach0[used][a]
            r1 = reach1[used][a]
            if not r0 and not r1:
                continue
            src = base[used][a]
            for b in range(1, rem + 1):
                comb = C[rem][b]
                if comb == 0:
                    continue
                nu = used + b

                l0 = []
                if r0:
                    cm = can_mask[nu][1]
                    if cm:
                        l0 = [e for e in r0 if (cm >> e) & 1]

                l1 = []
                if r1:
                    cm = can_mask[nu][0]
                    if cm:
                        limit = half - b
                        if limit >= 0:
                            for e in r1:
                                if e > limit:
                                    break
                                if (cm >> (e + b)) & 1:
                                    l1.append(e)

                if l0 or l1:
                    dst0 = base[nu][b]
                    dst1 = dst0 + b
                    tidx = a * stride + b
                    trans_by_used[used].append(
                        (tidx, src, dst0, dst1, comb, tuple(l0), tuple(l1))
                    )

    final0 = []
    final1 = []
    for a in range(1, N + 1):
        if (mask0[N][a] >> half) & 1:
            final0.append(base[N][a] + half)
        if (mask1[N][a] >> half) & 1:
            final1.append(base[N][a] + half)

    trans_by_used = [tuple(x) for x in trans_by_used]
    mod_info0 = [tuple(x) for x in mod_info0]
    mod_info1 = [tuple(x) for x in mod_info1]
    final0 = tuple(final0)
    final1 = tuple(final1)

    start_ok = can[1][1][0]
    start_idx = base[1][1] + 1

    del can, can_mask, mask0, mask1, reach0, reach1, base, C

    # Factorials for interpolation.
    fact = [1] * (D + 1)
    for i in range(1, D + 1):
        fact[i] = fact[i - 1] * i % P
    invfact = [1] * (D + 1)
    invfact[D] = pow(fact[D], P - 2, P)
    for i in range(D, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    # Evaluate the edge-count generating function at x = 0..D.
    vals = [0] * (D + 1)
    pow_len = max(maxE, N) + 1

    for x in range(1, D + 1):
        r = x + 1
        pow_r = [1] * pow_len
        for e in range(1, pow_len):
            pow_r[e] = pow_r[e - 1] * r % P
        pow_C2 = [pow_r[c] for c in C2]

        trans_flat = [0] * (stride * stride)
        for a in range(1, N + 1):
            ua = pow_r[a] - 1
            if ua < 0:
                ua += P
            val = 1
            row = a * stride
            for b in range(1, N + 1):
                val = val * ua % P
                trans_flat[row + b] = pow_C2[b] * val % P

        dp0 = [0] * size
        dp1 = [0] * size
        if start_ok:
            dp0[start_idx] = 1

        d0 = dp0
        d1 = dp1
        tf = trans_flat
        mod = P

        for used in range(1, N):
            if not trans_by_used[used]:
                continue

            # Reduce source level modulo P before using it.
            for base_idx, reach in mod_info0[used]:
                for e in reach:
                    idx = base_idx + e
                    v = d0[idx]
                    if v >= mod:
                        d0[idx] = v % mod
            for base_idx, reach in mod_info1[used]:
                for e in reach:
                    idx = base_idx + e
                    v = d1[idx]
                    if v >= mod:
                        d1[idx] = v % mod

            for tidx, src, dst0, dst1, comb, l0, l1 in trans_by_used[used]:
                w = (comb * tf[tidx]) % mod
                if not w:
                    continue
                if l0:
                    for e in l0:
                        val = d0[src + e]
                        if val:
                            d1[dst0 + e] += val * w
                if l1:
                    for e in l1:
                        val = d1[src + e]
                        if val:
                            d0[dst1 + e] += val * w

        ans = 0
        for idx in final0:
            ans += d0[idx]
        for idx in final1:
            ans += d1[idx]
        vals[x] = ans % mod

    # Convert values at 0..D to monomial coefficients.
    y = vals[:]
    newton = [0] * (D + 1)
    mod = P
    for k in range(D + 1):
        newton[k] = y[0]
        for i in range(D - k):
            y[i] = (y[i + 1] - y[i]) % mod

    coeff = [0] * (D + 1)
    row = [0] * (D + 1)
    row[0] = 1

    # Signed Stirling numbers of the first kind, row by row.
    for k in range(D + 1):
        if k:
            km1 = k - 1
            for j in range(k, 0, -1):
                row[j] = (row[j - 1] - km1 * row[j]) % mod
            row[0] = 0

        factor = newton[k] * invfact[k] % mod
        if factor:
            for j in range(k + 1):
                coeff[j] = (coeff[j] + factor * row[j]) % mod

    out = []
    for m in range(N - 1, maxE + 1):
        if m <= D:
            out.append(str(coeff[m] % mod))
        else:
            out.append("0")

    sys.stdout.write(" ".join(out) + "\n")


if __name__ == "__main__":
    solve()