import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = list(map(int, data[pos:pos + N])); pos += N
    B = list(map(int, data[pos:pos + N])); pos += N
    K = int(data[pos]); pos += 1
    qs = list(map(int, data[pos:pos + 2 * K]))
    qx = qs[0::2]
    qy = qs[1::2]

    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        An = np.array(A, dtype=np.int64)
        Bn = np.array(B, dtype=np.int64)
        S = 1000
        if S > N:
            S = N
        M = (N + S - 1) // S

        # cumE[y][i] = sum_{i' < i} E[y][i'],  E[y][i'] = sum_{j < y*S} |A_i' - B_j|
        cumE = np.zeros((M + 1, N + 1), dtype=np.int64)
        curE = np.zeros(N, dtype=np.int64)
        for y in range(M):
            lo = y * S
            hi = lo + S
            if hi > N:
                hi = N
            sb = np.sort(Bn[lo:hi])
            L = sb.size
            ps = np.empty(L + 1, dtype=np.int64)
            ps[0] = 0
            ps[1:] = np.cumsum(sb)
            tot = ps[L]
            idx = np.searchsorted(sb, An, side='left')
            curE += An * idx - ps[idx] + (tot - ps[idx]) - An * (L - idx)
            cumE[y + 1, 1:] = np.cumsum(curE)

        # cumD[x][j] = sum_{j' < j} D[x][j'],  D[x][j'] = sum_{i < x*S} |A_i - B_j'|
        cumD = np.zeros((M + 1, N + 1), dtype=np.int64)
        curD = np.zeros(N, dtype=np.int64)
        for x in range(M):
            lo = x * S
            hi = lo + S
            if hi > N:
                hi = N
            sa = np.sort(An[lo:hi])
            L = sa.size
            ps = np.empty(L + 1, dtype=np.int64)
            ps[0] = 0
            ps[1:] = np.cumsum(sa)
            tot = ps[L]
            idx = np.searchsorted(sa, Bn, side='left')
            curD += Bn * idx - ps[idx] + (tot - ps[idx]) - Bn * (L - idx)
            cumD[x + 1, 1:] = np.cumsum(curD)

        qxa = np.array(qx, dtype=np.int64)
        qya = np.array(qy, dtype=np.int64)
        xb = qxa // S
        yb = qya // S
        xs = xb * S
        ys = yb * S
        base = cumE[yb, qxa] + cumD[xb, qya] - cumD[xb, ys]

        res = []
        for i in range(K):
            a0 = int(xs[i]); a1 = int(qxa[i])
            b0 = int(ys[i]); b1 = int(qya[i])
            if a1 > a0 and b1 > b0:
                PA = np.sort(An[a0:a1])
                Lp = PA.size
                psp = np.empty(Lp + 1, dtype=np.int64)
                psp[0] = 0
                psp[1:] = np.cumsum(PA)
                tot = psp[Lp]
                PB = Bn[b0:b1]
                j2 = np.searchsorted(PA, PB, side='left')
                cross = int((PB * j2 - psp[j2] + (tot - psp[j2]) - PB * (Lp - j2)).sum())
            else:
                cross = 0
            res.append(int(base[i]) + cross)
        sys.stdout.write("\n".join(map(str, res)))
    else:
        from bisect import bisect_left
        from array import array

        def zarr(n):
            return array('q', bytes(8 * n))

        S = 1000
        if S > N:
            S = N
        M = (N + S - 1) // S

        cumE = [zarr(N + 1)]
        curE = [0] * N
        for y in range(M):
            lo = y * S
            hi = min(lo + S, N)
            block = sorted(B[lo:hi])
            L = len(block)
            pref = [0] * (L + 1)
            s = 0
            for t in range(L):
                s += block[t]
                pref[t + 1] = s
            tot = pref[L]
            for i in range(N):
                a = A[i]
                p = bisect_left(block, a)
                curE[i] += a * p - pref[p] + (tot - pref[p]) - a * (L - p)
            row = zarr(N + 1)
            ss = 0
            for i in range(N):
                ss += curE[i]
                row[i + 1] = ss
            cumE.append(row)

        cumD = [zarr(N + 1)]
        curD = [0] * N
        for x in range(M):
            lo = x * S
            hi = min(lo + S, N)
            block = sorted(A[lo:hi])
            L = len(block)
            pref = [0] * (L + 1)
            s = 0
            for t in range(L):
                s += block[t]
                pref[t + 1] = s
            tot = pref[L]
            for j in range(N):
                b = B[j]
                p = bisect_left(block, b)
                curD[j] += b * p - pref[p] + (tot - pref[p]) - b * (L - p)
            row = zarr(N + 1)
            ss = 0
            for j in range(N):
                ss += curD[j]
                row[j + 1] = ss
            cumD.append(row)

        res = []
        for t in range(K):
            X = qx[t]; Y = qy[t]
            xb = X // S; yb = Y // S
            xs = xb * S; ys = yb * S
            base = cumE[yb][X] + cumD[xb][Y] - cumD[xb][ys]
            PA = sorted(A[xs:X])
            PB = sorted(B[ys:Y])
            cross = 0
            if PA and PB:
                Lp = len(PB)
                pref = [0] * (Lp + 1)
                s = 0
                for u in range(Lp):
                    s += PB[u]
                    pref[u + 1] = s
                tot = pref[Lp]
                for a in PA:
                    q = bisect_left(PB, a)
                    cross += a * q - pref[q] + (tot - pref[q]) - a * (Lp - q)
            res.append(base + cross)
        sys.stdout.write("\n".join(map(str, res)))


main()