import sys
from collections import defaultdict

def solve():
    data = sys.stdin.read().split()
    N = int(data[0]); P = int(data[1])
    H = N // 2
    maxE = N * (N - 1) // 2

    # Binomial coefficients mod P via Pascal's rule (n up to maxE)
    C = [[0] * (maxE + 1) for _ in range(maxE + 1)]
    for n in range(maxE + 1):
        C[n][0] = 1 % P
        C[n][n] = 1 % P
        for k in range(1, n):
            C[n][k] = (C[n-1][k-1] + C[n-1][k]) % P

    # w[n][e] = C(n(n-1)/2, e): within-layer edge polynomials
    w = [None] * (N + 1)
    for n in range(N + 1):
        m = n * (n - 1) // 2
        poly = [0] * (maxE + 1)
        poly[0] = 1
        for _ in range(m):
            for e in range(maxE, 0, -1):
                poly[e] = (poly[e] + poly[e-1]) % P
        w[n] = poly

    # h[a][b][e] = number of bipartite edge sets between parts of sizes a,b
    # such that every vertex of the b-side has >=1 neighbor in the a-side.
    # Inclusion-exclusion: sum_j (-1)^j C(b,j) C(a(b-j), e)
    h = [[None] * (N + 1) for _ in range(N + 1)]
    for a in range(N + 1):
        for b in range(N + 1):
            poly = [0] * (maxE + 1)
            for j in range(b + 1):
                m = a * (b - j)
                cj = C[b][j]
                if j & 1:
                    for e in range(min(m, maxE) + 1):
                        poly[e] = (poly[e] - cj * C[m][e]) % P
                else:
                    for e in range(min(m, maxE) + 1):
                        poly[e] = (poly[e] + cj * C[m][e]) % P
            h[a][b] = poly

    # Precompute hw[a][b] = h[a][b] * w[b] (cross-layer covering edges times
    # within-new-layer edges), truncated to maxE. Only a,b <= H are reachable.
    hw = [[None] * (H + 1) for _ in range(H + 1)]
    hwdeg = [[0] * (H + 1) for _ in range(H + 1)]
    for a in range(1, H + 1):
        for b in range(1, H + 1):
            hab = h[a][b]
            wb = w[b]
            d1 = a * b
            d2 = b * (b - 1) // 2
            deg = min(d1 + d2, maxE)
            res = [0] * (deg + 1)
            for i in range(d1 + 1):
                vi = hab[i]
                if vi == 0:
                    continue
                lim = min(d2, deg - i)
                for j in range(lim + 1):
                    vj = wb[j]
                    if vj:
                        res[i+j] = (res[i+j] + vi * vj) % P
            hw[a][b] = res
            hwdeg[a][b] = deg

    # dp[(ev, od, p, a)] = polynomial in total edges for partial BFS-layer structures:
    # ev/od = total vertices placed in even/odd layers so far, p = parity of last layer,
    # a = size of last layer. Root: layer 0 = {1}, even.
    dp = defaultdict(lambda: [0] * (maxE + 1))
    dp[(1, 0, 0, 1)][0] = 1

    for used in range(1, N):
        cap_used = min(maxE, used * (used - 1) // 2)
        for (ev, od, p, a), poly in list(dp.items()):
            if ev + od != used:
                continue
            rem = N - used
            for b in range(1, rem + 1):
                if p == 0:
                    if od + b > H:
                        break
                    nev, nod = ev, od + b
                else:
                    if ev + b > H:
                        break
                    nev, nod = ev + b, od
                ways = C[rem][b]
                if ways == 0:
                    continue
                hwab = hw[a][b]
                d2 = hwdeg[a][b]
                cap_new = min(maxE, (used + b) * (used + b - 1) // 2)
                # conv = ways * poly * hwab, truncated to cap_new
                conv = [0] * (cap_new + 1)
                for i in range(cap_used + 1):
                    vi = poly[i]
                    if vi == 0:
                        continue
                    wv = ways * vi % P
                    lim = min(d2, cap_new - i)
                    for j in range(lim + 1):
                        vj = hwab[j]
                        if vj:
                            conv[i+j] = (conv[i+j] + wv * vj) % P
                dpoly = dp[(nev, nod, 1 - p, b)]
                for e in range(cap_new + 1):
                    v = conv[e]
                    if v:
                        dpoly[e] = (dpoly[e] + v) % P

    ans = [0] * (maxE + 1)
    for (ev, od, p, a), poly in dp.items():
        if ev == H and od == H:
            for e in range(maxE + 1):
                v = poly[e]
                if v:
                    ans[e] = (ans[e] + v) % P

    out = []
    for M in range(N - 1, maxE + 1):
        out.append(str(ans[M] % P))
    sys.stdout.write(' '.join(out) + '\n')

solve()